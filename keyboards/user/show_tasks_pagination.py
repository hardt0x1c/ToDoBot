from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loader import db


def show_tasks(tasks, index_page):
    count_tasks = len(tasks)
    menu = InlineKeyboardBuilder()
    count_in_page = 10
    last_page = False
    user_tasks = []

    # Calculate start and end indices based on index_page
    start = (index_page - 1) * count_in_page
    end = start + count_in_page

    try:
        for task in tasks[start:end]:
            user_tasks.append(task)
    except Exception as ex:
        print(ex)

    if len(user_tasks) < 10:
        last_page = True

    for task in tasks:
        task_b = InlineKeyboardButton(text=f"{task[2]}",
                                      callback_data=f"show_task_number_{task[0]}_{index_page}")
        menu.add(task_b)

    # Add pagination buttons
    if count_tasks <= count_in_page:
        # Only one page of models, no pagination needed
        pass
    elif last_page is True:
        # Last page, add only previous page button
        page_b = InlineKeyboardButton(text="<<",
                                      callback_data=f"change_page_{index_page - 1}")
        menu.add(page_b)
    elif last_page is False and index_page == 1 and len(user_tasks) == 10:
        # First page, add only next page button
        page_b = InlineKeyboardButton(text=">>",
                                      callback_data=f"change_page_{index_page + 1}")
        menu.add(page_b)
    elif last_page is False and index_page != 1:
        # Middle page, add both previous and next page buttons
        prev_b = InlineKeyboardButton(text="<<",
                                      callback_data=f"change_page_{index_page - 1}")
        page_b = InlineKeyboardButton(text=">>",
                                      callback_data=f"change_page_{index_page + 1}")
        menu.row(prev_b, page_b)
    else:
        # Error condition, add previous page button as fallback
        page_b = InlineKeyboardButton(text="<<",
                                      callback_data=f"change_page_{index_page - 1}")
        menu.add(page_b)
    close_ta = InlineKeyboardButton(text="❌ Закрыть",
                                    callback_data=f"close_tab")
    menu.add(close_ta)
    menu.adjust(1)
    menu_inline = menu.as_markup()
    return menu_inline


def task_menu(task, index_page):
    menu = InlineKeyboardBuilder()
    delete_task = InlineKeyboardButton(text='Удалить',
                                       callback_data=f'delete_task_{task}_{index_page}')
    edit_task = InlineKeyboardButton(text='Редактировать',
                                     callback_data=f'edit_task_{task}_{index_page}')
    back = InlineKeyboardButton(text='◀️ Назад',
                                callback_data=f'return_tasks_{index_page}')
    menu.add(delete_task, edit_task, back)
    menu.adjust(1)
    menu = menu.as_markup()
    return menu


def task_delete_menu(task, index_page):
    menu = InlineKeyboardBuilder()
    delete_task_confirm = InlineKeyboardButton(text='Подтвердить',
                                               callback_data=f'confirm_delete_task_{task}_{index_page}')
    delete_task_cancel = InlineKeyboardButton(text='Отменить',
                                              callback_data=f'show_task_number_{task}_{index_page}')
    menu.add(delete_task_confirm, delete_task_cancel)
    menu.adjust(1)
    menu = menu.as_markup()
    return menu


def task_edit_menu(task, index_page):
    menu = InlineKeyboardBuilder()
    edit_title = InlineKeyboardButton(text='Изменить название',
                                      callback_data=f'change_task_title_{task}_{index_page}')
    edit_desc = InlineKeyboardButton(text='Изменить описание',
                                     callback_data=f'change_task_desc_{task}_{index_page}')
    edit_date = InlineKeyboardButton(text='Изменить дату',
                                     callback_data=f'change_task_date_{task}_{index_page}')
    edit_url = InlineKeyboardButton(text='Изменить картинку',
                                    callback_data=f'change_task_url_{task}_{index_page}')
    back = InlineKeyboardButton(text='◀️ Назад',
                                callback_data=f'return_task_{task}_{index_page}')
    menu.add(edit_title, edit_desc, edit_date, edit_url, back)
    menu.adjust(1)
    menu = menu.as_markup()
    return menu
