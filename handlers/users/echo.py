from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery
from filters.states import From
from keyboards.default.default_menus import check_menu, user_main_menu, admin_main_menu, add_and_main
from keyboards.inline.inline_menus import cb_id_remove_desk, get_admin_desk_menu
from loader import dp
from moduls import tasks
from moduls.notifications import send_notification, get_admins_all, get_users_all
from moduls.personnel import get_users, add_user, add_group, is_admin_check, is_admins_check, get_group
from moduls.tasks import get_desks


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!",
                         reply_markup=check_menu)


@dp.message_handler(state="*", text="↪ В главное меню")
async def main_menu(message: types.Message, state: FSMContext):
    if message.text == "↪ В главное меню" and await state.get_state() is not None:
        await state.finish()
    if is_admin_check(message.from_user.id):
        await message.answer("Вы в главном меню!", reply_markup=admin_main_menu)
    else:
        await message.answer("Вы в главном меню!", reply_markup=user_main_menu)


@dp.message_handler(Text(equals=["Пользователь", "Администратор", "2064"]))
async def check(message: Message):
    result = get_users(message.from_user.id)

    if message.text == "Пользователь":
        if len(result) > 0:
            await message.answer("Вы вошли как пользователь!", reply_markup=user_main_menu)
        else:
            await message.answer("Вы должны получить ссылку на приглашение")
    elif message.text == "2064":
        if is_admin_check(message.from_user.id):
            await message.answer("Вы вошли как администратор!", reply_markup=admin_main_menu)
        else:
            if is_admins_check("admins"):
                result = get_group("admins")
                add_user(id_user=message.from_user.id, id_group=result[0][0], _is_admin=True,
                         name=message.from_user.full_name)
            else:
                result = add_group("admins")
                add_user(id_user=message.from_user.id, id_group=result[0][0], _is_admin=True,
                         name=message.from_user.full_name)
            await message.answer("Вы вошли как администратор!", reply_markup=admin_main_menu)
    elif message.text == "Администратор":
        await message.answer("Введите пароль")


@dp.message_handler(Text(equals=["Доска", "Личные задачи", "Кадры", "Задачи"]))
async def check_desk(message: Message):
    if message.text == "Доска":
        await message.answer("Вы перешли в доску", reply_markup=add_and_main)
        result = get_desks()
        if is_admin_check(message.from_user.id):
            for io in result:
                await dp.bot.send_message(chat_id=message.from_user.id, text=io[1],
                                          reply_markup=get_admin_desk_menu(io[0]))
        else:
            for io in result:
                await dp.bot.send_message(chat_id=message.from_user.id, text=io[1])
        await From.add_desk.set()


@dp.message_handler(state=From.add_desk, text="Добавить")
async def add_desk(message):
    await message.answer("Введите текст для доски")
    await From.add_desk2.set()


@dp.message_handler(state=From.add_desk2)
async def add_desk2(message: Message):
    tasks.create_desk_notification(content=message.text)
    await From.add_desk.set()
    await send_notification(IDs=[i[0] for i in get_admins_all(id_user=message.from_user.id,
                                                              name_admins_group="admins")],
                            content=f"📰 {message.from_user.full_name} добавил запись на доску: {message.text}")
    await send_notification(IDs=[i[0] for i in get_users_all(id_user=message.from_user.id)],
                            content=f"📰 {message.from_user.full_name} добавил запись на доску: {message.text}")
    await message.answer("Доска добавлена!")


@dp.callback_query_handler(cb_id_remove_desk.filter(), state="*")
async def remove_desk(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    _id = callback_data.get("id")
    tasks.remove_desk_notification(_id)

# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
# @dp.message_handler(state=None)
# async def bot_echo(message: types.Message):
#     await message.answer(f"Эхо без состояния."
#                          f"Сообщение:\n"
#                          f"{message.text}")
#
#
# # Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
# @dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state = await state.get_state()
#     await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
#                          f"\nСодержание сообщения:\n"
#                          f"<code>{message}</code>")
