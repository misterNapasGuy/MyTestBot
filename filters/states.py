from aiogram.dispatcher.filters.state import StatesGroup, State


class From(StatesGroup):
    delegate_task = State()
    private_task = State()
    group_task = State()
    private_task_admin = State()
    group_task_admin = State()
    add_group = State()
    add_user = State()
    add_desk = State()
    private_task2 = State()
    group_task2 = State()
    private_task_admin2 = State()
    group_task_admin2 = State()
    add_group2 = State()
    add_user2 = State()
    add_desk2 = State()
    edit_comment = State()
    edit_task = State()



