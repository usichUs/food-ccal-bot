import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from setting.settings import TOKEN
from database import init_db
from populate_db import populate_db

DATABASE = 'bot_database.db'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

def get_user_data(user_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT weight, height, age, physical_activity_level FROM user WHERE id = ?', (user_id,))
        return cursor.fetchone()

def update_user_data(user_id, weight, height, age, activity_level):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO user (id, weight, height, age, physical_activity_level)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
            weight = excluded.weight,
            height = excluded.height,
            age = excluded.age,
            physical_activity_level = excluded.physical_activity_level
        ''', (user_id, weight, height, age, activity_level))
        connection.commit()

def get_random_meal():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT name, description FROM meals ORDER BY RANDOM() LIMIT 1')
        return cursor.fetchone()

def get_healthy_foods():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT name, description FROM healthy_foods')
        return cursor.fetchall()

def get_nutrition_tips():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT tip FROM nutrition_tips')
        return cursor.fetchall()

def get_activity_tips():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT tip FROM activity_tips')
        return cursor.fetchall()

def get_user_meal_plan(user_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT mb.name, ml.name, md.name, ms.name 
            FROM user_meal_plan ump
            LEFT JOIN meal_breakfast mb ON ump.breakfast_id = mb.id
            LEFT JOIN meal_lunch ml ON ump.lunch_id = ml.id
            LEFT JOIN meal_dinner md ON ump.dinner_id = md.id
            LEFT JOIN meal_snacks ms ON ump.snack_id = ms.id
            WHERE ump.user_id = ?
        ''', (user_id,))
        return cursor.fetchone()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить рецепт", callback_data="get_recipe")],
        [InlineKeyboardButton(text="Полезные продукты", callback_data="healthy_foods")],
        [InlineKeyboardButton(text="Рекомендации по питанию", callback_data="nutrition_tips")],
        [InlineKeyboardButton(text="Рекомендации по активности", callback_data="activity_tips")],
        [InlineKeyboardButton(text="План питания на день", callback_data="meal_plan")],
        [InlineKeyboardButton(text="Мои данные", callback_data="my_data")]
    ])
    await message.answer("Привет! Я бот для расчета питания. Что вы хотите сделать?", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == 'my_data')
async def my_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        weight, height, age, activity_level = user_data
        response = f"Ваши данные:\n\nВес: {weight}\nРост: {height}\nВозраст: {age}\nУровень активности: {activity_level}"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Изменить параметры", callback_data="set_parameters")]
        ])
        
        await callback_query.message.answer(response, reply_markup=keyboard)
    else:
        await callback_query.message.answer("Данные пользователя не найдены. Пожалуйста, задайте параметры сначала.")

@dp.callback_query(lambda c: c.data == 'set_parameters')
async def set_parameters(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите ваши данные в формате: вес, рост, возраст, уровень активности (низкий, средний, высокий). Пример: 70 170 30 средний")

@dp.message(lambda message: ' ' in message.text and len(message.text.split()) == 4)
async def handle_parameters(message: types.Message):
    user_id = message.from_user.id
    try:
        weight, height, age, activity_level = message.text.split()
        update_user_data(user_id, weight=float(weight), height=float(height), age=int(age), activity_level=activity_level)
        await message.answer("Ваши данные обновлены.")
    except Exception as e:
        await message.answer("Ошибка при вводе данных. Убедитесь, что вы ввели данные в правильном формате.")

@dp.callback_query(lambda c: c.data == 'get_recipe')
async def get_recipe(callback_query: types.CallbackQuery):
    meal = get_random_meal()
    if meal:
        await callback_query.message.answer(f"Рецепт: {meal[0]}\nОписание: {meal[1]}")
    else:
        await callback_query.message.answer("Не удалось найти рецепт.")

@dp.callback_query(lambda c: c.data == 'healthy_foods')
async def healthy_foods(callback_query: types.CallbackQuery):
    foods = get_healthy_foods()
    response = "\n\n".join([f"{food[0]}: {food[1]}" for food in foods])
    await callback_query.message.answer(f"Полезные продукты:\n\n{response}")

@dp.callback_query(lambda c: c.data == 'nutrition_tips')
async def nutrition_tips(callback_query: types.CallbackQuery):
    tips = get_nutrition_tips()
    response = "\n\n".join([tip[0] for tip in tips])
    await callback_query.message.answer(f"Рекомендации по питанию:\n\n{response}")

@dp.callback_query(lambda c: c.data == 'activity_tips')
async def activity_tips(callback_query: types.CallbackQuery):
    tips = get_activity_tips()
    response = "\n\n".join([tip[0] for tip in tips])
    await callback_query.message.answer(f"Рекомендации по активности:\n\n{response}")

@dp.callback_query(lambda c: c.data == 'meal_plan')
async def meal_plan(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    plan = get_user_meal_plan(user_id)
    if plan:
        response = f"Ваш план питания на день:\n\nЗавтрак: {plan[0]}\nОбед: {plan[1]}\nУжин: {plan[2]}\nПерекус: {plan[3]}"
        await callback_query.message.answer(response)
    else:
        await callback_query.message.answer("Не удалось найти план питания. Пожалуйста, задайте параметры сначала.")

if __name__ == "main":
    init_db()
    populate_db()
    dp.run_polling(bot, skip_updates=True)
