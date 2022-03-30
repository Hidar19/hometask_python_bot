from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from emoji import emojize
import json

from config import conn, cur, bot

from keyboards.keyboard import StudentKeyboards
from keyboards.keyboard import OtherKeyboards

from get_info import *

from handlers.student_handler import homework


class FSMChange_class(StatesGroup):
    number_class = State()


class FSMChange_username(StatesGroup):
    username = State()


async def setting(message: Message):
    person = get_person(message.from_user.id)
    if len(person) == 0:
        await homework.homework_show(message, state=None)
    await message.answer(f'''
<b>Настройки</b>
Класс: <i>{person[0]} класс,</i>
Обращение: <i>{person[1]}</i>''', reply_markup=StudentKeyboards.keyboard_setting())


async def cancel_setting(call: CallbackQuery, state: FSMContext):
    person = get_person(call.from_user.id)
    await bot.answer_callback_query(call.id)
    await state.finish()
    await call.message.edit_text(f'''
<b>Настройки</b>
Класс: <i>{person[0]} класс,</i>
Обращение: <i>{person[1]}</i>''', reply_markup=StudentKeyboards.keyboard_setting())


async def setting_class(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    with open('classes.json', 'r') as f_classes:
        await call.message.edit_text('Выберите класс:', reply_markup=OtherKeyboards.keyboard_class_generate(json.load(f_classes)))
    await FSMChange_class.number_class.set()


async def new_number_class(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    cur.execute('UPDATE users SET class=? WHERE user_id = ?;',
                (call.data, call.from_user.id,))
    conn.commit()
    await cancel_setting(call, state)


async def setting_username(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    keyboard_cancel = InlineKeyboardMarkup(resize_keyboard=True).add(
        InlineKeyboardButton('Отмена', callback_data='cancel_setting'))
    await call.message.edit_text('Впишите новое обращение', reply_markup=keyboard_cancel)
    await FSMChange_username.username.set()


async def new_username(message: Message, state: FSMContext):
    cur.execute('UPDATE users SET first_name=? WHERE user_id = ?;',
                (message.text, message.from_user.id,))
    conn.commit()
    await state.finish()
    await setting(message)


def setting_handlers(dp: Dispatcher):
    dp.register_message_handler(setting, Text(
        equals=emojize(':gear: Настройки')))
    dp.register_message_handler(setting, commands='setting')
    dp.register_callback_query_handler(
        setting_class, text='class_setting', state=None)
    dp.register_callback_query_handler(
        setting_username, text='username_setting', state=None)
    dp.register_callback_query_handler(
        cancel_setting, text='cancel_setting', state='*')
    dp.register_callback_query_handler(
        new_number_class, state=FSMChange_class.number_class)
    dp.register_message_handler(
        new_username, state=FSMChange_username.username)
