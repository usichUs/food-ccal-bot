from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
import json

import requests
import time

from setting.settings import TOKEN
from functions.format_recipe_message import format_recipe_message
from functions.format_recipe_message import get_time_by_type

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def process_menu_command(message: Message):
    # Читаем данные из файла JSON
    with open('receipts/receipts.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)
    
    # Формируем и отправляем сообщение о завтраке
    breakfast_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Breakfast')
    await message.answer(format_recipe_message(breakfast_recipe))
    
    # Формируем и отправляем сообщение о обеде
    lunch_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Lunch')
    await message.answer(format_recipe_message(lunch_recipe))
    
    # Формируем и отправляем сообщение о ужине
    dinner_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Dinner')
    await message.answer(format_recipe_message(dinner_recipe))

async def process_menu_command_wrapper(message: Message):
    await process_menu_command(message)

async def process_start_command(message: Message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Получить меню на день", callback_data="get_menu")
    keyboard.add(button)
    await message.answer("Нажмите кнопку, чтобы получить меню на день.", reply_markup=keyboard)

async def process_help_command(message: Message):
    await message.answer("I don't have help :(")

async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy')

dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(process_menu_command_wrapper, Command(commands=["menu"]))
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)

