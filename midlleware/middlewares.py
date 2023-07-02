from typing import Any, Tuple
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types, Dispatcher
from data_base import base
# from typing import


class StartBot(BaseMiddleware):
    # async def on_pre_process_update(self, update: types.Update, dict: dict):
    #      pass

    async def on_process_update(self, update: types.Update, dict: dict):
            await base.save_user_to_db(update.message)


def register_middleware(dp: Dispatcher):
    dp.middleware.setup(StartBot())