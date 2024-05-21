from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, BotCommand
from states.user_states import FilterState
from functions.get_recipes_by_products import find_matching_dishes, filter_dishes_by_preferences_and_exclusions
from functions.format_recipe_message import format_recipe_message
from keyboards.inline_keyboards import create_ingredient_keyboard, PreferenceCallback, ExcludeCallback
import json

button_menu = KeyboardButton(text="Получить меню на день")
button_help = KeyboardButton(text="Помощь")

keyboard = ReplyKeyboardMarkup(keyboard=[[button_menu, button_help]], resize_keyboard=True)

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/help', description='Справка по работе бота'),
        BotCommand(command='/support', description='Поддержка'),
        BotCommand(command='/contacts', description='Другие способы связи'),
        BotCommand(command='/menu', description='Питание на День'),
        BotCommand(command='/start', description='Перезапуск бота'),
    ]
    await bot.set_my_commands(main_menu_commands)

async def process_start_command(message: Message):
    await message.answer("Привет! Я бот для получения рецептов. Напиши /help, чтобы узнать, что я умею.", reply_markup=keyboard)

async def process_help_command(message: Message):
    await message.answer("I don't have help :(")

async def process_ingredient_preferences(message: types.Message, state: FSMContext):
    ingredients = ["паста", "томаты", "оливковое масло", "лук", "чеснок", "базилик"]  # Примерный список ингредиентов
    await message.answer("Выберите ваши предпочтения и исключения:", reply_markup=create_ingredient_keyboard(ingredients))
    await state.set_state(FilterState.EnterPreferences)

async def preference_callback_handler(callback_query: types.CallbackQuery, callback_data: PreferenceCallback, state: FSMContext):
    user_data = await state.get_data()
    preferences = user_data.get("preferences", [])
    preferences.append(callback_data["ingredient"])
    await state.update_data(preferences=preferences)
    await callback_query.answer(f"{callback_data['ingredient']} добавлен в предпочтения")

async def exclusion_callback_handler(callback_query: types.CallbackQuery, callback_data: ExcludeCallback, state: FSMContext):
    user_data = await state.get_data()
    exclusions = user_data.get("exclusions", [])
    exclusions.append(callback_data["ingredient"])
    await state.update_data(exclusions=exclusions)
    await callback_query.answer(f"{callback_data['ingredient']} добавлен в исключения")

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

async def process_invalid_command(message: Message):
    await message.answer("Такой команды нет :(")
