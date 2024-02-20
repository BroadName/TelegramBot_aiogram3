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
            'v', 'b', 'n', 'm', "'"}

start_words = {'i': 'я', 'she': 'она', 'he': 'он', 'they': 'они', 'we': 'мы', 'red': 'красный', 'black': 'черный',
               'yellow': 'желтый', 'blue': 'синий', 'green': 'зеленый'}


@router.message(Command('start'))
async def cmd_start(message: Message, request: Request):
    await request.add_user(message.from_user.id, message.from_user.first_name)
    await message.answer(
        f'{message.from_user.first_name} давай начнём учиться!',
        reply_markup=reply_keyboard
    )


@router.message(F.text)
async def check_add(message: Message, state: FSMContext):
    await message.answer('Введите новое слово(выражение) на английском языке',
                         reply_murkup=ReplyKeyboardRemove())
    await state.set_state(StepsForm.GET_ENG_WORD)


@router.message(F.text)
async def check_to_del(message: Message, state: FSMContext):
    await message.answer('Введите слово, которое хотели бы удалить',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(StepsForm.GET_WORD_DEL)


@router.message(F.text)
async def delete_word(message: Message, request: Request, state: FSMContext):
    check = message.text.lower().replace(' ', '')
    if (set(check) - eng) == set():
        await request.delete_word(message.text.lower())
        await message.answer(f'{message.text} удалено',
                             reply_markup=reply_keyboard)
        await state.clear()
    else:
        await message.answer('Вы ввели неверные данные. Введите одно слово на английском языке, которое нужно удалить!'
                             'Либо введите команду /start для выбора действий',
                             reply_markup=reply_keyboard)


@router.message(F.text)
async def get_eng_word(message: Message, state: FSMContext, request: Request):
    check = message.text.lower().replace(' ', '')
    if (set(check) - eng) == set():
        if await request.check_add_word(message.text.lower(), message.from_user.id) == []:
            await message.answer('Введите его перевод, или определение')
            await state.update_data(eng_word=message.text)
            await state.set_state(StepsForm.GET_RUS_WORD)
        else:
            await message.answer('Вы уже добавляли это слово.\n'
                                 'Введите другое или выберите другое действие', reply_markup=reply_keyboard)
    else:
        await message.answer('Вы ввели неверные данные!\nСлово(выражение) должны быть на английском языке,\n'
                             'из знаков доступен только апостроф!', reply_markup=next_keyboard_1())


@router.message(F.text)
async def add_new_word(message: Message, request: Request, state: FSMContext):
    check = message.text.lower().replace(' ', '')
    eng_word = (await state.get_data()).get('eng_word').lower()
    if (set(check) - rus) == set():
        await request.add_word(message.from_user.id, eng_word, message.text)
        await message.answer('Well done!', reply_markup=next_keyboard_1())
        await state.clear()
    else:
        await message.answer('Вы ввели неправильные данные.\n '
                             'Введите перевод, используя только буквы русского алфавита.\n'
                             'Либо введите команду /start для выбора действий', reply_markup=reply_keyboard)

    await state.clear()


@router.message(F.text)
async def lets_start(message: Message, request: Request, state: FSMContext):
    check = await request.check_words(message.from_user.id)
    if check:
        word = choice(await request.lets_start(message.from_user.id)).get("english")
        descriptions = await request.get_description(message.from_user.id)
        translate = (await request.get_translate(word))[0].get('translate')
        from_db = [i.get('translate') for i in descriptions if i.get('translate') != translate] +\
                  [v for k, v in start_words.items() if v != translate]
        all_words = list(set(from_db))
        await message.answer(f'Выберите правильный вариант перевода для слова {word}',
                             reply_markup=get_random_keyboard(all_words, translate))
        await state.set_state(StepsForm.GET_TRANSLATE)
        await state.update_data(right_word=translate, words=all_words)
    else:
        await message.answer('В вашей базе ещё нет слов, добавьте хотя бы одно слово!',
                             reply_markup=reply_keyboard)
        await state.clear()


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
