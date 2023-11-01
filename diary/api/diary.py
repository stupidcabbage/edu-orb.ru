import datetime

import aiohttp
from loguru import logger
from diary.api.classes import Diary, Lesson
from diary.config import CURRENT_USER

from diary.db.models import User

WEEKDAYS = ("Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота", "Воскресенье")


def get_weekday(date: str) -> str:
    day, month, year = date.split(".")
    weekday = WEEKDAYS[datetime.datetime(int(year), int(month), int(day)).weekday()]
    return f"{day}.{month}. {weekday}"


def get_tomorrow_date() -> str:
    return (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

async def get_diary_json(date: str, user: User) -> dict:
    """
    Возвращает расписание в виде json.
    :param date str: Дата начала в расписании (DD.MM.YYYY).
    :param user User: Пользователь, который делает запрос.
    """
    cookies = {"PHPSESSID": f"{user.phpsessid}"}
    parcipiant_id = user.parcipiants_id[CURRENT_USER].parcipiant_id
    async with aiohttp.ClientSession(headers=HEADERS, 
                                     cookies=cookies) as s:
        async with s.get(f"https://de.edu.orb.ru/edv/index/diary/{parcipiant_id}?date={date}") as r:
            return await r.json()


async def get_diary(user: User, date: str = get_tomorrow_date()) -> Diary | None:
    """
    Возвращает расписание.
    :param date str: Дата начала в расписании (DD.MM.YYYY). Default=следующий день.
    :param user User: Пользователь, который делает запрос.
    """
    diary = await get_diary_json(date, user)
    try:
        return Diary.model_validate(diary)
    except Exception as e:
        logger.warning(f"Не удалось получить дневник: {e}")
        return None


async def get_lessons(user: User,
                      date: str = get_tomorrow_date()) -> list[Lesson] | None:
    """
    Возвращает уроки переданного дня. Если в этот день нет уроков, то
    возвращает None
    :param date str: Дата начала в расписании (DD.MM.YYYY). Default=следующий день.
    :param user User: Пользователь, который делает запрос.
    """
    diary = await get_diary(user, date)
    if not diary.data.diary:
        return None
    return diary.data.diary.get(get_weekday(date))
