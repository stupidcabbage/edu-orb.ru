import asyncio
from datetime import datetime

from db.services.users import get_user

from diary.api.deeduorb import DeEduOrb
from diary.api.request import EduOrbRequest, Period
from diary.config import db_session

user = get_user(db_session, 1122659029)
date = datetime.today()

period = Period(date, date)
request = asyncio.run(EduOrbRequest(user).get_marks_table(period))
print(request)

