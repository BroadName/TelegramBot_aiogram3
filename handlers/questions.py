from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from db_connect import Request
from keyboards import reply_keyboard, next_keyboard, next_keyboard_1, get_random_keyboard
from aiogram.fsm.context import FSMContext
from statesform import StepsForm
from random import choice
router = Router()

rus = {'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж',
           'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', 'ё'}

eng = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c',
           'v', 'b', 'n', 'm'}

start_words = {'i': 'я', 'she': 'она', 'he': 'он', 'they': 'они', 'we': 'мы', 'red': 'красный', 'black': 'черный',
               'yellow': 'желтый', 'blue': 'синий', 'green': 'зеленый'}


@router.message(Command('start'))
async def cmd_start(message: Message, request: Request):
    await request.add_user(message.from_user.id, message.from_user.first_name)
    if not (await request.check_user(message.from_user.id))[0].get('status'):
        await request.change_status(1, message.from_user.id)
        for i in start_words.items():
            await request.add_word(message.from_user.id, i[0], i[1])
    await message.answer(
        f'{message.from_user.first_name} давай начнём учиться!',
        reply_markup=reply_keyboard
    )


@router.message(F.text)
async def check_add(message: Message, state: FSMContext):
    await message.answer('Введите новое слово и его перевод через пробел',
                         reply_murkup=ReplyKeyboardRemove())
    await state.set_state(StepsForm.GET_WORD)


@router.message(F.text)
async def check_to_del(message: Message, state: FSMContext):
    await message.answer('Введите слово, которое хотели бы удалить',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(StepsForm.GET_WORD_DEL)


@router.message(F.text)
async def delete_word(message: Message, request: Request, state: FSMContext):
    if len(message.text.split()) == 1 and message.text[0].lower() in eng:
        await request.delete_word(message.from_user.id, message.text.lower())
        await message.answer(f'{message.text} удалено',
                             reply_markup=reply_keyboard)
        await state.clear()
    else:
        await message.answer('Вы ввели неверные данные. Введите одно слово на английском языке, которое нужно удалить!'
                             'Либо введите команду /start для выбора действий',
                             reply_markup=reply_keyboard)


@router.message(F.text)
async def add_new_word(message: Message, request: Request, state: FSMContext):
    if len(message.text.split()) == 2 and message.text.split()[0][0].lower() in eng\
            and message.text.split()[1][0].lower() in rus:
        await request.add_word(message.from_user.id, message.text.split()[0].lower(), message.text.split()[1].lower())
        await message.answer('Well done!', reply_markup=next_keyboard_1())
        await state.clear()
    else:
        await message.answer('Вы ввели неправильные данные. Введите английское слово а потом его перевод через пробел.'
                             'Либо введите команду /start для выбора действий', reply_markup=reply_keyboard)


@router.message(F.text)
async def lets_start(message: Message, request: Request, state: FSMContext):
    word = choice(await request.lets_start(message.from_user.id)).get("english")
    descriptions = await request.get_description(message.from_user.id)
    translate = (await request.get_translate(word))[0].get('translate')
    await message.answer(f'Выберите правильный вариант перевода для слова {word}',
                         reply_markup=get_random_keyboard(descriptions, translate))
    await state.set_state(StepsForm.GET_TRANSLATE)
    await state.update_data(right_word=translate, words=descriptions)


@router.message(F.text)
async def try_translate(message: Message, state: FSMContext):
    right_word = (await state.get_data()).get('right_word')
    words = (await state.get_data()).get('words')
    if message.text.lower() == right_word:
        await message.answer(f'Вы совершенно правы! Это {right_word}',
                             reply_markup=next_keyboard())
        await state.clear()
    else:
        await message.answer('Ответ неверный, попробуйте ещё раз. \n'
                             'Либо вызовите меню для выбора действий с помощью команды /start',
                             reply_markup=get_random_keyboard(words, right_word))


@router.message(F.text)
async def last_word(message: Message):
    await message.answer(f'{message.from_user.first_name} возвращайся скорее!')
