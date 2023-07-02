from aiogram import executor
from create_bot import dp
from handlers import client
from utils.functions import on_startup
from midlleware import middlewares


middlewares.register_middleware(dp)
client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)