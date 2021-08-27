from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from filters.states import From
from keyboards.default.default_menus import add_and_main
from keyboards.inline.inline_menus import get_admin_private_task_menu, cb_id_remove_task, \
    cb_id_accept_task, cb_id_admin_private_task_comment, get_im_id_tasks_remove, \
    cb_id_id_tasks_remove, get_im_id_tasks_apply, cb_id_id_tasks_apply, cb_id_edit_task, get_im_id_tasks_edit, \
    cb_id_id_tasks_edit, get_im_id_tasks_comment, cb_id_id_tasks_comment
from loader import dp, bot
from moduls.notifications import send_notification, get_admins_all
from moduls.personnel import is_admin_check
from moduls.tasks import get_tasks_privat, create_task, close_task, edit_task_comment, get_owner_task, apply_task, \
    edit_task

temp_messages_task = {}


def get_tasks_string(id_user):
    result = get_tasks_privat(id_user=id_user)
    private_tasks = ""
    for io in result:
        if io[5] != "":
            private_tasks += f"№{result.index(io) + 1} {'✅ ' if io[3] else '⭕ '}{io[1]}\r\n📩 Коментарий:\r\n{io[5]}"
        else:
            private_tasks += f"№{result.index(io) + 1} {'✅ ' if io[3] else '⭕ '} {io[1]}"
        private_tasks += "\r\n\n"
    return private_tasks


@dp.message_handler(Text(equals=["Личные задачи"]))
async def check_private_tasks(message: Message):
    if message.text == "Личные задачи":
        await From.private_task.set()
        await message.answer("💫 Это ваши задачи! Удачной работы!", reply_markup=add_and_main)
        temp_messages_task[f"{message.from_user.id}"] = \
            await bot.send_message(chat_id=message.from_user.id, text=get_tasks_string(message.from_user.id),
                                   reply_markup=get_admin_private_task_menu(message.from_user.id))


@dp.callback_query_handler(cb_id_remove_task.filter(), state="*")
async def remove_private_task(call: CallbackQuery, callback_data: dict):
    _id = callback_data.get("id_user")
    await call.message.edit_text(text=get_tasks_string(call.from_user.id),
                                 reply_markup=get_im_id_tasks_remove(tasks=get_tasks_privat(id_user=_id), id_user=_id))


@dp.callback_query_handler(cb_id_id_tasks_remove.filter(), state="*")
async def remove_private_task2(call: CallbackQuery, callback_data: dict):
    tasks = callback_data.get("id_task")
    id_user = get_owner_task(tasks)[0]
    await send_notification(IDs=[id_user], content=f"Задача: {get_tasks_privat(id_user)[0][1]}.\r\n"
                                                   f"была удалена - {call.from_user.full_name}")
    close_task(tasks)
    await call.message.edit_text(text=get_tasks_string(call.from_user.id),
                                 reply_markup=get_admin_private_task_menu(call.from_user.id))


@dp.callback_query_handler(cb_id_accept_task.filter(), state="*")
async def apply_private_task(call: CallbackQuery, callback_data: dict):
    _id = callback_data.get("id_user")
    await call.message.edit_text(text=get_tasks_string(call.from_user.id),
                                 reply_markup=get_im_id_tasks_apply(tasks=get_tasks_privat(id_user=_id), id_user=_id))


@dp.callback_query_handler(cb_id_id_tasks_apply.filter(), state="*")
async def apply_private_task2(call: CallbackQuery, callback_data: dict):
    tasks = callback_data.get("id_task")
    apply_task(tasks)
    await call.message.edit_text(text=get_tasks_string(call.from_user.id),
                                 reply_markup=get_admin_private_task_menu(call.from_user.id))


temp: dict = {}


@dp.callback_query_handler(cb_id_edit_task.filter(), state="*")
async def edit_private_task(call: CallbackQuery, callback_data: dict):
    _id = callback_data.get("id_user")
    await call.message.edit_text(text=get_tasks_string(call.from_user.id),
                                 reply_markup=get_im_id_tasks_edit(tasks=get_tasks_privat(id_user=_id), id_user=_id))


@dp.callback_query_handler(cb_id_id_tasks_edit.filter(), state="*")
async def edit_private_task2(call: CallbackQuery, callback_data: dict):
    _id = callback_data.get("id_task")
    temp[f"{call.from_user.id}"] = _id
    await call.message.edit_text(text="Введите новые данные!")
    await From.edit_task.set()


@dp.message_handler(state=From.edit_task)
async def edit_private_task3(message: Message):
    if message.text == "Редактировать" or message.text == "Добавить" or message.text == "↪ В главное меню":
        await message.answer(text="Данные не верны!")
        await From.private_task.set()
        return None

    edit_task(content=f"{message.text}", _id=temp.pop(f"{message.from_user.id}"))
    await From.private_task.set()
    await message.answer(text="✅ изменения внесены!")

    await message.answer(text=get_tasks_string(message.from_user.id),
                         reply_markup=get_admin_private_task_menu(message.from_user.id))


@dp.callback_query_handler(cb_id_admin_private_task_comment.filter(), state="*")
async def add_comment(call: CallbackQuery, callback_data: dict):
    _id = callback_data.get("id_user")
    await call.message.edit_text(text=get_tasks_string(call.from_user.id),
                                 reply_markup=get_im_id_tasks_comment(tasks=get_tasks_privat(id_user=_id), id_user=_id))


@dp.callback_query_handler(cb_id_id_tasks_comment.filter(), state="*")
async def add_comment2(call: CallbackQuery, callback_data: dict):
    await call.message.answer(text="Введите новый коментарий")
    temp[f"{call.from_user.id}"] = callback_data.get("id_task")
    await From.edit_comment.set()


@dp.message_handler(state=From.edit_comment)
async def add_comment3(message):
    if message.text == "Редактировать" or message.text == "Добавить" or message.text == "↪ В главное меню":
        await message.answer(text="Данные не верны!")
        await From.private_task.set()
        return None
    await message.answer(text=f"{temp[f'{message.from_user.id}']}")
    edit_task_comment(comment=f"📄 {message.text}\r\n", _id=temp.pop(f"{message.from_user.id}"))
    await From.private_task.set()
    await message.answer(text="✅ Коментарий добавлен!")
    await message.answer(text=get_tasks_string(message.from_user.id),
                         reply_markup=get_admin_private_task_menu(message.from_user.id))


@dp.message_handler(state=From.private_task, text="Добавить")
async def add_private_task(message):
    await message.answer("Введите текст задачи")
    await From.private_task2.set()


@dp.message_handler(state=From.private_task2)
async def add_private_task2(message: Message):
    if message.text == "Редактировать" or message.text == "Добавить" or message.text == "↪ В главное меню":
        await message.answer(text="Данные не верны!")
        await From.private_task.set()
        return None

    create_task(content=f"{message.text}", user_id=message.from_user.id)

    await From.private_task.set()
    await send_notification(IDs=[i[0] for i in get_admins_all(id_user=message.from_user.id,
                                                              name_admins_group="admins")],
                            content=f"📰 {message.from_user.full_name} добавил себе задание: {message.text}")
    await message.answer("Задача добавлена!")
    await bot.send_message(chat_id=message.from_user.id, text=get_tasks_string(message.from_user.id),
                           reply_markup=get_admin_private_task_menu(message.from_user.id))
