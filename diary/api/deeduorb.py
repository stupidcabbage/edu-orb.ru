import datetime
from typing import NamedTuple

from diary.api.handlers import exception_token_handler
from diary.api.request import EduOrbRequest
from diary.db.models.users import User
from diary.services.time import format_date_with_weekday

WeekDayWithDate = str
Diary = dict[WeekDayWithDate, list["Lesson"]]


class DeEduOrb():
    def __init__(self, user: User) -> None:
        self.user = user

    async def get_day_diary(self, *, date: datetime.datetime):
        diary = await self.get_diary(date=date)
        return self.get_weekday_from_diary(diary=diary, date=date)

    async def get_diary(self, *, date: datetime.datetime) -> Diary:
        return await EduOrbRequest(self.user).get_diary_object(date)

    @exception_token_handler
    async def get_marks(self, *, user: User, period: "Period"):
        print(user, period)
        return

    def get_weekday_from_diary(self, *, diary, date: datetime.datetime):
        return diary.get(format_date_with_weekday(date))

class Period(NamedTuple):
    date_begin: datetime.datetime
    date_end: datetime.datetime

class Lesson:
    pass
