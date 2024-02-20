from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from random import choice, shuffle


def next_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Следующее')
    kb.button(text='Добавить новое слово')
    kb.button(text='Удалить слово')
    kb.button(text='Закончить')
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def next_keyboard_1() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Let's start!")
    kb.button(text='Добавить новое слово')
    kb.button(text='Удалить слово')
    kb.button(text='Закончить')
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Добавить новое слово',
            resize_keyboard=True,
            one_time_keyboadr=True
        ),
        KeyboardButton(
            text='Удалить слово'
        ),
        KeyboardButton(
            text="Let's start!"
        )
    ]
], resize_keyboard=True, one_time_keyboard=True)


def get_random_keyboard(words, translate):
    buttons = [
                KeyboardButton(
                    text=f'{choice(words)}'
                ),
                KeyboardButton(
                    text=f'{choice(words)}'
                ),
                KeyboardButton(
                    text=f'{choice(words)}'
                ),
                KeyboardButton(
                    text=f'{translate}'
                )
            ]
    shuffle(buttons)
    random_keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True, one_time_keyboard=True)
    return random_keyboard
