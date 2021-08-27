from aiogram.types import CallbackQuery

from filters.states import From
from keyboards.inline.inline_menus import cb_id_admin_private_task_delegate, get_inline_menu_users_delegate, \
    cb_id_users_delegate, chois_delegate, cb_cd_y, cb_cd_no
from loader import dp
from moduls.notifications import choice_listeners, send_notification, get_admins_all, get_users_all_and_admins
from moduls.personnel import get_user_group_id, get_user
from moduls.tasks import get_task_privat, delegate_task

temp = {}


@dp.callback_query_handler(cb_id_admin_private_task_delegate.filter(), state="*")
async def delegate_task_f(call: CallbackQuery, callback_data: dict):
    await call.message.answer(text="Выберите получателя",
                              reply_markup=get_inline_menu_users_delegate(
                                  get_users_all_and_admins(call.from_user.id), id_task=callback_data.get("id")))
    await call.message.delete()


@dp.callback_query_handler(cb_id_users_delegate.filter(), state="*")
async def add_comment(call: CallbackQuery, callback_data: dict):
    id_user = callback_data.get("id_user")
    id_task = callback_data.get("id_task")
    await call.message.answer("Ожидайте ответа!")
    await dp.bot.send_message(chat_id=id_user, text=f"Вам было делегировано задание\r\n{get_task_privat(id_task)[1]}",
                              reply_markup=chois_delegate(id_task=id_task, id_owner=call.from_user.id))
    await call.message.delete()


@dp.callback_query_handler(cb_cd_y.filter(), state="*")
async def set_delegate_task(call: CallbackQuery, callback_data: dict):
    id_task = callback_data.get("id_task")
    id_owner = callback_data.get("id_owner")
    delegate_task(_id_task=id_task, _id_from_user=id_owner, _id_to_user=call.from_user.id)
    await send_notification(IDs=[id_owner], content="Задание было передано!")
    await send_notification(IDs=[i[0] for i in get_admins_all(id_user=call.from_user.id,
                                                              name_admins_group="admins")],
                            content=f"Задание {get_task_privat(id_task)[1]} было передано от {get_user(id_owner)[2]}"
                                    f" кому {call.from_user.full_name}!")
    await call.message.delete()


@dp.callback_query_handler(cb_cd_no.filter(), state="*")
async def set_delegate_task(call: CallbackQuery, callback_data: dict):
    id_owner = callback_data.get("id_owner")
    await send_notification(IDs=[id_owner], content="Задание НЕ было принято!")
    await call.message.delete()
