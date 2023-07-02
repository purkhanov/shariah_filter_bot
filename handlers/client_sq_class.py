from aiogram import types, Dispatcher
from create_bot import bot
from stocks.shariah_filter import check_stock
from utils.generate_msg import shariah_filter_message, client_info_message
from data_base.sq_lite import DataBase
import config


# start command
async def start_command(message: types.Message):
    await message.answer(text=config.start_text)


# # help command
async def help_command(message: types.Message):
    await message.answer(text=config.help_msg)


# Bot is online
async def on_startup_bot():
    db = DataBase()
    users = db.get_all_users()

    if users:
        for user in users:
            user = dict(user)
            print(user)
            # await bot.send_message(chat_id=user['tg_chat_id'], text='Бот в онлайне!')


# Bot is offline
async def bot_is_offline(message: types.Message):
    if config.admin_id == message.from_user.id:
        db = DataBase()

        users = db.get_all_users()

        for user in users:
            user = dict(user)
            await bot.send_message(chat_id=user['tg_chat_id'], text='Бот отключен!')


# Parsing info
async def all_msg_handler(message: types.Message):
    await message.answer(text=f'Проверяем ваш запрос {message.text}\nПодождите...\nПока все данные в тестовом режиме некоторые даннае может не совпадать')


    msg_to_admin = await client_info_message(message)
    await bot.send_message(chat_id='649984893', text=msg_to_admin, parse_mode=types.ParseMode.HTML)

    data = await check_stock(message.text)
    db = DataBase()
    db.save_user_to_db(message, data)
    db.save_search_info_to_db(message, data)

    msg_stock_info = await shariah_filter_message(data, message.text)
    await message.reply(text=msg_stock_info, parse_mode=types.ParseMode.HTML)


# register handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, commands='start')
    dp.register_message_handler(help_command, commands='help')
    dp.register_message_handler(bot_is_offline, commands='off')
    dp.register_message_handler(all_msg_handler)