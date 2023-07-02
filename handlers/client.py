from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from create_bot import bot
from data_base import base
from stocks.shariah_filter import shariah_filter
from utils.generate_msg import shariah_filter_message, client_info_message
import config


# start command
async def start_command(message: types.Message):
    await message.answer(text=config.start_text, parse_mode=types.ParseMode.HTML)


# # help command
async def help_command(message: types.Message):
    await message.answer(text=config.help_msg)


# Send message to all users bot is offline
async def send_msg_offline(message: types.Message):
    # if config.admin_id == message.from_user.id:
        # users_chat_id = await get_users_chat_id()
        # if users_chat_id:
        #     for chat_id in users_chat_id:
        #         try:
        #             await bot.send_message(chat_id=chat_id, text='Бот в онлайне!')
        #         except:
        #             continue
    pass

# Inline Handler
# async def inline_handler(query: InlineQuery):
#     # search_info = await main_search(query, inline_search=True) or 'aapl'

#     text = query.query or 'echo'
#     input_content = InputTextMessageContent(text)
#     result_id: str = hashlib.md5(text.encode()).hexdigest()

#     article = InlineQueryResultArticle(
#         input_message_content=text,
#         id=result_id,
#         title='Тикер'
#     )

#     # await bot.answer_inline_query(inline_query_id=query.id, results=[article], cache_time=3)
#     await query.answer(results=[article], cache_time=1, is_personal=True)


# Parsing info
async def all_msg_handler(message: types.Message):
    await message.answer(
        text=f'Проверяем ваш запрос <b>{message.text.upper()}</b>\nПодождите...\nПока все данные в тестовом режиме некоторые даннае может не совпадать',
        parse_mode=types.ParseMode.HTML)

    msg_to_admin = await client_info_message(message)
    await bot.send_message(chat_id='649984893', text=msg_to_admin, parse_mode=types.ParseMode.HTML)

    data = await shariah_filter(message.text)

    msg_stock_info = await shariah_filter_message(data, message.text)
    await message.reply(text=msg_stock_info, parse_mode=types.ParseMode.HTML)
    await base.save_search_info_to_db(message, data)


# register handlers
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_command, CommandStart())
    dp.register_message_handler(help_command, CommandHelp())
    dp.register_message_handler(send_msg_offline, commands='off')
    # dp.register_inline_handler(inline_handler)
    dp.register_message_handler(all_msg_handler)