import asyncio

from db.services.users import get_user

from diary.api.deeduorb import DeEduOrb
from diary.config import db_session
from diary.services.time import parse_date

user = get_user(db_session, 1122659029)
date = parse_date("21.11.2023")

d = DeEduOrb(user)
diary = asyncio.run(d.get_day_diary(date=date))
for i in diary:
    lesson = i
    print(lesson)
    print()


def make_something_cool(message: str) -> str:
    return 1


make_something_cool(123)
