from aiogram.dispatcher.filters.state import StatesGroup, State

class AddManager(StatesGroup):
    username = State()
    manager_id = State()
    city = State()
    department = State()