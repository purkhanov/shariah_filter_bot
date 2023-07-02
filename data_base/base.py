from aiogram.types import Message, Update
from sqlalchemy import select, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from data_base.models import Users, SearchInfo, user_tag


engine = create_async_engine('sqlite+aiosqlite:///shariah_filter_2.db', echo = True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)


async def get_users_chat_id():
    async with async_session() as session:
        users_chat_id = await session.execute(select(Users.tg_chat_id))

        return users_chat_id.scalars()


async def get_user(tg_id):
    async with async_session() as session:
        user_tg_id = await session.execute(select(Users).where(Users.tg_user_id == tg_id))
        return user_tg_id.scalars().first()


async def get_searched_stock(ticer):
    async with async_session() as session:
        ticer = await session.execute(select(SearchInfo).where(SearchInfo.ticer == ticer))
        return ticer.scalars().first()


async def save_user_to_db(message: Message):
    tg_user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    tg_chat_id = message.chat.id

    user = await get_user(tg_user_id)
    print(user)


    if user:
        update_user = update(Users).where(Users.tg_user_id == tg_user_id).values(first_name = first_name)

        async with async_session() as session:
            session.execute(update_user)
            await session.commit()
    else:

        user = Users(
            first_name = first_name,
            last_name = last_name,
            username = username,
            tg_user_id = tg_user_id,
            tg_chat_id = tg_chat_id,
        )

        async with async_session() as session:
            session.add(user)
            await session.commit()


async def save_search_info_to_db(message: Message, data):
    if not data:
        return

    ticer = message.text.lower().strip()
    stock_info = await get_searched_stock(ticer)

    if stock_info:
        async with async_session() as session:
            await session.execute(user_tag.insert().values(tg_user_id=message.from_user.id, search_info_id=stock_info.id))
            await session.commit()
        return

    add_ticer_db = SearchInfo(ticer = ticer)

    async with async_session() as session:
        session.add(add_ticer_db)
        await session.flush()
        await session.execute(user_tag.insert().values(tg_user_id = message.from_user.id, search_info_id = add_ticer_db.id))
        await session.commit()






# import asyncio
# from models import Base, Users, SearchInfo, user_tag
# async def migrate():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

# asyncio.run(migrate())