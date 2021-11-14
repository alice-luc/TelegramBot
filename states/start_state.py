from aiogram.dispatcher.filters.state import StatesGroup, State


class StartState(StatesGroup):

    StateName = State()
    StateChoice = State()
    StateEmail = State()
    StatePhone = State()
    NoAnswer = State()
    NoAnswer1 = State()
    Answer = State()
