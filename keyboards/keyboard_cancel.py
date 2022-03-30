from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

keyboard_student_cancel = InlineKeyboardMarkup(resize_keyboard=True)
keyboard_student_cancel.add(InlineKeyboardButton(
    emojize(':house: В главное меню'), callback_data='cancel_other'))

keyboard_teacher_cancel = InlineKeyboardMarkup(
    resize_keyboard=True, row_width=1)
keyboard_teacher_cancel.add(InlineKeyboardButton(
    'Отмена', callback_data='cancel_menu'))
