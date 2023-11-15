import datetime
from typing import Optional

import logging

from diary.api.classes import Diary, Lesson
from diary.api.response import get_json_response
from diary.config import CURRENT_USER
from diary.db.models import User
from diary.services.time import format_date, format_date_with_weekday


async def get_diary_json(date: str, user: User) -> dict:
    """
    Возвращает расписание в виде json.
    :param date str: Дата начала в расписании (DD.MM.YYYY).
    :param user User: Пользователь, который делает запрос.
    """
    cookies = {"PHPSESSID": f"{user.phpsessid}"}
    parcipiant_id = user.parcipiants_id[CURRENT_USER].parcipiant_id
    url = f"https://de.edu.orb.ru/edv/index/diary/{parcipiant_id}?date={date}"
    response = await get_json_response(url, cookies)
    return response


async def get_diary(user: User, date: datetime.datetime) -> Optional[Diary]:
    """
    Возвращает расписание.
    :param date str: Дата начала в расписании (DD.MM.YYYY). Default=следующий день.
    :param user User: Пользователь, который делает запрос.
    """
    diary = await get_diary_json(format_date(date), user)
    try:
        return Diary.model_validate(diary)
    except Exception as e:
        logging.warning(f"Не удалось получить дневник: {e}")
        return None

async def get_study_diary(user: User,
                          date: datetime.datetime) -> Optional[dict[str, list[Lesson]]]:
    diary = await get_diary(user, date)
    if not diary.data:
        return None
    if not isinstance(diary.data.diary, dict):
        return None
    return diary.data.diary

async def get_lessons(user: User,
                      date: datetime.datetime) -> Optional[list[Lesson]]:
    """
    Возвращает уроки переданного дня. Если в этот день нет уроков, то
    возвращает None
    :param date str: Дата начала в расписании (DD.MM.YYYY).
    :param user User: Пользователь, который делает запрос.
    """
    diary = await get_diary(user, date)
    if not diary.data.diary:
        return None
    return diary.data.diary.get(format_date_with_weekday(date))
