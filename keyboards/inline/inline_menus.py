from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cb_id_execute = CallbackData("Execute", "id")
cb_id_delegate = CallbackData("Delegate", "id")
cb_id_comment = CallbackData("User_private_task_comment", "id")


def get_inline_menu_user_private_task(_id):
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Выполнить", callback_data=cb_id_execute.new(id=_id)),
                InlineKeyboardButton(text="Делегировать", callback_data=cb_id_delegate.new(id=_id)),
                InlineKeyboardButton(text="Комментарий", callback_data=cb_id_comment.new(id=_id))
            ]
        ]
    )
    return menu


cb_id_execute_public_task = CallbackData("Execute_public_task", "id")
cb_id_user_public_task_comment = CallbackData("User_public_task_comment", "id")
cb_id_user_public_comment_remove = CallbackData("User_public_comment_remove", "id")


def get_users_public_task_menu(_id):
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Выполнено", callback_data=cb_id_execute_public_task.new(id=_id)),
                InlineKeyboardButton(text="Делегировать", callback_data=cb_id_user_public_task_comment.new(id=_id))
            ],
            [
                InlineKeyboardButton(text="Добавить комментарий",
                                     callback_data=cb_id_user_public_comment_remove.new(id=_id))
            ]
        ])
    return menu


cb_id_accept_task = CallbackData("Accept_admin_task", "id_user")
cb_id_remove_task = CallbackData("Remove_admin_task", "id_user")
cb_id_edit_task = CallbackData("Edit_admin_task", "id_user")
cb_id_admin_private_task_comment = CallbackData("Admin_private_task_comment", "id_user")
cb_id_admin_private_task_delegate = CallbackData("private_task_delegate", "id_user")


def get_admin_private_task_menu(id_user):
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Выполнено", callback_data=cb_id_accept_task.new(id_user=id_user)),
                InlineKeyboardButton(text="🗑 Удалить", callback_data=cb_id_remove_task.new(id_user=id_user)),
                InlineKeyboardButton(text="✏ Редактировать", callback_data=cb_id_edit_task.new(id_user=id_user))

            ],
            [
                InlineKeyboardButton(text="💬 Коментарий",
                                     callback_data=cb_id_admin_private_task_comment.new(id_user=id_user)),
                InlineKeyboardButton(text="📦 Делегировать",
                                     callback_data=cb_id_admin_private_task_delegate.new(id_user=id_user))
            ]
        ])
    return menu


cb_id_admin_group_task_comment = CallbackData("Admin_group_task_comment", "id")
cd_id_admin_group_task_comment_remove = CallbackData("Admin_group_task_comment_remove", "id")

# Доска админа
cb_id_remove_desk = CallbackData("Remove_desk", "id")


def get_admin_desk_menu(_id):
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Удалить доску", callback_data=cb_id_remove_desk.new(id=_id))
            ]
        ])
    return menu


cb_id_remove_user = CallbackData("Remove_user", "id")
cb_id_edit_user = CallbackData("Edit_user", "id")


def get_admin_user_info_menu(_id):
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Удалить", callback_data=cb_id_remove_user.new(id=_id))
            ]
        ])
    return menu


cb_id_group = CallbackData("choice", "id_group")


def get_inline_menu_groups(groups: list):
    menu = InlineKeyboardMarkup(row_width=1)
    for i in range(len(groups)):
        key = InlineKeyboardButton(text=f"Группа {groups[i][1]}", callback_data=cb_id_group.new(groups[i][0]))
        menu.insert(key)
    return menu


# users_chices вернется самым первым при коллбеке id_user поле для записи значения
cb_id_users = CallbackData("users_choice", "id_user")


def get_inline_menu_users(users: list):
    menu = InlineKeyboardMarkup(row_width=1)
    for i in range(len(users)):
        key = InlineKeyboardButton(text=f"Пользователь {users[i][2]}", callback_data=cb_id_users.new(users[i][0]))
        menu.insert(key)
    return menu


cb_id_users_delegate = CallbackData("users_choice", "id_user", "id_task")


def get_inline_menu_users_delegate(users: list, id_task):
    menu = InlineKeyboardMarkup(row_width=3)
    for i in range(len(users)):
        key = InlineKeyboardButton(text=f"Пользователь {users[i][2]}",
                                   callback_data=cb_id_users_delegate.new(id_user=users[i][0], id_task=id_task))
        menu.insert(key)
    return menu


cb_id_id_tasks_apply = CallbackData("cb_id_id_tasks_apply", "id_user", "id_task")


def get_im_id_tasks_apply(tasks: list, id_user):
    menu = InlineKeyboardMarkup(row_width=3)
    for i in range(len(tasks)):
        if not tasks[i][3]:
            key = InlineKeyboardButton(text=f"Задание №{i + 1}",
                                       callback_data=cb_id_id_tasks_apply.new(id_user=id_user, id_task=tasks[i][0]))
            menu.insert(key)
    return menu


cb_id_id_tasks_edit = CallbackData("cb_id_id_tasks_edit", "id_user", "id_task")


def get_im_id_tasks_edit(tasks: list, id_user):
    menu = InlineKeyboardMarkup(row_width=3)
    for i in range(len(tasks)):
        key = InlineKeyboardButton(text=f"Задание №{i + 1}",
                                   callback_data=cb_id_id_tasks_edit.new(id_user=id_user, id_task=tasks[i][0]))
        menu.insert(key)
    return menu


cb_id_id_tasks_comment = CallbackData("cb_id_id_tasks_comment", "id_user", "id_task")


def get_im_id_tasks_comment(tasks: list, id_user):
    menu = InlineKeyboardMarkup(row_width=3)
    for i in range(len(tasks)):
        key = InlineKeyboardButton(text=f"Задание №{i + 1}",
                                   callback_data=cb_id_id_tasks_comment.new(id_user=id_user, id_task=tasks[i][0]))
        menu.insert(key)
    return menu


cb_id_id_tasks_remove = CallbackData("cb_id_id_tasks_remove", "id_user", "id_task")


def get_im_id_tasks_remove(tasks: list, id_user):
    menu = InlineKeyboardMarkup(row_width=3)
    for i in range(len(tasks)):
        key = InlineKeyboardButton(text=f"Задание №{i + 1}",
                                   callback_data=cb_id_id_tasks_remove.new(id_user=id_user, id_task=tasks[i][0]))
        menu.insert(key)
    return menu


cb_cd_y = CallbackData("Remove_user", "id_task", "id_owner")
cb_cd_no = CallbackData("Edit_user", "id_task", "id_owner")


def chois_delegate(id_task, id_owner):
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Принять", callback_data=cb_cd_y.new(id_task=id_task, id_owner=id_owner)),
                InlineKeyboardButton(text="Отклонить", callback_data=cb_cd_no.new(id_task=id_task, id_owner=id_owner))
            ]
        ])
    return menu


cb_id_load_report_users = CallbackData("Load_report", "id")


def get_admin_load_report_menu(_id):
    menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Загрузить отчет пользователей",
                                     callback_data=cb_id_load_report_users.new(id=_id))
            ]
        ]
    )
    return menu
