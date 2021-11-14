import asyncio
import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import secure_rand
from states import StartState
from loader import dp, bot


@dp.message_handler(state=StartState.StateEmail)
async def email_collecting(message: types.Message, state: FSMContext):
    email = message.text
    if re.match(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+', email):
        await StartState.StatePhone.set()
        await message.answer('Принято! Теперь жду твой номер телефона')
        async with state.proxy() as data:
            data['email'] = email
    else:
        await message.answer('Попробуй еще раз, мне кажется, ты ввел неверный email')

    await asyncio.sleep(900)
    current_state = await state.get_state()
    if current_state == 'StartState:StateEmail':
        socks_name = await state.get_data('socks_name')
        await message.answer(f'Дружище, я говорил, что их быстро разбирают?\
Кажется, было такое... Так вот, за 15 минут купили уже 5 пар. Я не могу отправить операторам заказ без твоего номера\
телефона. Твои {socks_name} Нано-Носки ждут тебя!')


@dp.message_handler(state=StartState.StatePhone)
async def phone_number_collecting(message: types.Message, state: FSMContext):
    if re.match(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", message.text):
        chat_id = message.chat.id
        phone_number = message.text
        state_data = await state.get_data()
        await message.answer(f'Все готово! Наши менеджеры свяжутся с тобой по номеру {phone_number} в течение \
5 минут. Твой заказ: {state_data["socks_name"]} Нано-Носки')
        if state_data['multi']:
            for i in state_data['user_choice']:
                await bot.send_photo(chat_id, i, caption='1 шт')
        else:
            await bot.send_photo(chat_id, state_data['user_choice'], caption='1 шт')
        await asyncio.sleep(2)
        await message.answer(f'Спасибо за заказ! Если захочешь заказать для кого-то из друзей - вот тебе промокод \
на следующую покупку, {secure_rand(10)}. Назови его нашему оператору и получишь скидку 5%')
        await state.finish()
    else:
        await message.answer('Попробуй еще раз, мне кажется, ты ввел неверный номер телефона')
    await asyncio.sleep(900)
    current_state = await state.get_state()
    if current_state == 'StartState:StatePhone':
        socks_name = await state.get_data('socks_name')
        await message.answer(f'Твои {socks_name} Нано-Носки ждут тебя! Тебе осталось только написать номер телефона')


