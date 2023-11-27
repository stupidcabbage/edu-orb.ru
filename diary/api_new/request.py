import datetime

import aiohttp

from diary.api_new.validators import EduOrbDiaryObject
from diary.db.models import User
from diary.services.time import format_date


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
    
    async def get_diary_object(self, date: datetime.datetime):
        data = await self.get_json_index_diary(date)
        return await EduOrbDiaryObject(self.user, date, data).get_diary_object()

    async def get_json_index_diary(self, date: datetime.datetime) -> dict:
        "Возвращает JSON с данными дневника"
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
