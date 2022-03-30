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


class FSMAdd_Dist_Task(StatesGroup):
    number_class = State()
    subject = State()
    description = State()


class FSMDel_Dist_Task(StatesGroup):
    number_class = State()
    subject = State()


async def add_dist_task(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    if teacher.distant is True:
        if check_admin(call.from_user.username) is True:
            await set_class(call)
            await FSMAdd_Dist_Task.number_class.set()
    else:
        await teacher.cancel_menu(call, state)


async def add_number_class(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    global number_class
    number_class = call.data
    await set_subject(call)
    await FSMAdd_Dist_Task.next()


async def add_subject(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    global subject
    subject = call.data
    await FSMAdd_Dist_Task.next()
    await call.message.edit_text('Введите описание', reply_markup=keyboard_teacher_cancel)


async def add_description(message: Message, state: FSMContext):
    description = message.text
    if get_dist_task(number_class) is None:
        cur.execute("""INSERT INTO dist_task(class, subject, description, adress) VALUES(?, ?, ?, ?);""",
                    (number_class, subject, description, message.from_user.id))
        conn.commit()
    else:
        cur.execute("""UPDATE dist_task SET description=? WHERE class = ? AND subject = ?;""",
                    (description, number_class, subject))
        cur.execute("""UPDATE dist_task SET adress=? WHERE class = ? AND subject = ?;""",
                    (message.from_user.id, number_class, subject))
        conn.commit()
    await state.finish()
    for i in get_users_for_send(number_class):
        await bot.send_message(i[0],
                               f'Я узнал еще одно задание дистанта по предмету {subject}!\n' +
                               'Проверьте задания дистанционного обучения командой /dist_task')
    await message.answer('Решения этого задания придут в этот чат')
    if message.from_user.id == KING_ID:
        await teacher.king_admin_menu(message)
    else:
        await teacher.teacher_menu(message)


async def del_dist_task(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    if teacher.distant is True:
        if check_admin(call.from_user.username) is True:
            await set_class(call)
            await FSMDel_Dist_Task.number_class.set()
    else:
        await teacher.cancel_menu(call, state)


async def del_class_DelDist_task(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    global number_class
    number_class = call.data
    await set_subject(call)
    await FSMDel_Dist_Task.next()


async def del_subject_DelDist_task(call: CallbackQuery, state: FSMContext):
    if call.data == 'cancel_menu':
        await teacher.cancel_menu(call, state)
        return
    subject = call.data
    if get_dist_task(number_class) is not None:
        cur.execute("DELETE FROM dist_task WHERE class=? AND subject=?",
                    (number_class, subject,))
        conn.commit()
    await teacher.cancel_menu(call, state)


async def set_class(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    with open('classes.json', 'r') as f:
        await call.message.edit_text('Выберите номер класса', reply_markup=OtherKeyboards.keyboard_class_generate(json.load(f)))


async def set_subject(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text('Выберите предмет', reply_markup=TeacherKeyboards.keyboard_subject_generate(number_class))


def dist_task_teacher_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_dist_task, text='add_dist_task', state=None)
    dp.register_callback_query_handler(
        add_number_class, state=FSMAdd_Dist_Task.number_class)
    dp.register_callback_query_handler(
        add_subject, state=FSMAdd_Dist_Task.subject)
    dp.register_message_handler(
        add_description, state=FSMAdd_Dist_Task.description)

    dp.register_callback_query_handler(
        del_dist_task, text='del_dist_task', state=None)
    dp.register_callback_query_handler(
        del_class_DelDist_task, state=FSMDel_Dist_Task.number_class)
    dp.register_callback_query_handler(
        del_subject_DelDist_task, state=FSMDel_Dist_Task.subject)
