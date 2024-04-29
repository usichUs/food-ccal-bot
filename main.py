from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
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

keyboard = ReplyKeyboardMarkup(keyboard=[[button_menu, button_help]], resize_keyboard=True)

async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),#Доделать потом
        BotCommand(command='/contacts',
                   description='Другие способы связи'),#Доделать потом
        BotCommand(command='/menu',
                   description='Питание на День'),
        BotCommand(command='/start',
                   description='Перезапуск бота'),
    ]

    await bot.set_my_commands(main_menu_commands)

async def process_menu_command(message: Message):
    # Читаем данные из файла JSON
    with open('receipts/receipts.json', 'r', encoding='utf-8') as file:
        recipes = json.load(file)
    
    # Формируем и отправляем сообщение о завтраке
    breakfast_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Breakfast')
    await message.answer(format_recipe_message(breakfast_recipe), parse_mode='HTML')
    
    # Формируем и отправляем сообщение о обеде
    lunch_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Lunch')
    await message.answer(format_recipe_message(lunch_recipe), parse_mode='HTML')
    
    # Формируем и отправляем сообщение о ужине
    dinner_recipe = next(recipe for recipe in recipes if recipe['type'] == 'Dinner')
    await message.answer(format_recipe_message(dinner_recipe), parse_mode='HTML')

async def process_menu_command_wrapper(message: Message):
    await process_menu_command(message)

async def process_start_command(message: Message):
    await message.answer("Привет! Я бот для получения рецептов. Напиши /help, чтобы узнать, что я умею.", reply_markup=keyboard)

async def process_help_command(message: Message):
    await message.answer("I don't have help :(")

async def process_invalid_command(message: Message):
    await message.answer("Такой команды нет :(")

dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(process_menu_command_wrapper, Command(commands=["menu"]))
dp.message.register(process_menu_command_wrapper, F.text == "Получить меню на день")
dp.message.register(process_help_command, F.text == "Помощь")
dp.callback_query.register(process_menu_command_wrapper, F.data == "menu")
dp.callback_query.register(process_help_command, F.data == "help")
dp.startup.register(set_main_menu)
dp.message.register(process_invalid_command)

if __name__ == '__main__':
    dp.run_polling(bot)

