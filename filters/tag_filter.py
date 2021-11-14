import logging

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data


class TagFilter(BoundFilter):

    async def check(self, message: types.Message):
        data = ctx_data.get(message)
        logging.info(data)