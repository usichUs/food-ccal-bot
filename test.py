import sqlite3
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram import Router
from setting.settings import TOKEN
from database import reset_db
from populate_db import populate_db
 
DATABASE = 'bot_database.db'
 
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
 
user_states = {}
 
def get_user_data(user_id):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT weight, height, age, gender, physical_activity_level FROM user WHERE id = ?', (user_id,))
        return cursor.fetchone()
 
def update_user_data(user_id, weight=None, height=None, age=None, gender=None, activity_level=None):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT weight, height, age, gender, physical_activity_level FROM user WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        
        if user_data:
            weight = weight if weight is not None else user_data[0]
            height = height if height is not None else user_data[1]
            age = age if age is not None else user_data[2]
            gender = gender if gender is not None else user_data[3]
            activity_level = activity_level if activity_level is not None else user_data[4]
 
            cursor.execute('''
                UPDATE user SET weight = ?, height = ?, age = ?, gender = ?, physical_activity_level = ?
                WHERE id = ?
            ''', (weight, height, age, gender, activity_level, user_id))
        else:
            cursor.execute('''
                INSERT INTO user (id, weight, height, age, gender, physical_activity_level)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, weight, height, age, gender, activity_level))
        
        connection.commit()
 
def get_random_meal():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT meals.id, meals.name, meals.description, meals.calories, meal_links.url, 
                   IFNULL(AVG(meal_ratings.rating), 0) as avg_rating, COUNT(meal_ratings.rating) as rating_count
            FROM meals
            LEFT JOIN meal_links ON meals.id = meal_links.meal_id
            LEFT JOIN meal_ratings ON meals.id = meal_ratings.meal_id
            GROUP BY meals.id
            ORDER BY RANDOM() LIMIT 1
        ''')
        return cursor.fetchone()
 
def get_random_healthy_food():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT name, description FROM healthy_foods ORDER BY RANDOM() LIMIT 1')
        return cursor.fetchone()
 
def get_random_nutrition_tip():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT tip FROM nutrition_tips ORDER BY RANDOM() LIMIT 1')
        return cursor.fetchone()
 
def get_random_activity_tip():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT tip FROM activity_tips ORDER BY RANDOM() LIMIT 1')
        return cursor.fetchone()
 
def get_random_meal_by_type(exclude_ids):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        query = '''
            SELECT meals.id, meals.name, meals.description, meals.calories, meal_links.url, 
                   IFNULL(AVG(meal_ratings.rating), 0) as avg_rating
            FROM meals
            LEFT JOIN meal_links ON meals.id = meal_links.meal_id
            LEFT JOIN meal_ratings ON meals.id = meal_ratings.meal_id
            WHERE meals.id NOT IN ({})
            GROUP BY meals.id
            ORDER BY avg_rating DESC, RANDOM() LIMIT 1
        '''.format(','.join('?' for _ in exclude_ids))
        cursor.execute(query, exclude_ids)
        return cursor.fetchone()
 
def calculate_calories(weight, height, age, gender, activity_level):
    if gender == 'Мужской':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
 
    if activity_level == 'низкий':
        return bmr * 1.2
    elif activity_level == 'средний':
        return bmr * 1.55
    else:
        return bmr * 1.725
 
def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2
 
@router.message(Command('start'))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить рецепт", callback_data="get_recipe")],
        [InlineKeyboardButton(text="Полезные продукты", callback_data="healthy_foods")],
        [InlineKeyboardButton(text="Рекомендации по питанию", callback_data="nutrition_tips")],
        [InlineKeyboardButton(text="Рекомендации по активности", callback_data="activity_tips")],
        [InlineKeyboardButton(text="План питания на день", callback_data="meal_plan")],
        [InlineKeyboardButton(text="Мои данные", callback_data="my_data")],
        [InlineKeyboardButton(text="Заполнить данные", callback_data="fill_data")],
    ])
    await message.answer(
        "Привет! Я бот для расчета питания. Вот что я могу сделать:\n\n"
        "/start - Показать это сообщение\n"
        "/get_recipe - Получить случайный рецепт\n"
        "/healthy_foods - Полезные продукты\n"
        "/nutrition_tips - Рекомендации по питанию\n"
        "/activity_tips - Рекомендации по активности\n"
        "/meal_plan - План питания на день\n"
        "/my_data - Мои данные\n"
        "/search_meals - Поиск блюд по ключевому слову\n"
        "/rate_meal - Оценить блюдо\n\n"
        "Что вы хотите сделать?", 
        reply_markup=keyboard
    )
 
