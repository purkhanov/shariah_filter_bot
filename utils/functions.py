from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from create_bot import bot
from data_base.base import get_users_chat_id


async def on_startup(_):
    print('Bot is online')
    await set_commands(bot)
    # await send_msg_online()


# Send message to all users
async def send_msg_online():
    pass
    users_chat_id = await get_users_chat_id()

    if users_chat_id:
        for chat_id in users_chat_id:
            try:
                await bot.send_message(chat_id=chat_id, text='Бот в онлайне!')
            except:
                continue


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command = 'start',
            description = 'Начало работы'
        ),
        BotCommand(
            command = 'help',
            description = 'Помощь'
        ),
        BotCommand(
            command = 'info',
            description = 'Информация'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())