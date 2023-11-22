import datetime
from typing import NewType
from pydantic import BaseModel

from diary.db.models import User


WeekDayWithDate = NewType("WeekDayWithDate", str)


class EduOrbDiary():
    def __init__(self, user: User):
        self.user = user
        self.base_url = "https://de.edu.orb.ru"

    async def get_diary(self, date: datetime.datetime):
        cookies = {"PHPSESSID": f"{self.user.phpsessid}"}
        parcipiant_id = self.user.current_parcipiant.parcipiant_id
        url = f"{self.base_url}/edv/index/diary/{parcipiant_id}?date={date}"
        response = await get_json_response(url, cookies)
        return response

class Lesson(BaseModel):
    pass


class SchoolPeriod(BaseModel):
    pass


class DiaryResponseData(BaseModel):
    diary: dict[WeekDayWithDate, list[Lesson]] | list[None]
    edu_periods: list[SchoolPeriod] | list[None]


class EduOrbResponse(BaseModel):
    success: bool
    message: str
    data: DiaryResponseData
