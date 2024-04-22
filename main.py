from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

import requests
import time

from setting.settings import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def process_start_command(message: Message):
    await message.answer("Hi!\nI'm EchoBot!\nPowered by aiogram and UsichUs!\nWrite me smth.")

async def process_help_command(message: Message):
    await message.answer("I don't have help :(")

async def send_echo_photo(message: Message):
    await message.answer_photo(message.photo[0].file_id)

async def send_echo(message: Message):
    await message.answer(text=message.text)

dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(send_echo_photo, F.photo)
dp.message.register(send_echo)

if __name__ == '__main__':
    dp.run_polling(bot)