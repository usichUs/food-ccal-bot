import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from setting.settings import TOKEN
from data.text_data import recipes, healthy_foods, nutrition_tips, activity_tips, bmi_advice

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить рецепт", callback_data="get_recipe")],
        [InlineKeyboardButton(text="Полезные продукты", callback_data="get_healthy_food")],
        [InlineKeyboardButton(text="Рекомендации по питанию", callback_data="get_nutrition_tips")],
        [InlineKeyboardButton(text="Рассчитать ИМТ", callback_data="calculate_bmi")],
        [InlineKeyboardButton(text="Рекомендации по активности", callback_data="get_activity_tips")]
    ])
    await message.answer("Привет! Я бот для помощи с питанием. Выберите действие:", reply_markup=keyboard)

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

@dp.callback_query(F.data == "calculate_bmi")
async def request_bmi_info(callback: types.CallbackQuery):
    await callback.message.answer("Введите ваши данные в формате: вес(кг) рост(см)")
    await callback.answer()

@dp.callback_query(F.data == "get_activity_tips")
async def send_activity_tips(callback: types.CallbackQuery):
    tip = random.choice(activity_tips)
    await callback.message.answer(f"Рекомендация по физической активности: {tip}")
    await callback.answer()

# Обработчик текстовых сообщений для расчета ИМТ и выдачи советов
@dp.message(F.text.regexp(r'^\d+(\.\d+)? \d+$'))
async def calculate_bmi(message: types.Message):
    try:
        data = message.text.split()
        weight = float(data[0])
        height = float(data[1]) / 100  # Переводим рост в метры
        bmi = weight / (height ** 2)
        
        if bmi < 18.5:
            advice = bmi_advice['underweight']
        elif 18.5 <= bmi < 25:
            advice = bmi_advice['normal']
        elif 25 <= bmi < 30:
            advice = bmi_advice['overweight']
        else:
            advice = bmi_advice['obesity']

        await message.reply(f"Ваш ИМТ: {bmi:.2f}\n{advice}")
    except (ValueError, IndexError):
        await message.reply("Неверный формат данных. Пожалуйста, введите в формате: вес(кг) рост(см)")

# Дополнительная функция: советы по питанию
@dp.message(Command('advice'))
async def send_advice(message: types.Message):
    advice = random.choice(nutrition_tips)
    await message.answer(f"Совет по питанию: {advice}")

# Дополнительная функция: информация о полезных продуктах
@dp.message(Command('healthy_food'))
async def send_healthy_food_info(message: types.Message):
    food = random.choice(healthy_foods)
    await message.answer(f"Полезный продукт: {food}")

# Дополнительная функция: рекомендации по физической активности
@dp.message(Command('activity'))
async def send_activity(message: types.Message):
    activity = random.choice(activity_tips)
    await message.answer(f"Рекомендация по физической активности: {activity}")

# Установка команд бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/advice", description="Получить совет по питанию"),
        BotCommand(command="/bmi", description="Рассчитать ИМТ"),
        BotCommand(command="/healthy_food", description="Информация о полезных продуктах"),
        BotCommand(command="/activity", description="Рекомендации по физической активности")
    ]
    await bot.set_my_commands(commands)

# Запуск бота
if __name__ == '__main__':
    dp.startup.register(set_commands)
    dp.run_polling(bot)
