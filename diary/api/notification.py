from dataclasses import dataclass
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
from diary.db.services.marks import add_mark, bulk_add_marks, get_count_db_subject_marks, is_mark_exists

MARKS = {
    "Неявка": 6,
    "Пропуск": 7,
    "Болеет": 8
}


class Notification:
    def __init__(self, session):
        self.session: DBsession = session
        self.new_marks = []

    async def start_poiling(self):
        users = get_user_for_notification(self.session)
        for user in users:
            return await self.check_new_marks(user, get_notification_days())


    async def check_new_marks(self, user: User, dates: list[datetime]):
        new_marks = []
        subject_marks = await get_marks(dates[-1], datetime.today(), user)
        for subject in subject_marks:
            marks_counts = get_count_db_subject_marks(self.session, subject.name,
                                                   dates[-1], user.parcipiants_id[CURRENT_USER])
            for date in dates:
                if subject.marks and not len(subject.marks) == (marks_counts + len(new_marks)):
                    marks = await self.check_for_new_marks(user, date, db_session)
                    if marks:
                        new_marks += marks
                else: 
                    break
            if new_marks:
                bulk_add_marks(self.session, new_marks)
                new_marks=[]
        return new_marks


    async def check_for_new_marks(self, user: User, date: datetime, session: DBsession):
        diary = await get_study_diary(user, date)
        if not diary:
            return None
    
        new_marks = []
        parcipiant_id = user.parcipiants_id[CURRENT_USER].parcipiant_id
        for day in diary.values():
            for lesson in day:
                marks = self.make_list_marks(lesson)
                for mark in marks:
                    DBmark = Mark(subject=lesson.subject,
                            lesson_number=lesson.lessonNumber,
                            mark=mark, date=parse_date(lesson.date), 
                            parcipiant_id=parcipiant_id)
                    if not is_mark_exists(session, DBmark):
                        new_marks.append(DBmark)
        return new_marks

    def build_mark(lesson: Lesson, mark: int):
        DBmark = Mark(subject=lesson.subject,
                      lesson_number=lesson.lessonNumber,
                      mark=mark, date=parse_date(lesson.date),
                      parcipiant_id=parcipiant_id)

    def make_list_marks(self, lesson: Lesson) -> list[int]:
        marks = []
        for mark in lesson.marksRaw:
            marks.append(mark)
        for absence in lesson.absenceRaw:
            mark = MARKS.get(absence)
            if not None:
                marks.append(mark)
        return marks

async def check_for_new_marks(user: User, date: datetime, session: DBsession):
    diary = await get_study_diary(user, date)
    if not diary:
        return None
    
    new_marks = []
    parcipiant_id = user.parcipiants_id[CURRENT_USER].parcipiant_id
    for day in diary.values():
        for lesson in day:
            marks = make_list_marks(lesson)
            for mark in marks:
                DBmark = Mark(subject=lesson.subject,
                          lesson_number=lesson.lessonNumber,
                          mark=mark, date=parse_date(lesson.date), 
                          parcipiant_id=parcipiant_id)
                if not is_mark_exists(session, DBmark):
                    new_marks.append(DBmark)
    return new_marks


def make_list_marks(lesson: Lesson) -> list[int]:
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
        for date in dates:
            if subject.marks and not len(subject.marks) == (marks_counts + len(new_marks)):
                marks = await check_for_new_marks(user, date, db_session)
                if marks:
                    new_marks += marks
            else: 
                break
        if new_marks:
            bulk_add_marks(db_session, new_marks)
            new_marks=[]
    return new_marks


async def marks_poiling():
    users = get_user_for_notification(db_session)
    for user in users:
        return await check_new_marks(user, get_notification_days())
