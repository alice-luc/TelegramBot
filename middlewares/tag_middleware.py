from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
#
# import logging
#
#
# class TagMiddleware(BaseMiddleware):
#
#     async def on_pre_process_update(self, update: types.Update, data: dict):
#         logging.info('- - - - - - - PRE-PROCESS UPDATE - - - - - - - ')
#         message = update.message.text if update.message.text else update.message.caption
#         if message.__contains__('<'):
#             raise CancelHandler()
