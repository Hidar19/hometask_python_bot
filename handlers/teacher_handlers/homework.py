from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import json

from config import conn, cur, bot

from keyboards.keyboard import OtherKeyboards
from keyboards.keyboard import TeacherKeyboards
from keyboards.keyboard_cancel import keyboard_teacher_cancel

from get_info import *

from handlers import teacher


class FSMAdd_Homework(StatesGroup):
    number_class = State()
    subject = State()
    description = State()


class FSMDel_Homework(StatesGroup):
    number_class = State()
    subject = State()


async def add_homework(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if check_admin(call.from_user.username) is True:
        await set_class(call)
        await FSMAdd_Homework.number_class.set()


async def add_number_class(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    global number_class
    number_class = call.data
    await set_subject(call)
    await FSMAdd_Homework.next()


async def add_subject(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    global subject
    subject = call.data
    await FSMAdd_Homework.next()
    await call.message.edit_text('Введите описание', reply_markup=keyboard_teacher_cancel)


async def add_description(message: Message, state: FSMContext):
    description = message.text
    if get_hometask(number_class) is None:
        cur.execute("""INSERT INTO homework(class, subject, description) VALUES(?, ?, ?);""",
                    (number_class, subject, description))
        conn.commit()
    else:
        cur.execute("""UPDATE homework SET description=? WHERE class = ? AND subject = ?;""",
                    (description, number_class, subject))
        conn.commit()
    await state.finish()
    for i in get_users_for_send(number_class):
        await bot.send_message(i[0],
                               f'Я узнал еще одно домашнее задание по предмету {subject}!\n'
                               + 'Проверьте домашнее задание командой /homework')
    if message.from_user.id == KING_ID:
        await teacher.king_admin_menu(message)
    else:
        await teacher.teacher_menu(message)


async def del_homework(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if check_admin(call.from_user.username) is True:
        await set_class(call)
        await FSMDel_Homework.number_class.set()


async def del_class_DelHomework(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    global number_class
    number_class = call.data
    await set_subject(call)
    await FSMDel_Homework.next()


async def del_subject_DelHomework(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    subject = call.data
    if get_hometask(number_class) is not None:
        cur.execute("DELETE FROM homework WHERE class=? AND subject=?",
                    (number_class, subject,))
        conn.commit()
    await teacher.cancel_menu(call, state)


async def set_class(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    with open('classes.json', 'r') as f:
        await call.message.edit_text('Выберите номер класса',
                                     reply_markup=OtherKeyboards.keyboard_class_generate(json.load(f)))


async def set_subject(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text('Выберите предмет',
                                 reply_markup=TeacherKeyboards.keyboard_subject_generate(number_class))


def homework_teacher_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_homework, text='add_homework', state=None)
    dp.register_callback_query_handler(
        add_number_class, state=FSMAdd_Homework.number_class)
    dp.register_callback_query_handler(
        add_subject, state=FSMAdd_Homework.subject)
    dp.register_message_handler(
        add_description, state=FSMAdd_Homework.description)

    dp.register_callback_query_handler(
        del_homework, text='del_homework', state=None)
    dp.register_callback_query_handler(
        del_class_DelHomework, state=FSMDel_Homework.number_class)
    dp.register_callback_query_handler(
        del_subject_DelHomework, state=FSMDel_Homework.subject)
