from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from emoji import emojize

from config import distant
from config import KING_ID, bot, conn, cur

from keyboard import StudentKeyboards
from keyboard import TeacherKeyboards
from keyboard import OtherKeyboards
from keyboard_cancel import keyboard_student_cancel

from handlers.student_handler import homework, setting_user, dist_task

async def start(message: Message, state: FSMContext):
    await state.finish()
    if len(cur.execute("SELECT * FROM admin WHERE tgname = ?", (message.from_user.username,)).fetchall()) == 0 and message.from_user.id == KING_ID:
        cur.execute("INSERT INTO admin(tgname) VALUES(?);",
                    (message.from_user.username,))
        conn.commit()
    if len(cur.execute("SELECT * FROM admin WHERE tgname = ?", (message.from_user.username,)).fetchall()) > 0:
        if message.from_user.id == KING_ID:
            await message.answer('Вы главный модератор. Добро пожаловать!', reply_markup=TeacherKeyboards.start_menu_admin(distant))
        else:
            await message.answer('Вы учитель. Добро пожаловать!', reply_markup=TeacherKeyboards.start_menu_teacher(distant))
    else:
        await message.answer('Добро пожаловать!', reply_markup=StudentKeyboards.student_start_menu(distant))


async def main_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.answer_callback_query(call.id)
    if len(cur.execute("SELECT id FROM admin WHERE tgname = ?", (call.from_user.username,)).fetchall()) > 0:
        if call.from_user.id == KING_ID:
            await call.message.answer('Главное меню:', reply_markup=TeacherKeyboards.start_menu_admin(distant))
        else:
            await call.message.answer('Главное меню:', reply_markup=TeacherKeyboards.start_menu_teacher(distant))
    else:
        await call.message.answer('Главное меню:', reply_markup=StudentKeyboards.student_start_menu(distant))


async def helper(message: Message):
    await message.answer('''
Привет! Ты попал в телеграмм бота нашей школы.
Чтобы посмотреть больше жми на кнопку''', reply_markup=OtherKeyboards.keyboard_help_menu())


async def commands(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if call.from_user.id == KING_ID:
        await call.message.edit_text('''<b>Команды главного администратора:</b>
/menu_admin - Меню администратора
/menu_teacher - Меню учителя
/homework - Посмотреть домашнее задание для своего класса
/setting - Настройки пользователя
/help - Помощь
/start - Главное меню''', reply_markup=keyboard_student_cancel)
    else:
        await call.message.edit_text('''<b>Команды для вас:</b>
/homework - Посмотреть домашнее задание для своего класса
/setting - Настройки пользователя
/help - Помощь
/start - Главное меню''', reply_markup=keyboard_student_cancel)

def client_handlers(dp: Dispatcher):
    homework.homework_handlers(dp)
    dist_task.dist_task_handlers(dp)
    setting_user.setting_handlers(dp)
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(start, text=emojize(
        ':house: В главное меню'), state='*')
    dp.register_callback_query_handler(
        main_menu, text='cancel_other', state='*')
    dp.register_message_handler(helper, Text(
        equals=emojize(':thinking_face: Куда я попал?')))
    dp.register_message_handler(helper, commands='help')
    dp.register_callback_query_handler(commands, text='show_commands')
