from aiogram import types
from aiogram.fsm.context import FSMContext
from keyboards.inline_keyboards import PreferenceCallback, ExcludeCallback

async def preference_callback_handler(callback_query: types.CallbackQuery, callback_data: PreferenceCallback, state: FSMContext):
    user_data = await state.get_data()
    preferences = user_data.get("preferences", [])
    preferences.append(callback_data.ingredient)
    await state.update_data(preferences=preferences)
    await callback_query.answer(f"{callback_data.ingredient} добавлен в предпочтения")

async def exclusion_callback_handler(callback_query: types.CallbackQuery, callback_data: ExcludeCallback, state: FSMContext):
    user_data = await state.get_data()
    exclusions = user_data.get("exclusions", [])
    exclusions.append(callback_data.ingredient)
    await state.update_data(exclusions=exclusions)
    await callback_query.answer(f"{callback_data.ingredient} добавлен в исключения")
