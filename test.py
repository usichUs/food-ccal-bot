import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from setting.settings import TOKEN
from data.text_data import (
    recipes, healthy_foods, nutrition_tips, activity_tips, 
    meal_plan_templates, activity_level_description, bot_description
)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения данных пользователей
user_data = {}

# Функция для инициализации данных пользователя
def init_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {
            'weight': None, 'height': None, 'age': None, 
            'gender': None, 'activity_level': None, 'current_action': None
        }

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить рецепт", callback_data="get_recipe")],
        [InlineKeyboardButton(text="Полезные продукты", callback_data="get_healthy_food")],
        [InlineKeyboardButton(text="Рекомендации по питанию", callback_data="get_nutrition_tips")],
        [InlineKeyboardButton(text="Рекомендации по активности", callback_data="get_activity_tips")],
        [InlineKeyboardButton(text="План питания на день", callback_data="get_meal_plan")],
        [InlineKeyboardButton(text="Мои данные", callback_data="my_data")]
    ])
    await message.answer("Привет! Я бот для помощи с питанием. Выберите действие:", reply_markup=keyboard)

# Обработчик команды /description
@dp.message(Command('description'))
async def send_description(message: types.Message):
    await message.answer(bot_description)

# Обработчик нажатий кнопок
@dp.callback_query(F.data == "get_recipe")
async def send_random_recipe(callback: types.CallbackQuery):
    recipe = random.choice(recipes)
    await callback.message.answer(f"Ваш случайный рецепт: {recipe}")
    await callback.answer()

@dp.callback_query(F.data == "get_healthy_food")
async def send_healthy_food(callback: types.CallbackQuery):
    food = random.choice(healthy_foods)
    await callback.message.answer(f"Полезный продукт: {food}")
    await callback.answer()

@dp.callback_query(F.data == "get_nutrition_tips")
async def send_nutrition_tips(callback: types.CallbackQuery):
    tip = random.choice(nutrition_tips)
    await callback.message.answer(f"Рекомендация по питанию: {tip}")
    await callback.answer()

@dp.callback_query(F.data == "get_activity_tips")
async def send_activity_tips(callback: types.CallbackQuery):
    tip = random.choice(activity_tips)
    await callback.message.answer(f"Рекомендация по физической активности: {tip}")
    await callback.answer()

