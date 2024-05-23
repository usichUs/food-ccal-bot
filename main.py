from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from setting.settings import TOKEN
from handlers.commands import (
    set_main_menu,
    process_start_command,
    process_help_command,
    process_ingredient_preferences,
    preference_callback_handler,
    exclusion_callback_handler,
    process_filtered_dishes_command,
    process_menu_command_wrapper,
    process_invalid_command
)
from states.user_states import FilterState
from keyboards.inline_keyboards import PreferenceCallback, ExcludeCallback

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.startup.register(set_main_menu)

dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(process_ingredient_preferences, Command(commands=["filter_dishes"]))
dp.message.register(process_filtered_dishes_command, Command(commands=["show_filtered_dishes"]))
dp.message.register(process_menu_command_wrapper, Command(commands=["menu"]))
dp.message.register(process_menu_command_wrapper, F.text == "Получить меню на день")
dp.message.register(process_help_command, F.text =="Помощь")
dp.callback_query.register(preference_callback_handler, PreferenceCallback.filter())
dp.callback_query.register(exclusion_callback_handler, ExcludeCallback.filter())
dp.message.register(process_invalid_command)

if __name__ == '__main__':
    dp.run_polling(bot)
