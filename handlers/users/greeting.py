import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from data.config import LEGO_PIC, LEGO_CAPTION, TERM_PIC, TERM_CAPTION
from keyboards.default.choice import choice
from states import StartState
from loader import dp, bot


@dp.message_handler(Command('start'))
async def start_handler(message: types.Message):
    user_name = message.from_user.full_name
    await message.reply(f'Привет! Меня зовут Наносокс бот, я могу называть тебя {user_name}? Если ты согласен, напиши \
"Да", если нет - напиши свое имя')
    await StartState.StateName.set()


@dp.message_handler(state=StartState.StateName)
async def name_handler(message: types.Message, state: FSMContext):
    mes = message.text
    chat_id = message.chat.id
    user_name = message.from_user.full_name if mes.lower() == 'да' else mes
    await message.answer(f'Рад познакомиться с тобой, {user_name}!')
    await message.answer('Моя компания называется "Нано-Носки Юник". \
Как ты мог догадаться, мы занимаемся производством Нано-Носков\nСейчас я покажу тебе, что у меня есть')
    await StartState.StateChoice.set()
    async with state.proxy() as data:
        data['user_name'] = user_name
    await asyncio.sleep(2)
    await message.answer('Смотри, у нас тут 2 вида новых носков, расхватывают очень быстро, так что, дружеский \
совет тебе - не медли.')
    await asyncio.sleep(2)
    await bot.send_photo(chat_id, LEGO_PIC, LEGO_CAPTION)
    await asyncio.sleep(5)
    await bot.send_photo(chat_id, TERM_PIC, TERM_CAPTION)
    await asyncio.sleep(10)
    await message.answer('Ну что, попробуешь и те, и другие? Или получится выбрать что-то одно? Нажми на кнопку ниже.',
                         reply_markup=choice)
    await asyncio.sleep(600)
    current_state = await state.get_state()
    if current_state == 'StartState:StateChoice':
        await message.answer('Я вижу, ты так и не смог выбрать... Давай я тебе помогу\n\
У тебя дома часто рассыпано лего?', reply_markup=ReplyKeyboardRemove())
        await StartState.NoAnswer1.set()
