from typing import List
from config import KING_ID, cur


def check_admin(username: str) -> bool:
    if len(cur.execute("SELECT * FROM admin WHERE tgname = ?", (username,)).fetchall()) == 0:
        return False
    else:
        return True


def get_person(user_id: int) -> List:
    person = cur.execute(
        "SELECT class, first_name FROM users WHERE user_id = ?", (user_id,)).fetchall()
    # (id, user_id, class, name)
    if len(person) == 0:
        return None
    else:
        return person[0]


def get_dist_task(number_class: str) -> List:
    dist_task = cur.execute(
        "SELECT subject, description FROM dist_task WHERE class = ?", (number_class,)).fetchall()
    if len(dist_task) == 0:
        return None
    else:
        return dist_task


def get_adress_dist_task(number_class: str, subject: str) -> int:
    return cur.execute('SELECT adress FROM dist_task WHERE subject=? AND class=?', (subject, number_class)).fetchall()[0][0]


def get_hometask(number_class: str) -> List:
    hometask = cur.execute(
        "SELECT subject, description FROM homework WHERE class = ?", (number_class,)).fetchall()
    if len(hometask) == 0:
        return None
    else:
        return hometask


def get_users_for_send(number_class: str) -> List:
    return cur.execute("SELECT user_id FROM users WHERE class = ?;", (number_class,)).fetchall()
