# from aiogram.filters.callback_data import CallbackData
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PreferenceCallback = CallbackData("preference", "ingredient")
ExcludeCallback = CallbackData("exclude", "ingredient")

def create_ingredient_keyboard(ingredients):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"Предпочитаю {ingredient}",
                callback_data=PreferenceCallback.new(ingredient=ingredient)
            ),
            InlineKeyboardButton(
                text=f"Исключить {ingredient}",
                callback_data=ExcludeCallback.new(ingredient=ingredient)
            )
        ]
        for ingredient in ingredients
    ])
    return keyboard
