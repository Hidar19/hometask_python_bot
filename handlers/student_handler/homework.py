from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from emoji import emojize
import json

from config import bot, conn, cur

from keyboards.keyboard import OtherKeyboards
from keyboards.keyboard_cancel import keyboard_student_cancel

from get_info import *


class FSMClass(StatesGroup):
    number_class = State()


async def homework_show(message: Message, state: FSMContext):
    person = get_person(message.from_user.id)
    if person is None:
        await FSMClass.number_class.set()
        with open('classes.json', 'r') as f:
            await message.answer('Кажется ты тут новенький...Ну что ж, добро пожаловать! Выбери свой класс',
                                 reply_markup=OtherKeyboards.keyboard_class_generate(json.load(f)))
    else:
        hometask = get_hometask(person[0])
        if hometask is not None:
            out_string = [
                f'С возвращением, {person[1]}.\nСмотри что мне удалось для тебя раздобыть\n']
            for i in hometask:
                out_string.append(f'{i[0]}: {i[1]}')
            await message.answer('\n'.join(out_string), reply_markup=keyboard_student_cancel)
        else:
            await message.answer('Здесь ничего нет', reply_markup=keyboard_student_cancel)


async def add_class(call: CallbackQuery, state: FSMContext):
    cur.execute("INSERT INTO users(user_id, class, first_name) VALUES(?, ?, ?);",
                (call.from_user.id, call.data, call.from_user.first_name))
    conn.commit()
    await call.message.edit_text('Отлично! Теперь у тебя есть класс', reply_markup=keyboard_student_cancel)
    await state.finish()


async def cancel_homework(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await homework_show(call.message)


def homework_handlers(dp: Dispatcher):
    dp.register_message_handler(homework_show, Text(
        equals=emojize(':books: Домашнее задание')), state=None)
    dp.register_message_handler(homework_show, commands='homework', state=None)
    dp.register_callback_query_handler(add_class, state=FSMClass.number_class)
    dp.register_callback_query_handler(
        cancel_homework, text='cancel_menu_homework', state='*')