@router.callback_query(lambda c: c.data == 'my_data')
async def my_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        weight, height, age, gender, activity_level = user_data
        bmi = calculate_bmi(weight, height)
        calories = calculate_calories(weight, height, age, gender, activity_level)
        
        # Get today's meal plan
        today_date = datetime.now().date()
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT breakfast_id, lunch_id, dinner_id, snack_id 
                FROM user_meal_plan 
                WHERE user_id = ? AND date = ?
            ''', (user_id, today_date))
            meal_plan = cursor.fetchone()
        
        meal_plan_str = ""
        total_calories = 0
        
        if meal_plan:
            meal_ids = [meal_plan[0], meal_plan[1], meal_plan[2], meal_plan[3]]
            for meal_id in meal_ids:
                cursor.execute('SELECT name, description, calories, meal_links.url FROM meals LEFT JOIN meal_links ON meals.id = meal_links.meal_id WHERE meals.id = ?', (meal_id,))
                meal = cursor.fetchone()
                meal_plan_str += f"{meal[0]} - {meal[1]} ({meal[2]} ккал)\nСсылка: {meal[3]}\n"
                total_calories += meal[2]
        
        response = (
            f"<b>Ваши данные:</b>\n\n"
            f"Вес: {weight} кг\n"
            f"Рост: {height} см\n"
            f"Возраст: {age} лет\n"
            f"Пол: {gender}\n"
            f"Уровень активности: {activity_level}\n"
            f"ИМТ: {bmi:.2f}\n"
            f"Рекомендуемая калорийность: {calories:.2f} ккал\n\n"
            f"<b>Ваш план питания на день:</b>\n{meal_plan_str}\n"
            f"Общая калорийность: {total_calories} ккал"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Изменить вес", callback_data="set_weight")],
            [InlineKeyboardButton(text="Изменить рост", callback_data="set_height")],
            [InlineKeyboardButton(text="Изменить возраст", callback_data="set_age")],
            [InlineKeyboardButton(text="Изменить пол", callback_data="set_gender")],
            [InlineKeyboardButton(text="Изменить активность", callback_data="set_activity")]
        ])
        
        await callback_query.message.answer(response, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback_query.message.answer("Данные пользователя не найдены. Пожалуйста, заполните параметры сначала.")

@router.callback_query(lambda c: c.data == 'fill_data')
async def fill_data(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_states[user_id] = 'weight'
    await callback_query.message.answer("Введите ваш вес (кг):")
 
@router.callback_query(lambda c: c.data in ['set_weight', 'set_height', 'set_age', 'set_gender', 'set_activity'])
async def set_parameters(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = callback_query.data.split('_')[1]
    user_states[user_id] = state
    
    if state == 'weight':
        await callback_query.message.answer("Введите ваш вес (кг):")
    elif state == 'height':
        await callback_query.message.answer("Введите ваш рост (см):")
    elif state == 'age':
        await callback_query.message.answer("Введите ваш возраст (лет):")
    elif state == 'gender':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Мужской", callback_data="gender_male")],
            [InlineKeyboardButton(text="Женский", callback_data="gender_female")]
        ])
        await callback_query.message.answer("Выберите ваш пол:", reply_markup=keyboard)
    elif state == 'activity':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Низкий (малоподвижный образ жизни)", callback_data="activity_low")],
            [InlineKeyboardButton(text="Средний (умеренная активность)", callback_data="activity_medium")],
            [InlineKeyboardButton(text="Высокий (высокая активность)", callback_data="activity_high")]
        ])
        await callback_query.message.answer("Выберите уровень активности:", reply_markup=keyboard)
 
@router.message(lambda message: message.text.isdigit() and user_states.get(message.from_user.id) == 'weight')
async def handle_weight(message: types.Message):
    weight = float(message.text)
    user_id = message.from_user.id
    update_user_data(user_id, weight=weight)
    user_states[user_id] = 'height'
    await message.answer("Введите ваш рост (см):")
 
@router.message(lambda message: message.text.isdigit() and user_states.get(message.from_user.id) == 'height')
async def handle_height(message: types.Message):
    height = float(message.text)
    user_id = message.from_user.id
    update_user_data(user_id, height=height)
    user_states[user_id] = 'age'
    await message.answer("Введите ваш возраст (лет):")
 
@router.message(lambda message: message.text.isdigit() and user_states.get(message.from_user.id) == 'age')
async def handle_age(message: types.Message):
    age = int(message.text)
    user_id = message.from_user.id
    update_user_data(user_id, age=age)
    user_states[user_id] = 'gender'
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мужской", callback_data="gender_male")],
        [InlineKeyboardButton(text="Женский", callback_data="gender_female")]
    ])
    await message.answer("Выберите ваш пол:", reply_markup=keyboard)
 
@router.callback_query(lambda c: user_states.get(c.from_user.id) == 'gender' and c.data in ['gender_male', 'gender_female'])
async def handle_gender(callback_query: types.CallbackQuery):
    gender = "Мужской" if callback_query.data == 'gender_male' else "Женский"
    user_id = callback_query.from_user.id
    update_user_data(user_id, gender=gender)
    user_states[user_id] = 'activity_level'
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Низкий (малоподвижный образ жизни)", callback_data="activity_low")],
        [InlineKeyboardButton(text="Средний (умеренная активность)", callback_data="activity_medium")],
        [InlineKeyboardButton(text="Высокий (высокая активность)", callback_data="activity_high")]
    ])
    await callback_query.message.answer("Выберите уровень активности:", reply_markup=keyboard)
 
@router.callback_query(lambda c: user_states.get(c.from_user.id) == 'activity_level' and c.data in ['activity_low', 'activity_medium', 'activity_high'])
async def handle_activity_level(callback_query: types.CallbackQuery):
    activity_level = {
        'activity_low': 'низкий',
        'activity_medium': 'средний',
        'activity_high': 'высокий'
    }[callback_query.data]
    
    user_id = callback_query.from_user.id
    update_user_data(user_id, activity_level=activity_level)
    del user_states[user_id]
    await callback_query.message.answer("Уровень активности обновлен.")
    await send_welcome(callback_query.message)
 
@router.callback_query(lambda c: c.data == 'get_recipe')
async def get_recipe(callback_query: types.CallbackQuery):
    meal = get_random_meal()
    if meal:
        meal_id, name, description, calories, url, avg_rating, rating_count = meal
        response = (
            f"<b>Рецепт:</b> {name}\n"
            f"<b>Описание:</b> {description}\n"
            f"<b>Калории:</b> {calories} ккал\n"
            f"<b>Ссылка:</b> {url}\n"
            f"<b>Средний рейтинг:</b> {avg_rating:.1f} ({rating_count} оценок)\n"
            "Оцените это блюдо:"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="1", callback_data=f"rate_{meal_id}_1")],
            [InlineKeyboardButton(text="2", callback_data=f"rate_{meal_id}_2")],
            [InlineKeyboardButton(text="3", callback_data=f"rate_{meal_id}_3")],
            [InlineKeyboardButton(text="4", callback_data=f"rate_{meal_id}_4")],
            [InlineKeyboardButton(text="5", callback_data=f"rate_{meal_id}_5")]
        ])
        await callback_query.message.answer(response, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback_query.message.answer("Не удалось найти рецепт.")

@router.callback_query(lambda c: c.data == 'healthy_foods')
async def healthy_foods(callback_query: types.CallbackQuery):
    food = get_random_healthy_food()
    if food:
        await callback_query.message.answer(f"<b>Полезный продукт:</b> {food[0]}\n<b>Описание:</b> {food[1]}", parse_mode="HTML")
    else:
        await callback_query.message.answer("Не удалось найти полезные продукты.")
 
@router.callback_query(lambda c: c.data == 'nutrition_tips')
async def nutrition_tips(callback_query: types.CallbackQuery):
    tip = get_random_nutrition_tip()
    if tip:
        await callback_query.message.answer(f"<b>Рекомендация по питанию:</b> {tip[0]}", parse_mode="HTML")
    else:
        await callback_query.message.answer("Не удалось найти рекомендации по питанию.")
 
@router.callback_query(lambda c: c.data == 'activity_tips')
async def activity_tips(callback_query: types.CallbackQuery):
    tip = get_random_activity_tip()
    if tip:
        await callback_query.message.answer(f"<b>Рекомендация по активности:</b> {tip[0]}", parse_mode="HTML")
    else:
        await callback_query.message.answer("Не удалось найти рекомендации по активности.")
 
@router.callback_query(lambda c: c.data == 'meal_plan')
async def meal_plan(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    exclude_ids = []
    meals = []

    for meal_type in ['breakfast', 'lunch', 'dinner', 'snacks']:
        meal = get_random_meal_by_type(exclude_ids)
        if meal:
            exclude_ids.append(meal[0])
            meals.append(meal)

    if len(meals) == 4:
        today_date = datetime.now().date()
        with sqlite3.connect(DATABASE) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO user_meal_plan (user_id, date, breakfast_id, lunch_id, dinner_id, snack_id)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, date) DO UPDATE SET
                breakfast_id = excluded.breakfast_id,
                lunch_id = excluded.lunch_id,
                dinner_id = excluded.dinner_id,
                snack_id = excluded.snack_id
            ''', (user_id, today_date, meals[0][0], meals[1][0], meals[2][0], meals[3][0]))
            connection.commit()
        
        response = (
            f"<b>Ваш план питания на день:</b>\n\n"
            f"<b>Завтрак:</b> {meals[0][1]} - {meals[0][2]} ({meals[0][3]} ккал)\n<b>Ссылка:</b> {meals[0][4]}\n<b>Средняя оценка:</b> {meals[0][5]:.2f}\n\n"
            f"<b>Обед:</b> {meals[1][1]} - {meals[1][2]} ({meals[1][3]} ккал)\n<b>Ссылка:</b> {meals[1][4]}\n<b>Средняя оценка:</b> {meals[1][5]:.2f}\n\n"
            f"<b>Ужин:</b> {meals[2][1]} - {meals[2][2]} ({meals[2][3]} ккал)\n<b>Ссылка:</b> {meals[2][4]}\n<b>Средняя оценка:</b> {meals[2][5]:.2f}\n\n"
            f"<b>Перекус:</b> {meals[3][1]} - {meals[3][2]} ({meals[3][3]} ккал)\n<b>Ссылка:</b> {meals[3][4]}\n<b>Средняя оценка:</b> {meals[3][5]:.2f}\n"
        )
        await callback_query.message.answer(response, parse_mode="HTML")
    else:
        await callback_query.message.answer("Не удалось найти план питания. Пожалуйста, попробуйте снова.")

