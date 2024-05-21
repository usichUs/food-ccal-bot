from aiogram.fsm.state import StatesGroup, State

class FilterState(StatesGroup):
    EnterPreferences = State()
    EnterExclusions = State()
