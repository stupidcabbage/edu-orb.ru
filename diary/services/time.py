import datetime

from dateparser import parse

from diary.services.exceptions import DateNotCorrect

WEEKDAYS = ("Понедельник", "Вторник", "Среда",
            "Четверг", "Пятница", "Суббота", "Воскресенье")


def get_weekday_russian(date: datetime.datetime) -> str:
    "Возвращает название недели на русском языке"
    return WEEKDAYS[date.weekday()]

def get_tomorrow_date() -> datetime.datetime:
    "Возвращает дату завтрашнего дня."
    return datetime.datetime.today() + datetime.timedelta(days=1)


def format_date_with_weekday(date: datetime.datetime) -> str:
    "Возврашает время в формате: день.месяц. день недели (на русском языке)"
    weekday = get_weekday_russian(date)
    return date.strftime("%d.%m. ") + weekday


def parse_date(date: str) -> datetime.datetime:
    "Парсит время из текста и возвращает его в формате datetime"
    parsed_date = parse(date,
                        settings={"TIMEZONE": "Asia/Yekaterinburg",
                                  "PREFER_DATES_FROM": "future"},
                        date_formats=["%d.%m.%Y"])
    if not parsed_date:
        raise DateNotCorrect
    return parsed_date

def get_notification_days() -> list[datetime.datetime]:
    """
    Возвращает список из дат (три понедельника), в которые
    могли поставить оценки.
    Первая дата - ближайший понедельник. Последующие - предыдущий понедельник.
    """
    days = []
    for i in range(3, 6):
        days.append(parse_date("понедельник") - datetime.timedelta(days=i*7))
    return days

def format_date(date: datetime.datetime) -> str:
    "Возвращает время в формате: день.месяц.год"
    return date.strftime("%d.%m.%Y")
