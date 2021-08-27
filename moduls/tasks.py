# create_task (Создаёт задачу -> пользователь, задача str)
# edit_task (Редактирование -> id, задача str) \\ админ
# apply_task (подтвердить выполнение -> id задачи)
# close_task (завершение задачи -> id задачи) \\ админ
# delegate_task (передать задачу -> id задачи от к)
# ping_task (напомнить о задачи -> id задачи) \\ админ
# Общие задачи: (Доска с доступом только у админа)
# add_public_task(сообщение)
# remove_public_task(сообщение)
# get_tasks_privat (получить список личных задач)
# get_desks (получить список desks)
# get_tasks_public (получить список личных задач)
# create_desk_notification(Создать доску ->content)
# remove_desk_notification(Удалить доску -> id доски)

import datetime
import sqlite3
from data.config import PART


def create_task(content, user_id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute("INSERT INTO Tasks_users "
                    "(Content, ID_user, Status, Time_add, coment) VALUES (?, ?, ?, ?, ?)",
                    (content, user_id, False, datetime.datetime.today(), ""))
    conn.close()


def edit_task(content, _id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"UPDATE Tasks_users SET Content = '{content}'"
                    f"WHERE ID = {_id}")
    conn.close()


def edit_task_comment(comment, _id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"UPDATE Tasks_users SET coment = coment || '{comment}' "
                    f"WHERE ID = {_id}")
    conn.close()


def create_desk_notification(content):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"INSERT INTO Desk_notifications "
                    f"(Content) VALUES (?)", (content,))
    conn.close()


def remove_desk_notification(_id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"DELETE FROM Desk_notifications WHERE ID = '{_id}'")
    conn.close()


def apply_task(_id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"UPDATE Tasks_users SET Status = '{True}'"
                    f"WHERE ID = {_id}")
    conn.close()


def close_task(_id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"UPDATE Tasks_users SET ID_user = '{0}' WHERE ID = '{_id}'")
    conn.close()


def delegate_task(_id_task, _id_from_user, _id_to_user):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"UPDATE Tasks_users SET ID_user = '{_id_to_user}' WHERE ID = '{_id_task}' "
                    f"AND ID_user = '{_id_from_user}'")
    conn.close()


def ping_task_user(_id_task):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Tasks_users WHERE ID = '{_id_task}'")
        result = cur.fetchall()[0]
    conn.close()
    return result


def get_tasks_privat(id_user):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Tasks_users WHERE ID_user = '{id_user}'")
        result = cur.fetchall()
    conn.close()
    return result


def get_owner_task(id_task):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID = "
                    f"(SELECT MAX(ID_user) FROM Tasks_users WHERE Tasks_users.ID = {id_task})")
    result = cur.fetchall()[0]
    conn.close()
    return result


def get_task_privat(id_task):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Tasks_users WHERE ID = '{id_task}'")
        result = cur.fetchall()[0]
    conn.close()
    return result


def get_tasks_public(id_group):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Tasks_group WHERE ID_group = '{id_group}'")
        result = cur.fetchall()
    conn.close()
    return result


def add_public_task(content, id_user_from):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute("INSERT INTO Desk_notifications "
                    "(Content, Time_add, ID_user_from) VALUES (?, ?, ?)",
                    (content, datetime.datetime.today(), id_user_from))
    conn.close()


def remove_public_task(_id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"DELETE FROM Desk_notifications WHERE ID = '{_id}'")
    conn.close()


def get_desks():
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Desk_notifications")
        result = cur.fetchall()
    conn.close()
    return result
