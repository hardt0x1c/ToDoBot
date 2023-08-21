import text.user.user_messages as user_msg
import keyboards.user.user_keyboard as user_kb
import keyboards.user.show_tasks_pagination as user_kb_pag
from States.user import User
from aiogram import types
from aiogram.types import FSInputFile
from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from loader import dp, db, bot
from config import *


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(user_msg.greet.format(BOT_NAME), reply_markup=user_kb.user_actions)


@dp.message(Command('add_task'))
@dp.message(F.text == 'Добавить задачу')
async def add_task(message: types.Message, state: FSMContext):
    await message.answer(user_msg.add_task_title)
    await state.set_state(User.add_task_title)


@dp.message(User.add_task_title)
async def add_task_title(message: types.Message, state: FSMContext):
    await message.answer(user_msg.add_task_desc)
    task_title = message.text
    await state.update_data(task_title=task_title)
    await state.set_state(User.add_task_desc)


@dp.message(User.add_task_desc)
async def add_task_desc(message: types.Message, state: FSMContext):
    await state.update_data(task_desc=message.text)
    await message.answer('Отправьте ссылку на фотографию к задаче, если не нужно отправьте 0')
    await state.set_state(User.add_task_url)


@dp.message(User.add_task_url)
async def add_task_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_title = data['task_title']
    task_desc = data['task_desc']
    task_url = message.text if message.text != '0' else ''

    if db.add_task(who_user=message.from_user.id, title=task_title, desc=task_desc, img_url=task_url):
        await message.answer(user_msg.add_task_success)
        await state.clear()
    else:
        await message.answer(user_msg.add_task_error)
        await state.clear()


@dp.message(Command('show_tasks'))
@dp.message(F.text == 'Показать задачи')
async def show_tasks(message: types.Message):
    tasks = db.get_user_tasks(who_user=message.from_user.id)
    await message.answer('Ваш список задач:',
                         reply_markup=user_kb_pag.show_tasks(tasks=tasks, index_page=1))


@dp.message(Command('delete_task'))
@dp.message(F.text == 'Удалить задачу')
async def delete_task_title(message: types.Message, state: FSMContext):
    await message.answer(user_msg.delete_task)
    await state.set_state(User.delete_task)


@dp.message(User.delete_task)
async def delete_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    title = message.text
    if db.delete_task(task_title=title, who_user=user_id):
        await message.answer(user_msg.delete_task_success)
        await state.clear()
    else:
        await message.answer(user_msg.delete_task_error)
        await state.clear()


@dp.message(Command('delete_tasks'))
async def delete_tasks(message: types.Message):
    await message.answer('Вы уверенны, что хотите удалить все задачи?')


@dp.callback_query(F.data == 'asdasdasd')
async def delete_tasks_confirm(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if db.delete_tasks(who_user=user_id):
        await callback.message.answer('Все задачи успешно удалены!')
    else:
        await callback.message.answer('Не удалось удалить задачи!')
