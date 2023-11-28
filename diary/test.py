import asyncio

from db.services.users import get_user

from diary.api.deeduorb import DeEduOrb
from diary.config import db_session
from diary.services.time import parse_date

user = get_user(db_session, 1122659029)
date = parse_date("20.11.2023")

d = DeEduOrb(user)
diary = asyncio.run(d.get_diary(date=date))
for i in diary:
    lesson = diary[i][0]
    print(lesson.date)
    print()