def add_meal_rating(user_id, meal_id, rating):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO meal_ratings (user_id, meal_id, rating)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, meal_id) DO UPDATE SET
            rating = excluded.rating
        ''', (user_id, meal_id, rating))
        connection.commit()
 
@router.message(Command('rate_meal'))
async def rate_meal(message: types.Message):
    await message.answer("Введите ID блюда и вашу оценку (1-5) в формате: /rate_meal <ID> <оценка>")

@router.callback_query(lambda c: c.data.startswith('rate_'))
async def handle_rate(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    meal_id = int(data[1])
    rating = int(data[2])
    user_id = callback_query.from_user.id
    add_meal_rating(user_id, meal_id, rating)
    await callback_query.message.answer("Ваша оценка успешно сохранена!")

@router.message(lambda message: message.text.startswith('/rate_meal '))
async def handle_rate_meal(message: types.Message):
    try:
        _, meal_id, rating = message.text.split()
        meal_id = int(meal_id)
        rating = int(rating)
        if 1 <= rating <= 5:
            user_id = message.from_user.id
            add_meal_rating(user_id, meal_id, rating)
            await message.answer("Ваша оценка успешно сохранена!")
        else:
            await message.answer("Оценка должна быть числом от 1 до 5.")
    except ValueError:
        await message.answer("Неверный формат. Пожалуйста, используйте формат: /rate_meal <ID> <оценка>")

@router.message(Command('search_meals'))
async def search_meals(message: types.Message):
    await message.answer("Введите ключевое слово для поиска блюд:")

@router.message(lambda message: not message.text.startswith('/search_meals') and user_states.get(message.from_user.id) == 'search')
async def handle_search_meals(message: types.Message):
    keyword = message.text.strip()
    meals = search_meals_by_keyword(keyword)
    if meals:
        response = "\n\n".join([f"<b>{meal[0]}</b>\n{meal[1]}\nКалории: {meal[2]} ккал" for meal in meals])
        await message.answer(response, parse_mode="HTML")
    else:
        await message.answer("Не найдено ни одного блюда по вашему запросу.")
    del user_states[message.from_user.id]

def search_meals_by_keyword(keyword):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        query = "SELECT name, description, calories FROM meals WHERE name LIKE ? OR description LIKE ?"
        cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        return cursor.fetchall()

def register_handlers(router: Router):
    router.message.register(send_welcome, Command('start'))
    router.callback_query.register(my_data, lambda c: c.data == 'my_data')
    router.callback_query.register(fill_data, lambda c: c.data == 'fill_data')
    router.callback_query.register(set_parameters, lambda c: c.data in ['set_weight', 'set_height', 'set_age', 'set_gender', 'set_activity'])
    router.message.register(handle_weight, lambda message: message.text.isdigit() and user_states.get(message.from_user.id) == 'weight')
    router.message.register(handle_height, lambda message: message.text.isdigit() and user_states.get(message.from_user.id) == 'height')
    router.message.register(handle_age, lambda message: message.text.isdigit() and user_states.get(message.from_user.id) == 'age')
    router.callback_query.register(handle_gender, lambda c: c.data in ['gender_male', 'gender_female'] and user_states.get(c.from_user.id) == 'gender')
    router.callback_query.register(handle_activity_level, lambda c: c.data in ['activity_low', 'activity_medium', 'activity_high'] and user_states.get(c.from_user.id) == 'activity_level')
    router.callback_query.register(get_recipe, lambda c: c.data == 'get_recipe')
    router.callback_query.register(healthy_foods, lambda c: c.data == 'healthy_foods')
    router.callback_query.register(nutrition_tips, lambda c: c.data == 'nutrition_tips')
    router.callback_query.register(activity_tips, lambda c: c.data == 'activity_tips')
    router.callback_query.register(meal_plan, lambda c: c.data == 'meal_plan')
    router.message.register(search_meals, Command('search_meals'))
    router.message.register(handle_search_meals, lambda message: user_states.get(message.from_user.id) == 'search')
    router.message.register(rate_meal, Command('rate_meal'))
    router.message.register(handle_rate_meal, lambda message: message.text.startswith('/rate_meal '))

if __name__ == "__main__":
    reset_db()
    populate_db()
    register_handlers(router)
    dp.include_router(router)
    dp.run_polling(bot, skip_updates=True)