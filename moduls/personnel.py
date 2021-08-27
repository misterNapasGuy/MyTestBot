# Кадры:
# Add_user(Добавить пользователя -> Имя )
# Add_group(Добавить группу -> Название)
# get_users (получить список личных задачь)
# get_groups (получить список личных задачь)
# is_admin(Проверка на админа)
import sqlite3
from data.config import PART


def get_users(id_group):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID_group = '{id_group}'")
        result = cur.fetchall()
    return result


def get_user(id_user):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID = '{id_user}'")
        result = cur.fetchall()[0]
    return result


def add_user(id_user, id_group, name, _is_admin):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute("INSERT INTO Users "
                    "(ID, ID_group, Name, IS_admin) VALUES (?, ?, ?, ?)",
                    (id_user, id_group, name, _is_admin))
    conn.close()


def get_groups():
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Groups")
        result = cur.fetchall()
    return result


def add_group(name):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"INSERT INTO Groups (Name) VALUES ('{name}')")
    with conn:
        cur.execute(f"SELECT MAX(ID) FROM Groups WHERE Name = '{name}'")
    result = cur.fetchall()
    conn.close()
    return result


def get_group(name):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT MAX(ID) FROM Groups WHERE Name = '{name}'")
    result = cur.fetchall()
    conn.close()
    return result


def get_group_name(_id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Groups WHERE ID = '{_id}'")
    result = cur.fetchall()[0][1]
    conn.close()
    return result


def get_user_group_id(id_user):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Groups WHERE ID = (SELECT MAX(ID_group) FROM Users WHERE Users.ID ='{id_user}')")
    result = cur.fetchall()[0][0]
    conn.close()
    return result


def is_admins_check(name_admins_group):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Groups WHERE Name = '{name_admins_group}'")
    result = cur.fetchall()
    conn.close()
    if len(result) > 0 and result is not None:
        return True
    else:
        return False


def is_admin_check(_id):
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"SELECT * FROM Users WHERE ID = '{_id}' AND IS_admin = {True}")
    result = cur.fetchall()
    conn.close()
    if len(result) > 0:
        return True
    else:
        return False

def get_tasks_and_users():
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    query = "SELECT DISTINCT Tasks_users.ID_user, Content, Name, Status FROM Tasks_users, " \
            "Users WHERE Tasks_users.ID_user = Users.ID"
    with conn:
        cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result


def get_group_tasks_result():
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    query = "SELECT DISTINCT Groups.ID, Groups.Name, Tasks_group.Content,  Tasks_group.Status " \
            "FROM Groups, Tasks_group WHERE  Groups.ID= Tasks_group.ID_group"
    with conn:
        cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result


def update_user_id_private_task():
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"UPDATE Tasks_users SET ID_user = 0  WHERE Status = 1")
    result = cur.fetchall()
    conn.close()


def update_group_id_public_task():
    conn = sqlite3.connect(PART)
    cur = conn.cursor()
    with conn:
        cur.execute(f"UPDATE Tasks_group SET ID_group = 0 WHERE Status = 1")
    result = cur.fetchall()
    conn.close()
