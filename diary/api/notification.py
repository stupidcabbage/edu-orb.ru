import logging
from datetime import datetime

from diary.api.classes import Lesson
from diary.api.diary import get_diary
from diary.config import CURRENT_USER, db_session
from diary.db.services.users import get_user_for_notification
from diary.db.models import Mark, User
from diary.services.time import parse_date
from diary.db.services.marks import add_mark, is_subject_mark_exists

MARKS = {
    "Неявка": 6,
    "Пропуск": 7,
    "Болеет": 8,
    "Опоздал": 9
}


async def first_create_mark(user: User, date: datetime):
    diary = await get_diary(user, date)
    if not diary.data:
        return None
    diary = diary.data.diary
    if not isinstance(diary, dict):
        return None

    parcipiant_id = user.parcipiants_id[CURRENT_USER].parcipiant_id
    for day in diary.values():
        for lesson in day:
            add_marks(lesson, parcipiant_id)


def add_marks(lesson: Lesson,
              parcipiant_id: str):
    "Добавляет оценки из урока в БД"
    marks = get_list_marks(lesson)
    for mark in marks:
        DBmark = Mark(subject=lesson.subject,
                      lesson_number=lesson.lessonNumber,
                      mark=mark, date=parse_date(lesson.date), 
                      parcipiant_id=parcipiant_id)
        if not is_subject_mark_exists(db_session, DBmark):
            add_mark(db_session, DBmark)
        else:
            logging.info(f"{DBmark} already exists")


def get_list_marks(lesson: Lesson) -> list[int]:
    marks = []
    for mark in lesson.marksRaw:
        marks.append(mark)
    for absence in lesson.absenceRaw:
        mark = MARKS.get(absence)
        if not None:
            marks.append(mark)
    return marks



async def marks_poiling():
    users = get_user_for_notification(db_session)
    temp = []
    for user in users:
        for date in (parse_date("30.11.2023"), parse_date("06.11.2023"), parse_date("13.11.2023")):
            temp.append(await first_create_mark(user, date))
        return temp
