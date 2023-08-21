import text.user.user_messages as user_msg
import keyboards.user.user_keyboard as user_kb
import keyboards.user.show_tasks_pagination as user_kb_pag
from States.user import User
from aiogram import types
from aiogram.types import URLInputFile
from aiogram import F
from aiogram.fsm.context import FSMContext
from loader import dp, db, bot
from config import *


@dp.callback_query(lambda c: c.data.startswith('show_task_number_'))
async def show_task(callback: types.CallbackQuery):
    task_index = int(callback.data.split("_")[3])
    index_page = int(callback.data.split('_')[4])
    task = db.get_user_task_by_id(who_user=callback.from_user.id, task_id=task_index)
    await callback.message.delete()
    if task[4] == '':
        await callback.message.answer(user_msg.show_task.format(task[2], task[3], task[5]),
                                      reply_markup=user_kb_pag.task_menu(task_index, index_page))
    else:
        photo = URLInputFile(task[4])
        await callback.message.answer_photo(photo,
                                            caption=user_msg.show_task.format(task[2], task[3], task[5]),
                                            reply_markup=user_kb_pag.task_menu(task_index, index_page))


@dp.callback_query(lambda c: c.data.startswith('return_tasks_'))
async def return_tasks(callback: types.CallbackQuery):
    index_page = int(callback.data.split('_')[2])
    tasks = db.get_user_tasks(who_user=callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer('Ваш список задач:',
                                  reply_markup=user_kb_pag.show_tasks(tasks=tasks, index_page=index_page))


@dp.callback_query(lambda c: c.data.startswith('delete_task_'))
async def delete_task(callback: types.CallbackQuery):
    task = int(callback.data.split('_')[2])
    index_page = int(callback.data.split('_')[3])
    await callback.message.delete()
    await callback.message.answer('Вы уверенны, что хотите удалить задачу?',
                                  reply_markup=user_kb_pag.task_delete_menu(task=task, index_page=index_page))


@dp.callback_query(lambda c: c.data.startswith('confirm_delete_task_'))
async def delete_task_confirm(callback: types.CallbackQuery):
    task = int(callback.data.split('_')[3])
    index_page = int(callback.data.split('_')[4])
    if db.delete_task(task_id=task, who_user=callback.from_user.id):
        tasks = db.get_user_tasks(who_user=callback.from_user.id)
        await callback.message.answer('Задача успешно удалена!',
                                      reply_markup=user_kb_pag.show_tasks(tasks=tasks, index_page=index_page))
    else:
        tasks = db.get_user_tasks(who_user=callback.from_user.id)
        await callback.message.answer('Не удалось удалить задачу!',
                                      reply_markup=user_kb_pag.show_tasks(tasks=tasks, index_page=index_page))


@dp.callback_query(lambda c: c.data.startswith('edit_task_'))
async def edit_task(callback: types.CallbackQuery):
    task = callback.data.split('_')[2]
    index_page = callback.data.split('_')[3]
    await callback.message.answer('Выберите, что хотите изменить:',
                                  reply_markup=user_kb_pag.task_edit_menu(task=task, index_page=index_page))


@dp.callback_query(lambda c: c.data.startswith('change_task_'))
async def change_task(callback: types.CallbackQuery, state: FSMContext):
    edit = callback.data.split('_')[2]
    task = int(callback.data.split('_')[3])
    if edit == 'title':
        await callback.message.answer('Введите новое название задачи:')
        await state.set_state(User.edit_task_title)
        await state.update_data(task_id=task)
    elif edit == 'desc':
        await callback.message.answer('Введите новое описание задачи:')
        await state.set_state(User.edit_task_desc)
        await state.update_data(task_id=task)
    elif edit == 'date':
        await callback.message.answer('Введите новую дату задачи:')
        await state.set_state(User.edit_task_date)
        await state.update_data(task_id=task)
    elif edit == 'url':
        await callback.message.answer('Введите новую ссылку картинки:')
        await state.set_state(User.edit_task_url)
        await state.update_data(task_id=task)


@dp.message(User.edit_task_title)
async def edit_task_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_id = data['task_id']
    new_title = message.text
    if db.update_task_title(who_user=message.from_user.id, new_title=new_title, task_id=task_id):
        await message.answer('Название задачи успешно изменено!')
        await state.clear()
    else:
        await message.answer('Не удалось изменить название задачи!')
        await state.clear()


@dp.message(User.edit_task_desc)
async def edit_task_desc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_id = data['task_id']
    new_desc = message.text
    if db.update_task_desc(who_user=message.from_user.id, new_desc=new_desc, task_id=task_id):
        await message.answer('Описание задачи успешно изменено!')
        await state.clear()
    else:
        await message.answer('Не удалось изменить название задачи!')
        await state.clear()


@dp.message(User.edit_task_date)
async def edit_task_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_id = data['task_id']
    new_date = message.text
    if db.update_task_date(who_user=message.from_user.id, new_date=new_date, task_id=task_id):
        await message.answer('Дата задачи успешно изменена!')
        await state.clear()
    else:
        await message.answer('Не удалось изменить дату задачи!')
        await state.clear()


@dp.message(User.edit_task_url)
async def edit_task_url(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_id = data['task_id']
    new_url = message.text
    if db.update_task_url(who_user=message.from_user.id, new_url=new_url, task_id=task_id):
        await message.answer('Картинка успешно изменена!')
        await state.clear()
    else:
        await message.answer('Не удалось изменить картинку!')
        await state.clear()


@dp.callback_query(F.data == 'close_tab')
async def close_tab(callback: types.CallbackQuery):
    await callback.message.delete()
