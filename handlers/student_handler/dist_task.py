from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputMediaDocument, InputMediaPhoto, InputMediaVideo
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from emoji import emojize

from config import bot, cur
from config import distant

from keyboard import StudentKeyboards
from keyboard_cancel import keyboard_student_cancel

from handlers.student_handler import homework
from handlers import student


class FSMSend_Dist_Task(StatesGroup):
    subject = State()
    name = State()
    MediaGroup = State()


async def dist_task_show(message: Message):
    if distant is True:
        class_person = cur.execute(
            "SELECT class, first_name FROM users WHERE user_id = ?", (message.from_user.id,)).fetchall()
        if len(class_person) == 0:
            await homework.homework_show(message, state=None)
            return
        dist_task = cur.execute(
            "SELECT subject, description FROM dist_task WHERE class = ?", (class_person[0][0],)).fetchall()
        if len(dist_task) > 0:
            out_string = [
                f'С возвращением, {class_person[0][1]}.\nСмотри что мне удалось для тебя раздобыть\n']
            for i in dist_task:
                out_string.append(f'{i[0]}: {i[1]}')
            await message.answer('\n'.join(out_string), reply_markup=keyboard_student_cancel)
        else:
            await message.answer('Здесь ничего нет', reply_markup=keyboard_student_cancel)


async def cancel_dist_task(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if distant is True:
        class_person = cur.execute(
            "SELECT class, first_name FROM users WHERE user_id = ?", (call.from_user.id,)).fetchall()
        if len(class_person) == 0:
            await homework.homework_show(call, state=None)
            return
        dist_task = cur.execute(
            "SELECT subject, description FROM dist_task WHERE class = ?", (class_dist_task[0][0],)).fetchall()
        if len(dist_task) > 0:
            out_string = [
                f'С возвращением, {class_person[0][1]}.\nСмотри что мне удалось для тебя раздобыть\n']
            for i in dist_task:
                out_string.append(f'{i[0]}: {i[1]}')
            await call.message.answer('\n'.join(out_string), reply_markup=keyboard_student_cancel)
        else:
            await call.message.answer('Здесь ничего нет', reply_markup=keyboard_student_cancel)
#######################################################################################################################################


async def dist_task_send(message: Message, state: FSMContext):
    if distant is True:
        global class_person
        class_person = cur.execute(
            "SELECT class, first_name FROM users WHERE user_id = ?", (message.from_user.id,)).fetchall()
        if len(class_person) == 0:
            await homework.homework_show(message, state=None)
            return
        subject = cur.execute(
            "SELECT subject FROM dist_task WHERE class = ?", (class_person[0][0],)).fetchall()
        if len(subject) > 0:
            await message.answer(f'Привет, {class_person[0][1]}.\nВыбери по какому предмету ты сделал задание', 
                                reply_markup=StudentKeyboard.dist_task_send_subject(subject))
            await FSMSend_Dist_Task.subject.set()
        else:
            await message.answer('Здесь ничего нет', reply_markup=keyboard_student_cancel)


async def subject_set(call: CallbackQuery, state: FSMContext):
    if distant is True:
        class_person = cur.execute(
            "SELECT class, first_name FROM users WHERE user_id = ?", (call.from_user.id,)).fetchall()
        if len(class_person) == 0:
            await homework.homework_show(call, state=None)
            await state.finish()
            return
        global mediaGroup
        mediaGroup = []
        try:
            global subject_dist_task_send
            subject_dist_task_send = call.data
            await FSMSend_Dist_Task.next()
            await call.message.answer('Чтобы продолжить напиши мне свое имя и фамилию (учти что оно будет видно учителю)', reply_markup=keyboard_student_cancel)
            await bot.answer_callback_query(call.id)
        except:
            await call.answer('Чтобы продолжить напиши мне свое имя и фамилию (учти что оно будет видно учителю)', reply_markup=keyboard_student_cancel)


async def name_set(message: Message, state: FSMContext):
    global name
    await message.answer('Чтобы продолжить пришли мне свое решение в виде одного или группы файлов и нажми на кнопку "Дальше"', 
                         reply_markup=StudentKeyboard.send_media())
    if message.text == 'Дальше':
        return
    name = message.text
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
    if distant is True:
        if len(mediaGroup) > 0:
            await bot.send_media_group(cur.execute('SELECT adress FROM dist_task WHERE subject=? AND class=?', (subject_dist_task_send, class_person[0][0])).fetchall()[0][0],
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
