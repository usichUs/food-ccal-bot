import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from setting.settings import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Примерный список рецептов
recipes = [
    "Салат Цезарь: курица, салат, сыр, соус Цезарь",
    "Борщ: свекла, капуста, картофель, морковь, лук",
    "Паста Болоньезе: макароны, фарш, томаты, лук, чеснок",
    # Добавьте другие рецепты по вашему желанию
]

# Функция для расчета суточной потребности в калориях
def calculate_calories(weight, height, age, gender):
    if gender == 'male':
        return 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        return 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить рецепт", callback_data="get_recipe")],
        [InlineKeyboardButton(text="Рассчитать калории", callback_data="calculate_calories")]
    ])
    await message.answer("Привет! Я бот для помощи с питанием. Выберите действие:", reply_markup=keyboard)

# Обработчик нажатий кнопок
@dp.callback_query(F.data == "get_recipe")
async def send_random_recipe(callback: types.CallbackQuery):
    recipe = random.choice(recipes)
    await callback.message.answer(f"Ваш случайный рецепт: {recipe}")
    await callback.answer()

@dp.callback_query(F.data == "calculate_calories")
async def request_calories_info(callback: types.CallbackQuery):
    await callback.message.answer("Введите данные в формате: вес(кг) рост(см) возраст пол(м/ж)")
    await callback.answer()

# Обработчик текстовых сообщений для расчета калорий
@dp.message(F.text.regexp(r'^\d+(\.\d+)? \d+(\.\d+)? \d+ [мжМЖ]$'))
async def handle_message(message: types.Message):
    try:
        data = message.text.split()
        weight = float(data[0])
        height = float(data[1])
        age = int(data[2])
        gender = data[3].lower()
        
        if gender not in ('м', 'ж'):
            await message.reply("Пол должен быть 'м' или 'ж'")
            return
        
        gender = 'male' if gender == 'м' else 'female'
        calories = calculate_calories(weight, height, age, gender)
        await message.reply(f"Ваша суточная потребность в калориях: {calories:.2f} калорий.")
    except (ValueError, IndexError):
        await message.reply("Неверный формат данных. Пожалуйста, введите в формате: вес(кг) рост(см) возраст пол(м/ж)")

# Дополнительная функция: советы по питанию
@dp.message(Command('advice'))
async def send_advice(message: types.Message):
    advices = [
        "Пейте больше воды.",
        "Ешьте больше овощей и фруктов.",
        "Избегайте переработанных продуктов.",
        "Сократите потребление сахара.",
        "Употребляйте белок в каждом приеме пищи."
    ]
    advice = random.choice(advices)
    await message.answer(f"Совет по питанию: {advice}")

# Дополнительная функция: проверка ИМТ
@dp.message(Command('bmi'))
async def request_bmi_info(message: types.Message):
    await message.answer("Введите ваши данные в формате: вес(кг) рост(см)")

@dp.message(F.text.regexp(r'^\d+(\.\d+)? \d+$'))
async def calculate_bmi(message: types.Message):
    try:
        data = message.text.split()
        weight = float(data[0])
        height = float(data[1]) / 100  # Переводим рост в метры
        bmi = weight / (height ** 2)
        await message.reply(f"Ваш ИМТ: {bmi:.2f}")
    except (ValueError, IndexError):
        await message.reply("Неверный формат данных. Пожалуйста, введите в формате: вес(кг) рост(см)")

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)