@dp.callback_query(F.data == "get_meal_plan")
async def request_meal_plan_info(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    user_data[user_id]['current_action'] = 'meal_plan'
    await callback.message.answer("Введите ваши данные в формате: вес(кг) рост(см) возраст")
    await callback.answer()

# Функция для расчета суточной потребности в калориях
def calculate_calories(weight, height, age, gender, activity_level):
    if gender == 'м':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
    
    if activity_level == 'низкий':
        calories = bmr * 1.2
    elif activity_level == 'средний':
        calories = bmr * 1.55
    else:
        calories = bmr * 1.725
    
    return calories

# Функция для расчета ИМТ
def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        return bmi, "Недостаточный вес"
    elif 18.5 <= bmi < 24.9:
        return bmi, "Нормальный вес"
    elif 25 <= bmi < 29.9:
        return bmi, "Избыточный вес"
    else:
        return bmi, "Ожирение"

@dp.callback_query(F.data == "my_data")
async def show_user_data(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    
    data = user_data[user_id]
    bmi, bmi_status = calculate_bmi(data['weight'], data['height']) if data['weight'] and data['height'] else (None, None)
    
    response = (
        f"Ваши данные:\n"
        f"Вес: {data['weight']} кг\n"
        f"Рост: {data['height']} см\n"
        f"Возраст: {data['age']} лет\n"
        f"Пол: {'Мужской' if data['gender'] == 'м' else 'Женский'}\n"
        f"Уровень активности: {data['activity_level']}\n"
        f"ИМТ: {bmi:.2f} ({bmi_status})" if bmi else "ИМТ: не рассчитан"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить вес", callback_data="change_weight")],
        [InlineKeyboardButton(text="Изменить рост", callback_data="change_height")],
        [InlineKeyboardButton(text="Изменить возраст", callback_data="change_age")],
        [InlineKeyboardButton(text="Изменить уровень активности", callback_data="change_activity_level")],
        [InlineKeyboardButton(text="Обновить план питания", callback_data="update_meal_plan")]
    ])
    
    await callback.message.answer(response, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data == "change_weight")
async def change_weight(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    user_data[user_id]['current_action'] = 'weight'
    await callback.message.answer("Введите новый вес в кг:")
    await callback.answer()

@dp.callback_query(F.data == "change_height")
async def change_height(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    user_data[user_id]['current_action'] = 'height'
    await callback.message.answer("Введите новый рост в см:")
    await callback.answer()

@dp.callback_query(F.data == "change_age")
async def change_age(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    user_data[user_id]['current_action'] = 'age'
    await callback.message.answer("Введите новый возраст:")
    await callback.answer()

@dp.callback_query(F.data == "change_activity_level")
async def change_activity_level(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Низкий", callback_data="activity_low")],
        [InlineKeyboardButton(text="Средний", callback_data="activity_medium")],
        [InlineKeyboardButton(text="Высокий", callback_data="activity_high")]
    ])
    await callback.message.answer(activity_level_description, reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data.in_({"activity_low", "activity_medium", "activity_high"}))
async def set_activity_level(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    
    if callback.data == "activity_low":
        user_data[user_id]['activity_level'] = "низкий"
    elif callback.data == "activity_medium":
        user_data[user_id]['activity_level'] = "средний"
    else:
        user_data[user_id]['activity_level'] = "высокий"
    
    await show_user_data(callback)

@dp.callback_query(F.data == "update_meal_plan")
async def update_meal_plan(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    init_user_data(user_id)
    
    if None in [user_data[user_id][key] for key in ('weight', 'height', 'age', 'gender', 'activity_level')]:
        await callback.message.answer("Пожалуйста, заполните все данные перед обновлением плана питания.")
        await callback.answer()
        return
    
    weight = user_data[user_id]['weight']
    height = user_data[user_id]['height']
    age = user_data[user_id]['age']
    gender = user_data[user_id]['gender']
    activity_level = user_data[user_id]['activity_level']
    
    calories = calculate_calories(weight, height, age, gender, activity_level)
    meal_plan = random.choice(meal_plan_templates)
    
    response = (
        f"Ваш обновленный план питания на день (примерно {calories:.0f} калорий):\n\n"
        f"Завтрак: {meal_plan['breakfast']}\n"
        f"Обед: {meal_plan['lunch']}\n"
        f"Ужин: {meal_plan['dinner']}\n"
        f"Перекусы: {meal_plan['snacks']}\n"
    )
    
    await callback.message.answer(response)
    await callback.answer()

# Обработчик текстовых сообщений для изменения данных пользователя
@dp.message(F.text.regexp(r'^\d+(\.\d+)?$'))
async def handle_numeric_input(message: types.Message):
    user_id = message.from_user.id
    init_user_data(user_id)
    
    # Определение, какой параметр обновляется
    current_action = user_data[user_id].get('current_action')
    if current_action:
        value = float(message.text) if '.' in message.text else int(message.text)
        user_data[user_id][current_action] = value
        user_data[user_id]['current_action'] = None
        await show_user_data(message)
    else:
        await message.reply("Введите команду для изменения данных или используйте кнопки.")

# Установка команд бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/description", description="Описание функционала бота"),
        BotCommand(command="/advice", description="Получить совет по питанию"),
        BotCommand(command="/healthy_food", description="Информация о полезных продуктах"),
        BotCommand(command="/activity", description="Рекомендации по физической активности"),
        BotCommand(command="/meal_plan", description="Создать план питания"),
        BotCommand(command="/my_data", description="Посмотреть и изменить мои данные")
    ]
    await bot.set_my_commands(commands)

# Запуск бота
if __name__ == '__main__':
    dp.startup.register(set_commands)
    dp.run_polling(bot)
