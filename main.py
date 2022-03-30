from aiogram import executor
from config import dp
from handlers import student, teacher
import logging

teacher.admin_handlers(dp)
student.client_handlers(dp)
logging.basicConfig(level=logging.ERROR,
                    filename='errors.txt',
                    filemode='w')

autograph = r"""
||      ||  =||=   ||\\         /\\         ||\ \
||      ||   ||    || \\       /  \\        || \ \
||______||   ||    ||  \\     /    \\       || / /
||======||   ||    ||   ||   /______\\      ||/_/
||      ||   ||    ||  //   /========\\     ||  |
||      ||   ||    || //   /          \\    ||   \
||      ||  =||=   ||//   /            \\   ||    |_
"""
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False,
                           on_startup=print(autograph))
