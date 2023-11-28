import datetime

from diary.old_api.classes import SchoolPeriod
from diary.old_api.diary import get_diary
from diary.db.models import User


async def get_school_periods(user: User) -> list[SchoolPeriod]:
    """
    Возвращает школьные периоды в виде списка из объектов SchoolPeriod.
    :param user User: Пользователь, обращающийся к дневнику.
    """
    diary = await get_diary(user, datetime.datetime.today())
    return diary.data.edu_periods
