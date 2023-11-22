from diary.api.new_diary import EduOrbDiary
from diary.config import db_session
from db.services.users import get_user
from diary.services.time import parse_date
import asyncio
user = get_user(db_session, 1122659029)
date = parse_date("20.11.2023")

d = EduOrbDiary(user)
diary = asyncio.run(d.get_diary(date))
print(diary)
