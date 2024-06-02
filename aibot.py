import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat
from setting.settings import TOKEN, GIGACHAT_CREDENTIALS
import httpx

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем HTTP-клиент с увеличенным тайм-аутом
http_client = httpx.Client(timeout=httpx.Timeout(30.0))

# Обертка для GigaChat, использующая наш HTTP-клиент
class CustomGigaChat(GigaChat):
    def __init__(self, credentials, client, **kwargs):
        super().__init__(credentials=credentials, **kwargs)
        self.client = client

    def _generate(self, **kwargs):
        return self.client.post("https://api.gigachat.com/generate", json=kwargs)

# Авторизация в сервисе GigaChat
chat = CustomGigaChat(credentials=GIGACHAT_CREDENTIALS, client=http_client, verify_ssl_certs=False)

# Сообщения для GigaChat
messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот на основе GigaChat. Как я могу помочь вам сегодня?")

# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: Message):
    await message.reply("Я могу ответить на следующие команды:\n/start - Начать общение\n/help - Помощь")

# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    user_input = message.text
    messages.append(HumanMessage(content=user_input))
    res = chat(messages)
    messages.append(res)
    await message.reply(res.content)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
