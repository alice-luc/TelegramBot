import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import ReplyKeyboardRemove

from data.config import LEGO_PIC, TERM_PIC, secure_rand
from states import StartState
from loader import dp


@dp.message_handler(lambda message: ['терморегулирующие', 'анти-лего', 'возьму все'].__contains__(message.text.lower()),
                    state="*")
async def choice_handler(message: types.Message, state: FSMContext):

    await message.answer(f'Отлично! Напиши свою почту и номер телефона, и наш менеджер свяжется с тобой',
                         reply_markup=ReplyKeyboardRemove())
    user_choice = message.text.lower()

    if user_choice == 'терморегулирующие':
        async with state.proxy() as data:
            data['multi'] = False
            data['socks_name'] = 'Терморегулирующие'
            data['user_choice'] = TERM_PIC
    elif user_choice == 'анти-лего':
        async with state.proxy() as data:
            data['multi'] = False
            data['socks_name'] = 'Анти-Лего'
            data['user_choice'] = LEGO_PIC
    else:
        async with state.proxy() as data:
            data['multi'] = True
            data['socks_name'] = 'Терморегулирующие и Анти-Лего'
            data['user_choice'] = [TERM_PIC, LEGO_PIC]
    await message.answer('Сначала напиши свой email')
    await StartState.StateEmail.set()


@dp.message_handler(Text(equals='Еще подумаю'), state=StartState.StateChoice)
async def choice_handler_wait(message: types.Message, state: FSMContext):
    await StartState.NoAnswer.set()
    await message.answer('Это очень ответственный выбор, я понимаю...')
    await asyncio.sleep(600)
    current_state = await state.get_state()
    if current_state == 'StartState:NoAnswer':
        await message.answer('Я вижу, ты так и не смог выбрать... Давай я тебе помогу\n\
У тебя дома часто рассыпано лего?', reply_markup=ReplyKeyboardRemove())
        await StartState.NoAnswer1.set()


@dp.message_handler(state=StartState.NoAnswer1)
async def answer_quiz_handler(message: types.Message, state: FSMContext):

    if not message.text:
        await message.answer('Кажется, я не могу прочитать твое сообщение, нажми на подходящую кнопку внизу')
        raise CancelHandler()
    if message.text.lower() == 'да':
        answer = 'Анти-Лего'
        async with state.proxy() as data:
            data['multi'] = False
            data['socks_name'] = answer
            data['user_choice'] = LEGO_PIC
    else:
        answer = 'Терморегулирующие'
        async with state.proxy() as data:
            data['multi'] = False
            data['socks_name'] = answer
            data['user_choice'] = TERM_PIC
    await message.answer(f'Тогда вот тебе загадка, отгадаешь ее и я дам тебе 5% скидку на {answer} нано-носки')
    await asyncio.sleep(1)
    await message.answer('Наполовину полный стакан стоял на краю стола так, что его большая часть была на весу. Через \
час стакан упал и разбился. Что было внутри стакана?')
    await StartState.Answer.set()


@dp.message_handler(state=StartState.Answer)
async def choice_handler(message: types.Message, state: FSMContext):

    if not message.text:
        await message.answer('Кажется, я не могу прочитать твое сообщение, нажми на подходящую кнопку внизу')
        raise CancelHandler()
    answer = message.text.lower()
    if ['лед', 'лёд'].__contains__(answer):
        await message.answer(f'Молодец, однако.\
Всего 43% людей дало правильный ответ. Вот тебе скидка! {secure_rand(10)} \
Напиши свою почту и номер телефона, и мы свяжемся с тобой\
Скажи промокод нашему менеджеру и получишь скидку 5%')
        await message.answer('Сначала напиши свой email')
        async with state.proxy() as data:
            data['has_discount'] = True
        await StartState.StateEmail.set()
        await asyncio.sleep(600)
        current_state = await state.get_state()
        if current_state == 'StartState:StateEmail':
            await message.answer('')
    elif ['нет', 'не знаю', 'сдаюсь'].__contains__(answer):
        await message.answer('Подсказка: \nПрошёл час... Подумай, что может изменить свое состояние за час?')
    else:
        await message.answer('Попробуй еще разок, напиши "сдаюсь", чтобы получить подсказку')
