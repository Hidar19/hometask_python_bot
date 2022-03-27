from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize
import json

buttons_start_menu = [emojize(':books: Домашнее задание'),
                      emojize(':thinking_face: Куда я попал?'),
                      emojize(':gear: Настройки')]


class StudentKeyboards():
    def student_start_menu(distant):
        keyboard_start_menu_student = ReplyKeyboardMarkup(resize_keyboard=True,
                                                          row_width=2,
                                                          one_time_keyboard=True)
        keyboard_start_menu_student.add(*buttons_start_menu)
        if distant is True:
            keyboard_start_menu_student.add(KeyboardButton(emojize(':man_student: Посмотреть задания на сегодня')))
            keyboard_start_menu_student.add(KeyboardButton(emojize(':package: Отправить задание')))
        return keyboard_start_menu_student

    def keyboard_setting():
        setting_menu = InlineKeyboardMarkup(resize_keyboard=True,
                                            row_width=1)
        setting_menu.add(*[InlineKeyboardButton('Поменять класс', callback_data='class_setting'),
                           InlineKeyboardButton('Изменить обращение', callback_data='username_setting'),
                           InlineKeyboardButton(emojize(':house: В главное меню'), callback_data='cancel_other')])
        return setting_menu

    def dist_task_send_subject(subject):
        keyboard_dist_task_subject = InlineKeyboardMarkup(resize_keyboard=True,
                                                          row_width=2)
        for i in subject:
            keyboard_dist_task_subject.add(
                InlineKeyboardButton(f'{i[0]}', callback_data=f'{i[0]}'))
        keyboard_dist_task_subject.add(InlineKeyboardButton(
            emojize(':house: В главное меню'), callback_data='cancel_other'))
        return keyboard_dist_task_subject

    def send_media():
        keyboard_dist_task_mediaGroup = ReplyKeyboardMarkup(resize_keyboard=True,
                                                            row_width=1)
        keyboard_dist_task_mediaGroup.add(KeyboardButton('Дальше'))
        keyboard_dist_task_mediaGroup.add(KeyboardButton(emojize(':house: В главное меню')))
        return keyboard_dist_task_mediaGroup


class TeacherKeyboards():
    def start_menu_admin(distant):
        keyboard_start_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True,
                                                        row_width=2,
                                                        one_time_keyboard=True).add(*buttons_start_menu)
        keyboard_start_menu_admin.add(
            KeyboardButton('Меню главного модератора'))
        if distant is True:
            keyboard_start_menu_admin.add(KeyboardButton(emojize(':man_student: Посмотреть задания на сегодня')))
            keyboard_start_menu_admin.add(KeyboardButton(emojize(':package: Отправить задание')))
        return keyboard_start_menu_admin

    def start_menu_teacher(distant):
        keyboard_start_menu_teacher = ReplyKeyboardMarkup(resize_keyboard=True, 
                                                          row_width=2,
                                                          one_time_keyboard=True).add(*buttons_start_menu)
        keyboard_start_menu_teacher.add(KeyboardButton('Меню учителя'))
        if distant is True:
            keyboard_start_menu_teacher.add(KeyboardButton(emojize(':man_student: Посмотреть задания на сегодня')))
            keyboard_start_menu_teacher.add(KeyboardButton(emojize(':package: Отправить задание')))
        return keyboard_start_menu_teacher

    def king_admin_keyboard_generate(distant):
        buttons_king_admin_keyboard = [InlineKeyboardButton('Добавить учителя', callback_data='add_teacher'), 
                                       InlineKeyboardButton('Удалить учителя', callback_data='del_teacher'),
                                       InlineKeyboardButton('Добавить д/з', callback_data='add_homework'), 
                                       InlineKeyboardButton('Удалить д/з', callback_data='del_homework'),
                                       InlineKeyboardButton('Начать новый учебный год', callback_data='new_year')]
        king_admin_keyboard = InlineKeyboardMarkup(resize_keyboard=True,
                                                   row_width=2)
        king_admin_keyboard.add(*buttons_king_admin_keyboard)
        if distant is True:
            king_admin_keyboard.add(InlineKeyboardButton('Добавить дист.задание', callback_data='add_dist_task'))
            king_admin_keyboard.add(InlineKeyboardButton('Удалить дист.задание', callback_data='del_dist_task'))
            king_admin_keyboard.add(InlineKeyboardButton('Завершить режим дист.образования', callback_data='close_distant'))
        else:
            king_admin_keyboard.add(InlineKeyboardButton('Активировать режим дист.образования', callback_data='open_distant'))
        king_admin_keyboard.add(InlineKeyboardButton(emojize(':house: В главное меню'), callback_data='cancel_other'))
        return king_admin_keyboard

    def cofirmation():
        keyboard_agree_new_year = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard_agree_new_year.add(*[InlineKeyboardButton(emojize(':check_mark_button: Да, все верно'), callback_data='agree'),
                                      InlineKeyboardButton('Отмена', callback_data='cancel_menu')])
        return keyboard_agree_new_year

    def teacher_keyboard_generate(distant):
        buttons_teacher_keyboard = [InlineKeyboardButton('Добавить д/з', callback_data='add_homework'),
                                    InlineKeyboardButton('Удалить д/з', callback_data='del_homework')]
        teacher_keyboard = InlineKeyboardMarkup(resize_keyboard=True, 
                                                row_width=2)
        teacher_keyboard.add(*buttons_teacher_keyboard)
        teacher_keyboard.add(InlineKeyboardButton(emojize(':house: В главное меню'), callback_data='cancel_other'))
        if distant is True:
            teacher_keyboard.add(InlineKeyboardButton('Добавить дист.задание', callback_data='add_dist_task'))
            teacher_keyboard.add(InlineKeyboardButton('Удалить дист.задание', callback_data='del_dist_task'))
        return teacher_keyboard

    def keyboard_subject_generate(number_class):
        keyboard_subject = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        with open('subject.json', 'r') as f_subject:
            subject = json.load(f_subject)
        for i in subject['class' + str(number_class)]:
            keyboard_subject.insert(InlineKeyboardButton(i, callback_data=i))
        keyboard_subject.add(InlineKeyboardButton('Отмена', callback_data='cancel_menu'))
        return keyboard_subject


class OtherKeyboards():
    def keyboard_help_menu():
        buttons_help = [InlineKeyboardButton('Показать команды', callback_data='show_commands'),
                        InlineKeyboardButton(emojize(':house: В главное меню'), callback_data='cancel_other')]
        keyboard_help = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard_help.add(*buttons_help)
        return keyboard_help

    def keyboard_class_generate(classes):
        keyboard_class = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        for i in classes:
            keyboard_class.insert(InlineKeyboardButton(f'{i} класс', callback_data=f'{i}'))
        return keyboard_class
