# Оповещения:
# send_notification (организует отправку оповещения ->  от,  к, сообщения)
# choice_listeners (Выборка получателей)
from aiogram import types
from data.config import PART
import sqlite3
from loader import dp


async def send_notification(IDs: list, content):
    for i in range(len(IDs)):
        await dp.bot.send_message(chat_id=IDs[i], text=content)


def choice_listeners(id_group):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID_group = '{id_group}'")
    result = cur.fetchall()
    return [i[0] for i in result]


def get_users_all(id_user):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID != '{id_user}' AND IS_admin = {False}")
        result = cur.fetchall()
    return result


def get_users_all_and_admins(id_user):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID != '{id_user}'")
        result = cur.fetchall()
    return result


def get_admins_all(id_user, name_admins_group):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID != '{id_user}' AND ID_group ="
                    f" (SELECT ID FROM Groups WHERE Name = '{name_admins_group}' LIMIT 1)")
        result = cur.fetchall()
    return result
