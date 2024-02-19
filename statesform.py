from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    GET_ENG_WORD = State()
    GET_RUS_WORD = State()
    GET_WORD_DEL = State()
    GET_TRANSLATE = State()
