import datetime
from typing import NamedTuple

import aiohttp

from diary.db.models import User
from diary.services.time import format_date


class EduOrbCookies():
    def __init__(self, user: User):
        self.user = user # TODO: Убрать зависимость от юзера
    
    async def get_with_phpsessid(self) -> dict:
        return {"PHPSESSID": f"{self.user.phpsessid}"}

class Period(NamedTuple): # TODO: убрать класс
    date_begin: datetime.datetime
    date_end: datetime.datetime


class BaseEduOrbRequest:
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
    }
    BASE_URL = "https://de.edu.orb.ru"

    def __init__(self, user: User,
                 headers: dict = DEFAULT_HEADERS):
        self.user = user # TODO: Убрать зависимоость от юзера | Сделать parcipiant ID
        self.cookies = EduOrbCookies(self.user)
        self.headers = headers

    async def get_json(self, url: str) -> dict:
        cookies = await self.cookies.get_with_phpsessid()
        url = self.constitute_full_url(url) # TODO: Функция должна получать уже полный URL. Или переделывать его в init

        async with aiohttp.ClientSession(
                cookies=cookies, headers=self.headers) as session:
            async with session.get(url) as response:
                return await response.json()

    async def get_text(self, url: str) -> str:
        cookies = await self.cookies.get_with_phpsessid()
        url = self.constitute_full_url(url) # TODO: Функция должна получать уже полный URL. Или переделывать его в init
        print(url)
        async with aiohttp.ClientSession(headers=self.headers, 
                                         cookies=cookies) as s:
            async with s.get(url) as response:
                return await response.text()


    def constitute_full_url(self, url: str) -> str:
        return self.BASE_URL + url


class EduOrbRequest(BaseEduOrbRequest):
    async def get_json_index_diary(self, date: datetime.datetime) -> dict:
        "Возвращает JSON с данными от API дневника"
        return await DiaryEduOrbRequest(user=self.user).get_index_diary(date)

    async def get_marks_table(self, period: Period):
        return await MarksEduOrbRequest(user=self.user).get_html_marks_table(period)


class MarksEduOrbRequest(BaseEduOrbRequest):
    async def get_html_marks_table(self, period: Period):
        url = await self.make_html_mark_url(period)
        return await self.get_text(url)

    async def make_html_mark_url(self, period: Period):
        parcipiant_id = self.user.current_parcipiant().parcipiant_id # TODO: Закон дементры.
        return f"/edv/index/report/marks/{parcipiant_id}?begin={format_date(period.date_begin)}&end={format_date(period.date_end)}&format=html"


class DiaryEduOrbRequest(BaseEduOrbRequest):
    async def get_index_diary(self, date: datetime.datetime) -> dict:
        url = await self.make_index_diary_url(date)
        return await self.get_json(url)

    async def make_index_diary_url(self, date: datetime.datetime) -> str:
        parcipiant_id = self.user.current_parcipiant().parcipiant_id # TODO: Закон дементры.
        return f"/edv/index/diary/{parcipiant_id}?date={format_date(date)}"
