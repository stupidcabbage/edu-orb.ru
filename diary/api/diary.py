import datetime

import aiohttp
from pydantic import BaseModel

from diary.services.user import User

WEEKDAYS = ("Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота", "Воскресенье")


def get_weekday(date: str) -> str:
    day, month, year = date.split(".")
    weekday = WEEKDAYS[datetime.datetime(int(year), int(month), int(day)).weekday()]
    return f"{day}.{month}. {weekday}"


def get_tomorrow_date() -> str:
    return (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")


class PreviosHomewok(BaseModel):
    date: str
    homework: str


class Lesson(BaseModel):
    subject: str
    teacher: str
    date: str
    marksRaw: list[int]
    lessonNumber: int
    lessonTime: str
    homework: str | None
    previousHomework: PreviosHomewok | None
    topic: str | None


class Data(BaseModel):
    diary: dict[str, list[Lesson]]
    edu_periods: list[dict]


class Diary(BaseModel):
    success: bool
    message: str
    data: Data


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

async def get_diary_json(date: str, user: User) -> dict:
    """
    Возвращает расписание в виде json.
    :param date str: Дата начала в расписании (DD.MM.YYYY).
    :param user User: Пользователь, который делает запрос.
    """
    async with aiohttp.ClientSession(headers=HEADERS, 
                                     cookies=user.cookies) as s:
        async with s.get(f"https://de.edu.orb.ru/edv/index/diary/{user.parcipiant_id}?date={date}") as r:
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
    except Exception:
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
    if not diary:
        return None
    return diary.data.diary.get(get_weekday(date))
