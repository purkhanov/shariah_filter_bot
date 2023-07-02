
from datetime import date
from sqlalchemy import Table, String, Integer, Column, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


user_tag = Table('user_tag', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('searched', Integer, default=1),
    Column('tg_user_id', String, ForeignKey('users.tg_user_id')),
    Column('search_info_id', Integer, ForeignKey('search_info.id')))


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    is_admin = Column(Boolean, default=False)
    super_user = Column(Boolean, default=False)
    paid = Column(Boolean, default=False)
    searched = Column(Integer, default=0)
    tg_user_id = Column(String(30),unique=True, nullable=False)
    tg_chat_id = Column(String(30), nullable=False)
    last_paid = Column(DateTime, nullable=True)
    joined = Column(DateTime, default=date.today())


class SearchInfo(Base):
    __tablename__ = 'search_info'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    ticer = Column(String(30), nullable=False)