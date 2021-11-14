from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Терморегулирующие'),
            KeyboardButton(text='Анти-Лего')
        ],
        [
            KeyboardButton(text='Возьму все'),
            KeyboardButton(text='Еще подумаю')
        ]
    ],
    resize_keyboard=True
)
