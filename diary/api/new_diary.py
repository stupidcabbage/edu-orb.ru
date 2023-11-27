import datetime
import logging
from dataclasses import dataclass
from typing import NamedTuple, Union

import aiohttp
from pydantic import BaseModel, ValidationError

from diary.db.models import User
from diary.services.time import format_date

WeekDayWithDate = str

class EduOrbCookies():
    def __init__(self, user: User):
        self.user = user
    
    @property
    async def with_phpsessid(self) -> dict:
        return {"PHPSESSID": f"{self.user.phpsessid}"}

class EduOrbRequest():
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
    }

    def __init__(self, user: User,
                 headers: dict = DEFAULT_HEADERS):
        self.base_url = "https://de.edu.orb.ru"
        self.user = user
        self.cookies = EduOrbCookies(self.user)
        self.headers = headers
        
    async def get_diary_object(self):
        pass
    
    async def get_index_diary(self, date: datetime.datetime) -> dict:
        url = await self.make_index_diary_url(date)
        return await self.get_json(url)

    async def get_json(self, url: str) -> dict:
        cookies = await self.cookies.with_phpsessid
        url = self.base_url + url

        async with aiohttp.ClientSession(
                cookies=cookies, headers=self.headers) as session:
            async with session.get(url) as response:
                return await response.json()

    async def make_index_diary_url(self, date: datetime.datetime) -> str:
        parcipiant_id = self.user.current_parcipiant().parcipiant_id
        return f"/edv/index/diary/{parcipiant_id}?date={format_date(date)}"



class Lesson(BaseModel):
    pass


class SchoolPeriod(BaseModel):
    pass


class DiaryResponseData(BaseModel):
    diary: dict[WeekDayWithDate, list[Lesson]] | list[None]
    edu_periods: list[SchoolPeriod] | list[None]


class BaseEduOrbResponse(BaseModel):
    success: bool
    message: str

class EduOrbFailResponse(BaseEduOrbResponse):
    pass

class EduOrbSuccessResponse(BaseEduOrbResponse):
    data: DiaryResponseData

class EduOrbObject():
    def __init__(self, user: User, data):
        self.user = user
        super().__init__(self.user)

    async def get_diary(self, date: datetime.datetime):
        data = await self.get_diary_data(date)
        if not data.success:
            return ()
        return data.data.diary

    async def get_diary_data(self, date: datetime.datetime) -> Union[EduOrbFailResponse, EduOrbSuccessResponse]:
        response = await self.get_index_diary(date) 
        return self.validate_diary_response(response)

    def validate_diary_response(self, response):
        try:
            return self.validate_success_response(response)
        except Exception as error:
            logging.error(f"Unknown response error: {error}")
            raise 
        
    def validate_success_response(self, response):
        try:
            return EduOrbSuccessResponse.model_validate(response)
        except ValidationError:
            return self.validate_fail_response(response)

    def validate_fail_response(self, response):
        try:
            return EduOrbFailResponse.model_validate(response)
        except Exception:
            raise


@dataclass
class Parcipiant:
    parcipiant_id: str
    cookies: dict


class Period(NamedTuple):
    date_begin: datetime.datetime
    date_end: datetime.datetime


class DeEduOrb:
    Diary = dict[WeekDayWithDate, list[Lesson]]
    def get_diary(self, 
                  parcipiant: Parcipiant,
                  date: datetime.datetime) -> Diary:
        print(parcipiant, date)

    def get_marks(self,
                  parcipiant: Parcipiant,
                  period: Period):
        print(parcipiant, period)
