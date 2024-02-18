from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_WORD = State()
    GET_WORD_DEL = State()
    GET_TRANSLATE = State()