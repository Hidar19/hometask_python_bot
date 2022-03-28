from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from config import KING_ID, conn, cur, bot
from config import distant

from keyboards.keyboard import TeacherKeyboards

from keyboards.keyboard_cancel import keyboard_teacher_cancel

from handlers.teacher_handlers import homework, dist_task, new_year


class FSMAdd_Teacher(StatesGroup):
    username = State()


class FSMDel_Teacher(StatesGroup):
    username = State()


async def king_admin_menu(message: Message):
    if message.from_user.id == KING_ID:
        try:
            await message.answer('Что вы хотите сделать?', reply_markup=TeacherKeyboards.king_admin_keyboard_generate(distant))
        except TypeError:
            await message.message.edit_text('Что вы хотите сделать?', reply_markup=TeacherKeyboards.king_admin_keyboard_generate(distant))


async def teacher_menu(message: Message):
    try:
        await message.answer('Что вы хотите сделать?', reply_markup=TeacherKeyboards.teacher_keyboard_generate(distant))
    except TypeError:
        await message.message.edit_text('Что вы хотите сделать?', reply_markup=TeacherKeyboards.teacher_keyboard_generate(distant))


async def cancel_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.answer_callback_query(call.id)
    if call.from_user.id == KING_ID:
        await king_admin_menu(call)
    else:
        await teacher_menu(call)


async def invers_distant(call: CallbackQuery):
    global distant
    if call.data == 'open_distant':
        distant = True
    else:
        distant = False
    await bot.answer_callback_query(call.id)
    await king_admin_menu(call)

###################################################################################################################################################################################################################################################


async def add_teacher(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if call.from_user.id == KING_ID:
        await FSMAdd_Teacher.username.set()
        await call.message.edit_text('Введите никнейм нового учителя в формате: <i>username</i>', reply_markup=keyboard_teacher_cancel)


async def add_username_newTeacher(message: Message, state: FSMContext):
    cur.execute("""INSERT INTO admin(tgname) VALUES(?);""", (message.text,))
    conn.commit()
    await state.finish()
    await message.answer('Список модераторов был обновлен')
    await king_admin_menu(message)
########################################################################################################################################################


async def del_teacher(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if call.from_user.id == KING_ID:
        await FSMDel_Teacher.username.set()
        await call.message.edit_text('Введите никнейм модератора которого хотите удалить в формате: <i>username</i>', reply_markup=keyboard_teacher_cancel)


async def add_username_delTeacher(message: Message, state: FSMContext):
    cur.execute("""DELETE FROM admin WHERE tgname=?""", (message.text,))
    conn.commit()
    await state.finish()
    await message.answer('Список модераторов был обновлен')
    await king_admin_menu(message)
##########################################################################################################################################################


def admin_handlers(dp: Dispatcher):
    homework.homework_teacher_handlers(dp)
    dist_task.dist_task_teacher_handlers(dp)
    new_year.new_year_teacher_handlers(dp)
    dp.register_message_handler(king_admin_menu, Text(
        equals="Меню главного модератора"))
    dp.register_message_handler(king_admin_menu, commands='menu_admin')
    dp.register_message_handler(teacher_menu, Text(equals="Меню учителя"))
    dp.register_message_handler(teacher_menu, commands='menu_teacher')
    dp.register_callback_query_handler(
        cancel_menu, text='cancel_menu', state='*')

    dp.register_callback_query_handler(invers_distant, text='open_distant')
    dp.register_callback_query_handler(invers_distant, text='close_distant')

    dp.register_callback_query_handler(
        add_teacher, text='add_teacher', state=None)
    dp.register_message_handler(
        add_username_newTeacher, state=FSMAdd_Teacher.username)

    dp.register_callback_query_handler(
        del_teacher, text='del_teacher', state=None)
    dp.register_message_handler(
        add_username_delTeacher, state=FSMDel_Teacher.username)
