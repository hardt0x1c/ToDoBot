import text.admin.admin_messages as admin_msg
import keyboards.admin.admin_keyboard as kb_admin
# from States.admin.Admin import *
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, FSInputFile
from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from loader import dp, db, bot
# from filters.admin_filters import IsAdmin


@dp.message(Command('admin'))
async def admin_command(message: types.Message):
    await message.answer('Добро пожаловать в админ-панель!')
