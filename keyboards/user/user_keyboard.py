from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


user_actions = [
    [KeyboardButton(text='Показать задачи')],
    [KeyboardButton(text='Добавить задачу'),
     KeyboardButton(text='Удалить задачу')],
    [KeyboardButton(text='Удалить все задачи')]
]
user_actions = ReplyKeyboardMarkup(keyboard=user_actions, resize_keyboard=True)
