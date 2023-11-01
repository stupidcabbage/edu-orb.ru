from datetime import datetime
from dateparser import parse


class DateNotCorrect(Exception):
    def __str__(self):
        return "Указанное время некорректно."


def parse_pagination_date(date: str) -> datetime:
    parsed_date = parse(date, date_formats=["%d.%m.%Y"])
    if not parsed_date:
        raise DateNotCorrect
    return parsed_date


def parse_date(date: str) -> datetime:
    parsed_date = parse(date,
                        settings={"TIMEZONE": "Asia/Yekaterinburg",
                                  "PREFER_DATES_FROM": "future"})
    if not parsed_date:
        raise DateNotCorrect
    return parsed_date


def format_date(date: datetime) -> str:
    return date.strftime("%d.%m.%Y")
