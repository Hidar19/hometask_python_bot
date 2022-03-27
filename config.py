from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

storage = MemoryStorage()
bot = Bot(token='5016310335:AAEEIVhssfl4ZuTrwGJWKsVQl-1WlZAyVB4',
          parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
KING_ID = 1258778423  # MAIN_ADMIN_ID
conn = sqlite3.connect('school.db')
cur = conn.cursor()
distant = False
