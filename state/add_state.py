from aiogram.dispatcher.filters.state import StatesGroup, State

class AddManager(StatesGroup):
    username = State()
    city = State()
    department = State()