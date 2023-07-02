
import sqlite3 as sq
from datetime import date
from aiogram.types import Message


def sql_start():
    try:
        con = sq.connect('shariah_filter.db')
        cur = con.cursor()

        create_table_users = 'CREATE TABLE IF NOT EXISTS \
            users (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                  name TEXT, \
                  username TEXT, \
                  is_admin BLOB NOT NULL DEFAULT 0, \
                  super_user BLOB NOT NULL DEFAULT 0, \
                  paid BLOB NOT NULL DEFAULT 0, \
                  searched INTEGER DEFAULT 0, \
                  tg_user_id TEXT NOT NULL, \
                  tg_chat_id TEXT NOT NULL, \
                  joined TEXT NOT NULL)'

        create_table_search_info = 'CREATE TABLE IF NOT EXISTS \
            search_info (id INTEGER PRIMARY KEY AUTOINCREMENT, searched TEXT NOT NULL)'

        create_table_link = 'CREATE TABLE IF NOT EXISTS \
            link (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                  tg_user_id INTEGER NOT NULL, \
                  search_info_id INTEGER NOT NULL, \
                  FOREIGN KEY (tg_user_id) REFERENCES users (tg_user_id) \
                  FOREIGN KEY (search_info_id) REFERENCES search_info (id))'

        if con:
            print('Data base connected OK!')

        cur.execute(create_table_users)
        cur.execute(create_table_search_info)
        cur.execute(create_table_link)

    except sq.Error as er:
        print('Ошибка при создании БД', er)

    finally:
        if con: con.close()


async def connect_db():
    try:
        con = sq.connect('shariah_filter.db')
        con.row_factory = sq.Row
        return con

    except sq.Error as er:
        print('Can not connecting some error: ', er)
    except Exception as ex:
        print(ex)


async def save_user_to_db(message: Message, data):
    has_user =  await get_user_info(message.from_user.id)

    if has_user:
        if not data: return

        save_user = 'UPDATE users SET searched = searched + 1 WHERE tg_user_id = ?'
        user_info = (message.from_user.id,)
    else:
        if data:
            save_user = 'INSERT INTO users \
                (name, username, searched, tg_user_id, tg_chat_id, joined) \
                VALUES (?, ?, ?, ?, ?, ?)'

            user_info = (message.from_user.first_name,
                message.from_user.username,
                1,
                message.from_user.id,
                message.chat.id,
                date.today())
        else:
            save_user = 'INSERT INTO users \
                (name, username, tg_user_id, tg_chat_id, joined) \
                VALUES (?, ?, ?, ?, ?)'

            user_info = (message.from_user.first_name,
                message.from_user.username,
                message.from_user.id,
                message.chat.id,
                date.today())

    try:
        con = await connect_db()
        cur = con.cursor()

        cur.execute(save_user, user_info)
        con.commit()

    except sq.Error as er:
        print(er)

    finally:
        if con: con.close()


async def get_all_users():
    try:
        con = await connect_db()
        cur = con.cursor()

        user_info = cur.execute('SELECT * FROM users').fetchall()

        if user_info:
            return user_info

        return False

    except sq.Error as er:
        print('Error in function: get_user_info', er)

    finally:
        if con: con.close()


async def get_user_info(user_id):
    try:
        con = await connect_db()
        cur = con.cursor()

        user_info = cur.execute('SELECT * FROM users WHERE tg_user_id = ?', (user_id,)).fetchone()

        if user_info:
            return dict(user_info)

        return False

    except sq.Error as er:
        print('Error in function: get_user_info', er)

    finally:
        if con: con.close()


async def get_search_info(searched_text):
    try:
        con = await connect_db()
        cur = con.cursor()

        search_info = cur.execute('SELECT * FROM search_info WHERE searched = ?', (searched_text,)).fetchone()

        if search_info:
            return dict(search_info)

        return False

    except sq.Error as er:
        print('Error in function: get_search_info', er)

    finally:
        if con: con.close()


async def save_search_info_to_db(message: Message, data):
    if not data:
        return

    search_info = await get_search_info(message.text.lower())

    try:
        user_searched = await user_is_searched(message.from_user.id, search_info['id'])
    except:
        user_searched = False

    try:
        con = await connect_db()
        cur = con.cursor()

        if search_info:
            if not user_searched:
                cur.execute('INSERT INTO link (tg_user_id, search_info_id) VALUES (?, ?)',
                        (message.from_user.id, search_info['id']))

        else:
            cur.execute('INSERT INTO search_info (searched) VALUES (?)', (message.text.lower(),))
            last_row_id = cur.lastrowid

            cur.execute('INSERT INTO link (tg_user_id, search_info_id) VALUES (?, ?)',
                        (message.from_user.id, last_row_id))

        con.commit()

    except sq.Error as er:
        print('Error in function: save_search_info_to_db', er)

    finally:
        if con: con.close()


async def user_is_searched(tg_user_id, search_info_id):
    try:
        con = await connect_db()
        cur = con.cursor()

        user_is_searched = cur.execute('SELECT * FROM link WHERE tg_user_id = ? AND search_info_id = ?', (tg_user_id, search_info_id)).fetchall()

        if user_is_searched:
            return True

        return False

    except sq.Error as er:
        print('Error in function: user_is_searched', er)

    finally:
        if con: con.close()