import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import config


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)