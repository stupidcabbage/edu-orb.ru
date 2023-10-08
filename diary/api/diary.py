from dataclasses import dataclass
import json
import requests
from pydantic import BaseModel, Field, ConfigDict, field_serializer, validator
import re

days = {
    "Понедельник": "monday",
    "Вторник": "tuesday",
    "Среда": "wednesday",
    "Четверг": "thursday",
    "Пятница": "friday"
}

day = "09.10."


class PreviosHomewok(BaseModel):
    date: str
    homework: str


class Lesson(BaseModel):
    subject: str
    teacher: str
    date: str
    marks: list[int]
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


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

s = requests.Session()
with open("cookies.json", "r") as f:
    cookie = json.load(f)
for cook in cookie:
    s.cookies.set(cook['name'], cook['value'])
r = s.get("https://de.edu.orb.ru/#diary")
r = s.get("https://de.edu.orb.ru/edv/index/diary/A7A48C5F8B939B82826487956E3FA893?date=09.10.2023", headers=headers).json()

a = Diary.model_validate(r)

