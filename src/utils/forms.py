from aiogram.fsm.state import StatesGroup, State


class CreateTaskFSBForm(StatesGroup):
    name = State()
    description = State()
    term = State()
    executor = State()