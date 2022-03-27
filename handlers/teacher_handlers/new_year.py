from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import json

from config import dp, conn, cur, bot, KING_ID

from keyboard import TeacherKeyboards
from keyboard_cancel import keyboard_teacher_cancel


class FSMNew_Year(StatesGroup):
    character = State()
    agree = State()
    
async def new_year(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    if call.from_user.id == king_id:
        await call.message.edit_text('Отлично! Теперь напишите последнюю букву 1 класса в формате: <i>в</i>.\nЕсли 1 класс только один напишите а\nЕсли есть 1е класс свяжитесь с разработчиком(@Hidar82)', reply_markup=keyboard_teacher_cancel)
        await FSMNew_Year.character.set()
        
async def character_NewYear(message: Message, state: FSMContext):
    character = list(message.text)
    global rus_alphabet
    rus_alphabet = 'абвгд'
    if len(character) > 1:
        await message.answer('Пожалуйста, введите одну русскую прописную букву. Например: <i>в</i>', reply_markup=keyboard_teacher_cancel)
        return
    elif len(character) == 1:
        if character[0] in rus_alphabet:
            pass
        else:
            await message.answer('Пожалуйста, введите одну русскую прописную букву. Например: <i>в</i>', reply_markup=keyboard_teacher_cancel)
            return
    global new_classes        
    new_classes = []
    if character[0] == 'а':
        new_classes.append('1')
    else:
        for i in list(rus_alphabet)[:list(rus_alphabet).index(character[0])+1]:
            new_classes.append('1'+i)
    await message.answer(f'''В новый учебный год вступают: \n{', '.join(new_classes)} классы
После завершения действия все классы будут смещены на 1''', reply_markup=TeacherKeyboards.keyboard_agree_new_year)
    await FSMNew_Year.next()
    
async def agree_NewYear(call: CallbackQuery, state: FSMContext):
    cur.execute("DELETE FROM homework")
    cur.execute("DELETE FROM dist_task")
    cur.execute("DELETE FROM users WHERE class=?", ('11',))
    for i in list(rus_alphabet):
        cur.execute("DELETE FROM users WHERE class=?", ('11'+i,))
    for i in cur.execute("SELECT class, user_id FROM users").fetchall():
        if i[0][:2] == '10':
            if i[0][1:] in rus_alphabet:
                cur.execute("UPDATE users SET class=? WHERE user_id=?", ('11'+i[0][1:], i[1]))
            else:
                cur.execute("UPDATE users SET class=? WHERE user_id=?", ('11', i[1]))
        else:
            if i[0][1:] in rus_alphabet: 
                cur.execute("UPDATE users SET class=? WHERE user_id=?", (str(int(i[0][0])+1)+i[0][1:], i[1]))
            else:
                cur.execute("UPDATE users SET class=? WHERE user_id=?", (int(i[0][0])+1, i[1]))
    conn.commit()
    with open('classes.json', 'r') as f:
        previous_classes = json.load(f)
        for i in previous_classes:
            if i[:2] == '10':
                if i[-1] in rus_alphabet:
                    new_classes.append('11' + i[-1])
                else:
                    new_classes.append('11')
            elif i[:2] == '11':
                pass
            else:
                if i[-1] in rus_alphabet:
                    new_classes.append(str(int(i[0])+1) + i[-1])
                else:
                    new_classes.append(str(int(i[0])+1))
    with open('classes.json', 'w') as f:
        json.dump(new_classes, f)
    await cancel_menu(call, state)
    
def new_year_teacher_handlers(dp : Dispatcher):
    dp.register_callback_query_handler(new_year, text='new_year', state = None)
    dp.register_callback_query_handler(agree_NewYear, state = FSMNew_Year.agree)
    dp.register_message_handler(character_NewYear, state = FSMNew_Year.character)
    