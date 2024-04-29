from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import json

import requests
import time

from setting.settings import TOKEN
from functions.format_recipe_message import format_recipe_message
from functions.format_recipe_message import get_time_by_type

bot = Bot(token=TOKEN)
dp = Dispatcher()

button_menu = KeyboardButton(text="Получить меню на день", callback_data="menu")
button_help = KeyboardButton(text="Помощь", callback_data="help")

keyboard = ReplyKeyboardMarkup(keyboard=[[button_menu, button_help]])

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
    await message.answer("Привет! Я бот для получения рецептов. Напиши /help, чтобы узнать, что я умею.", reply_markup=keyboard)

async def process_help_command(message: Message):
    await message.answer("I don't have help :(")

dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(process_menu_command_wrapper, Command(commands=["menu"]))
dp.message.register(process_menu_command_wrapper, F.text == "Получить меню на день")
dp.message.register(process_help_command, F.text == "Помощь")
dp.callback_query.register(process_menu_command_wrapper, F.data == "menu")
dp.callback_query.register(process_help_command, F.data == "help")

if __name__ == '__main__':
    dp.run_polling(bot)

