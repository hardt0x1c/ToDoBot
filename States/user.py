from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    add_task_title = State()
    add_task_desc = State()
    add_task_url = State()
    delete_task = State()
    edit_task_title = State()
    edit_task_desc = State()
    edit_task_date = State()
    edit_task_url = State()
