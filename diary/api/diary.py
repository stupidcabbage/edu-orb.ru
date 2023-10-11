import datetime
import json

import requests
from pydantic import BaseModel


def get_tomorrow() -> str:
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


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

def get_diary():
    s = requests.Session()
    with open("cookies.json", "r") as f:
        cookie = json.load(f)
    for cook in cookie:
        s.cookies.set(cook['name'], cook['value'])

    r = s.get(f"https://de.edu.orb.ru/edv/index/diary/A7A48C5F8B939B82826487956E3FA893?date={get_tomorrow()}",
              headers=headers).json()
    a = Diary.model_validate(r)
    return a.data.diary

print(get_diary())
# for day, lesson in get_diary().diary.items():
#     print("на", day)
#     for i in lesson:
#         print(f"{i.lessonNumber}. {i.subject}: {i.previousHomework.homework if i.previousHomework else i.homework}")
