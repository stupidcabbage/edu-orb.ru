import datetime
from typing import NamedTuple

import aiohttp
from diary.api.exceptions import PeriodHasIncorrectParametersCount, PeriodIsNotDatetime
from diary.api.parcipiant import EduOrbParcipiant

from diary.services.time import format_date


class Period(NamedTuple): # TODO: убрать класс
    date_begin: datetime.datetime
    date_end: datetime.datetime


class BaseEduOrbRequest:
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
    }
    BASE_URL = "https://de.edu.orb.ru"

    def __init__(self, parcipiant: EduOrbParcipiant,
                 headers: dict = DEFAULT_HEADERS):
        self.parcipiant = parcipiant
        self.cookies = parcipiant.get_cookies_with_phpsessid()
        self.headers = headers

    async def get_json(self, url: str) -> dict:
        url = self.constitute_full_url(url) # TODO: Функция должна получать уже полный URL. Или переделывать его в init

        async with aiohttp.ClientSession(
                cookies=self.cookies, headers=self.headers) as session:
            async with session.get(url) as response:
                return await response.json()

    async def get_text(self, url: str) -> str:
        url = self.constitute_full_url(url) # TODO: Функция должна получать уже полный URL. Или переделывать его в init
        async with aiohttp.ClientSession(headers=self.headers, 
                                         cookies=self.cookies) as s:
            async with s.get(url) as response:
                return await response.text()


    def constitute_full_url(self, url: str) -> str:
        return self.BASE_URL + url


class EduOrbRequest(BaseEduOrbRequest):
    async def get_json_index_diary(self, date: datetime.datetime) -> dict:
        "Возвращает JSON с данными от API дневника"
        return await DiaryEduOrbRequest(self.parcipiant).get_index_diary(date)

    async def get_marks_table(self, period: tuple[datetime.datetime,
                                                  datetime.datetime]):
        return await MarksEduOrbRequest(self.parcipiant).get_html_marks_table(period)


class MarksEduOrbRequest(BaseEduOrbRequest):
    async def get_html_marks_table(self, period: tuple[datetime.datetime,
                                                       datetime.datetime]):
        url = await self.make_html_mark_url(self.transform_to_period(period))
        return await self.get_text(url)

    async def make_html_mark_url(self, period: Period):
        return f"/edv/index/report/marks/{self.parcipiant.parcipiant_id}?begin={format_date(period.date_begin)}&end={format_date(period.date_end)}&format=html"

    def transform_to_period(self, tuple_period: tuple):
        if not len(tuple_period) == 2:
            raise PeriodHasIncorrectParametersCount
        
        if not self.is_tuple_period_datetime(tuple_period):
            raise PeriodIsNotDatetime

        return Period(*tuple_period)

    def is_tuple_period_datetime(self, tuple_period: tuple) -> bool:
        for date in tuple_period:
            if not isinstance(date, datetime.datetime):
                return False
        return True



class DiaryEduOrbRequest(BaseEduOrbRequest):
    async def get_index_diary(self, date: datetime.datetime) -> dict:
        url = await self.make_index_diary_url(date)
        return await self.get_json(url)

    async def make_index_diary_url(self, date: datetime.datetime) -> str:
        return f"/edv/index/diary/{self.parcipiant.parcipiant_id}?date={format_date(date)}"
