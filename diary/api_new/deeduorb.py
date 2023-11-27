import asyncio
import datetime
from typing import NamedTuple

from diary.api_new.handlers import exception_token_handler
from diary.api_new.request import EduOrbRequest
from diary.config import db_session
from diary.db.models.users import User
from diary.db.services.users import get_user

WeekDayWithDate = str
Diary = dict[WeekDayWithDate, list["Lesson"]]


class DeEduOrb():
    @exception_token_handler
    async def get_diary(self, *, user: User, date: datetime.datetime):
        return await EduOrbRequest(user).get_diary_object(date)
            
    @exception_token_handler
    async def get_marks(self, *, user: User, period: "Period"):
        print(user, period)
        return
    

class Period(NamedTuple):
    date_begin: datetime.datetime
    date_end: datetime.datetime

class Lesson:
    pass

user = get_user(db_session, 1122659029)

asyncio.run(DeEduOrb().get_diary(user=user, date=datetime.datetime(2023, 11, 23)))
