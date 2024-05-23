from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
import json

from setting.settings import TOKEN
from functions.format_recipe_message import format_recipe_message

bot = Bot(token=TOKEN)
dp = Dispatcher()

button_menu = KeyboardButton(text="Получить меню на день", callback_data="menu")
button_help = KeyboardButton(text="Помощь", callback_data="help")

keyboard = ReplyKeyboardMarkup(keyboard=[[button_menu, button_help]], resize_keyboard=True)

class PreferenceCallback(CallbackData, prefix="pref"):
    action: str
    ingredient: str

class ExcludeCallback(CallbackData, prefix="exclude"):
    action: str
    ingredient: str

class ProductState(StatesGroup):
    EnterProducts = State()

class FilterState(StatesGroup):
    EnterPreferences = State()
    EnterExclusions = State()

with open("receipts/receipts.json", "r") as file:
    dishes = json.load(file)

def find_matching_dishes(user_products):
    matching_dishes = []
    for dish in dishes:
        if all(ingredient in user_products for ingredient in dish["ingredients"]):
            matching_dishes.append(dish)
    return matching_dishes

def filter_dishes_by_preferences_and_exclusions(preferences, exclusions):
    filtered_dishes = []
    for dish in dishes:
        if all(ingredient not in exclusions for ingredient in dish["ingredients"]) and all(ingredient in dish["ingredients"] for ingredient in preferences):
            filtered_dishes.append(dish)
    return filtered_dishes

def create_ingredient_keyboard(ingredients):
    keyboard = InlineKeyboardMarkup()
    for ingredient in ingredients:
        keyboard.add(
            InlineKeyboardButton(
                text=f"Предпочитаю {ingredient}",
                callback_data=PreferenceCallback(action="prefer", ingredient=ingredient).pack()
            ),
            InlineKeyboardButton(
                text=f"Исключить {ingredient}",
                callback_data=ExcludeCallback(action="exclude", ingredient=ingredient).pack()
            )
        )
    return keyboard

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/support', description='Поддержка'),
        BotCommand(command='/contacts', description='Другие способы связи'),
        BotCommand(command='/menu', description='Питание на День'),
        BotCommand(command='/start', description='Перезапуск бота'),
    ]
    await bot.set_my_commands(main_menu_commands)

async def process_enter_products(message: types.Message, state: FSMContext):
    await message.answer("Введите через запятую продукты, которые у вас есть.")
    await state.set_state(ProductState.EnterProducts)

async def process_user_products(message: types.Message, state: FSMContext):
    user_products = message.text.split(", ")
    matching_dishes = find_matching_dishes(user_products)
    if matching_dishes:
        response = "Можно приготовить следующие блюда:\n"
        for dish in matching_dishes:
            response += f"- {dish['name']}\n"
    else:
        response = "Из введенных продуктов нельзя приготовить ни одного блюда."
    await message.answer(response)

async def process_ingredient_preferences(message: types.Message, state: FSMContext):
    ingredients = ["паста", "томаты", "оливковое масло", "лук", "чеснок", "базилик"]  # Примерный список ингредиентов
    await message.answer("Выберите ваши предпочтения и исключения:", reply_markup=create_ingredient_keyboard(ingredients))
    await state.set_state(FilterState.EnterPreferences)

async def preference_callback_handler(callback_query: types.CallbackQuery, callback_data: PreferenceCallback, state: FSMContext):
    user_data = await state.get_data()
    preferences = user_data.get("preferences", [])
    preferences.append(callback_data.ingredient)
    await state.update_data(preferences=preferences)
    await callback_query.answer(f"{callback_data.ingredient} добавлен в предпочтения")

async def exclusion_callback_handler(callback_query: types.CallbackQuery, callback_data: ExcludeCallback, state: FSMContext):
    user_data = await state.get_data()
    exclusions = user_data.get("exclusions", [])
    exclusions.append(callback_data.ingredient)
    await state.update_data(exclusions=exclusions)
    await callback_query.answer(f"{callback_data.ingredient} добавлен в исключения")

async def process_filtered_dishes_command(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    preferences = user_data.get("preferences", [])
    exclusions = user_data.get("exclusions", [])
    filtered_dishes = filter_dishes_by_preferences_and_exclusions(preferences, exclusions)

    if filtered_dishes:
        response = "Можно приготовить следующие блюда с учетом ваших предпочтений и исключений:\n"
        for dish in filtered_dishes:
            response += f"- {dish['name']}\n"
    else:
        response = "Нет блюд, соответствующих вашим предпочтениям и исключениям."

    await message.answer(response)

async def process_menu_command(message: Message):
    with open('receipts/receipts.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)
    
    breakfast_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Breakfast')
    await message.answer(format_recipe_message(breakfast_recipe), parse_mode='HTML')
    
    lunch_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Lunch')
    await message.answer(format_recipe_message(lunch_recipe), parse_mode='HTML')
    
    dinner_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Dinner')
    await message.answer(format_recipe_message(dinner_recipe), parse_mode='HTML')

async def process_menu_command_wrapper(message: Message):
    await process_menu_command(message)

async def process_start_command(message: Message):
    await message.answer("Привет! Я бот для получения рецептов. Напиши /help, чтобы узнать, что я умею.", reply_markup=keyboard)

async def process_help_command(message: Message):
    await message.answer("I don't have help :(")

async def process_invalid_command(message: Message):
    await message.answer("Такой команды нет :(")

dp.message.register(process_enter_products, Command(commands=["available_dishes"]))
dp.message.register(process_user_products, ProductState.EnterProducts)
dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(process_menu_command_wrapper, Command(commands=["menu"]))
dp.message.register(process_menu_command_wrapper, F.text == "Получить меню на день")
dp.message.register(process_help_command, F.text == "Помощь")
dp.message.register(process_ingredient_preferences, Command(commands=["filter_dishes"]))
dp.message.register(process_filtered_dishes_command, Command(commands=["show_filtered_dishes"]))
dp.callback_query.register(preference_callback_handler, PreferenceCallback.filter())
dp.callback_query.register(exclusion_callback_handler, ExcludeCallback.filter())
dp.callback_query.register(process_menu_command_wrapper, F.data == "menu")
dp.callback_query.register(process_help_command, F.data == "help")
dp.startup.register(set_main_menu)
dp.message.register(process_invalid_command)

if __name__ == '__main__':
    dp.run_polling(bot)
