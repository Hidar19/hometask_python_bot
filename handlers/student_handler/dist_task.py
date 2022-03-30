from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputMediaDocument, InputMediaPhoto, InputMediaVideo
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from emoji import emojize

from config import bot, cur

from keyboards.keyboard import StudentKeyboards
from keyboards.keyboard_cancel import keyboard_student_cancel

from get_info import *

from handlers.student_handler import homework
from handlers import student
from handlers.teacher import distant


class FSMSend_Dist_Task(StatesGroup):
    subject = State()
    name = State()
    MediaGroup = State()


async def dist_task_show(message: Message):
    if distant is True:
        person = get_person(message.from_user.id)
        if person is None:
            await homework.homework_show(message, state=None)
            return
        dist_task = get_dist_task(person[0])
        if dist_task is not None:
            out_string = [
                f'С возвращением, {person[1]}.\nСмотри что мне удалось для тебя раздобыть\n']
            for i in dist_task:
                out_string.append(f'{i[0]}: {i[1]}')
            await message.answer('\n'.join(out_string), reply_markup=keyboard_student_cancel)
        else:
            await message.answer('Здесь ничего нет', reply_markup=keyboard_student_cancel)


async def cancel_dist_task(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if distant is True:
        person = get_person(call.from_user.id)
        if person is None:
            await homework.homework_show(call, state=None)
            return
        dist_task = get_dist_task(person[0])
        if dist_task is not None:
            out_string = [
                f'С возвращением, {person[1]}.\nСмотри что мне удалось для тебя раздобыть\n']
            for i in dist_task:
                out_string.append(f'{i[0]}: {i[1]}')
            await call.message.answer('\n'.join(out_string), reply_markup=keyboard_student_cancel)
        else:
            await call.message.answer('Здесь ничего нет', reply_markup=keyboard_student_cancel)


async def dist_task_send(message: Message, state: FSMContext):
    if distant is True:
        person = get_person(message.from_user.id)
        if person is None:
            await homework.homework_show(message, state=None)
            return
        try:
            subject = get_dist_task(person[0])
            await message.answer(f'Привет, {person[1]}.\nВыбери по какому предмету ты сделал задание',
                                 reply_markup=StudentKeyboards.dist_task_send_subject(subject))
            await FSMSend_Dist_Task.subject.set()
        except TypeError:
            await message.answer('Здесь ничего нет', reply_markup=keyboard_student_cancel)


async def subject_set(call: CallbackQuery, state: FSMContext):
    if distant is True:
        person = get_person(call.from_user.id)
        if person is None:
            await homework.homework_show(call, state=None)
            await state.finish()
            return
        try:
            global subject
            subject = call.data
            await FSMSend_Dist_Task.next()
            await call.message.answer('Чтобы продолжить напиши мне свое имя и фамилию (учти что оно будет видно учителю)', reply_markup=keyboard_student_cancel)
            await bot.answer_callback_query(call.id)
        except Exception:
            await call.answer('Чтобы продолжить напиши мне свое имя и фамилию (учти что оно будет видно учителю)', reply_markup=keyboard_student_cancel)
        global mediaGroup
        mediaGroup = []


async def name_set(message: Message, state: FSMContext):
    global name
    name = message.text
    await message.answer('Чтобы продолжить пришли мне свое решение в виде одного или группы файлов и нажми на кнопку "Дальше"',
                         reply_markup=StudentKeyboards.send_media())
    if message.text == 'Дальше':
        return
    await FSMSend_Dist_Task.next()


async def media_group_set(message: Message, state: FSMContext):
    global mediaGroup
    try:
        file = message.photo.pop().file_id
        mediaGroup.append(InputMediaPhoto(file, caption=name))
    except IndexError:
        try:
            file = message.video.file_id
            mediaGroup.append(InputMediaVideo(file, caption=name))
        except AttributeError:
            file = message.document.file_id
            mediaGroup.append(InputMediaDocument(file, caption=name))


async def finish_state(message: Message, state: FSMContext):
    person = get_person(message.from_user.id)
    if distant is True:
        if len(mediaGroup) > 0:
            await bot.send_media_group(get_adress_dist_task(person[0], subject),
                                       mediaGroup)
            await student.start(message, state)
        else:
            await name_set(message, state)
    else:
        await state.finish()
        await student.start(message)


def dist_task_handlers(dp: Dispatcher):
    dp.register_message_handler(dist_task_show, Text(
        equals=emojize(':man_student: Посмотреть задания на сегодня')))
    dp.register_message_handler(dist_task_show, commands='dist_task')
    dp.register_callback_query_handler(
        cancel_dist_task, text='cancel_menu_dist_task')
    dp.register_message_handler(dist_task_send, Text(
        equals=emojize(':package: Отправить задание')), state=None)
    dp.register_callback_query_handler(
        subject_set, state=FSMSend_Dist_Task.subject)
    dp.register_message_handler(name_set, state=FSMSend_Dist_Task.name)
    dp.register_message_handler(media_group_set, content_types=['photo', 'video', 'document'],
                                state=FSMSend_Dist_Task.MediaGroup)
    dp.register_message_handler(finish_state, Text(
        equals='Дальше'), state=FSMSend_Dist_Task.MediaGroup)
