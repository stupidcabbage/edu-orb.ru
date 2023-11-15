import logging
from datetime import datetime
from typing import Literal, Optional, Union

from diary.api.classes import Lesson
from diary.api.diary import get_diary, get_study_diary
from diary.api.marks import get_marks
from diary.config import CURRENT_USER, db_session
from diary.db.services.users import get_user_for_notification
from diary.db.models import Mark, User
from diary.db.sessions import DBsession
from diary.services.time import get_notification_days, get_tomorrow_date, parse_date
from diary.db.services.marks import add_mark, get_count_db_subject_marks, is_mark_exists

MARKS = {
    "Неявка": 6,
    "Пропуск": 7,
    "Болеет": 8
}


async def check_for_new_marks(user: User, date: datetime):
    diary = await get_study_diary(user, date)
    if not diary:
        return None
    
    new_marks = []
    parcipiant_id = user.parcipiants_id[CURRENT_USER].parcipiant_id
    for day in diary.values():
        for lesson in day:
            new_marks.append(add_marks(db_session, lesson, parcipiant_id))
    return new_marks


def add_marks(session: DBsession,
              lesson: Lesson,
              parcipiant_id: str) -> list[Optional[Mark]]:
    "Добавляет оценки из урока в БД"
    marks = get_list_marks(lesson)
    new_marks = []
    for mark in marks:
        DBmark = Mark(subject=lesson.subject,
                      lesson_number=lesson.lessonNumber,
                      mark=mark, date=parse_date(lesson.date), 
                      parcipiant_id=parcipiant_id)
        if not is_mark_exists(session, DBmark):
            add_mark(session, DBmark)
            new_marks.append(DBmark)
    return new_marks


def get_list_marks(lesson: Lesson) -> list[int]:
    marks = []
    for mark in lesson.marksRaw:
        marks.append(mark)
    for absence in lesson.absenceRaw:
        mark = MARKS.get(absence)
        if not None:
            marks.append(mark)
    return marks


async def check_new_marks(user: User, dates: list[datetime]):
    new_marks = []
    subject_marks = await get_marks(dates[-1], datetime.today(), user)
    for subject in subject_marks:
        marks_counts = get_count_db_subject_marks(db_session, subject.name,
                                                   dates[-1], user.parcipiants_id[CURRENT_USER])
        print(f"Оценки из выписки по {subject.name}: {subject.marks}. Количество оценок в БД: {marks_counts}")
        for date in dates:
            if subject.marks and not len(subject.marks) == marks_counts:
                marks = await check_for_new_marks(user, date)
                if marks:
                    marks.append(marks)
            else: 
                break
    return new_marks


async def marks_poiling():
    users = get_user_for_notification(db_session)
    temp = []
    for user in users:
        return await check_new_marks(user, get_notification_days())
        for date in (parse_date("06.11.2023"), 
        parse_date("30.10.2023"), parse_date("23.10.2023"), parse_date("16.10.2023"), parse_date("06.11.2023"), parse_date("13.11.2023")):
            temp.append(await first_create_mark(user, date))
            print("------------------------------------------------------------------------------------")
        return temp
