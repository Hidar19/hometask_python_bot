from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

storage = MemoryStorage()
bot = Bot(token='YOUR_TOKEN_BOT',
          parse_mode=ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
KING_ID = # MAIN_ADMIN_ID
conn = sqlite3.connect('school.db')
cur = conn.cursor()
distant = False
