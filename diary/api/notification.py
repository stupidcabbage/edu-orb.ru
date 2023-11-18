import logging
import time
from abc import ABC
from datetime import datetime
from typing import Optional

from diary.api.classes import Lesson
from diary.api.diary import get_study_diary
from diary.api.marks import SubjectMarks, get_marks
from diary.config import db_session
from diary.db.models import User
from diary.db.models.users import Mark
from diary.db.services.marks import (bulk_add_marks, get_count_grades,
                                     is_mark_exists)
from diary.db.services.users import get_user_for_notification
from diary.services.time import get_notification_days, parse_date
from diary.telegram.handlers.notification import send_notification_message


class MarkNotification(ABC):
    """
    Уведомления о новых оценках.

    :param session DBsession: Сессия для работы с БД.
    """
    def __init__(self):
        self.session = db_session
        self.users = []

    async def start_poiling(self):
        "Старт проверки новых оценок."
        logging.info("Start poiling marks")
        while True:
            self.users = get_user_for_notification(self.session)
            await self.check_new_marks()
            time.sleep(300)
    
    async def check_new_marks(self):
        """
        Проверяет на наличие новых оценок у всех пользователей,
        для которых это необходимо.
        """
        for user in self.users:
            worker = MarkNotificationWorker(user)
            await worker.check_marks_and_notify()


class MarkNotificationWorker(MarkNotification):
    THIRD_WEEK = -1
    MARKS = {
        "Неявка": 6,
        "Пропуск": 7,
        "Болеет": 8
    }

    def __init__(self, user: User):
        self.session = db_session
        self.user = user
        self.new_marks = []
        self.notification_days = get_notification_days()

    async def check_marks_and_notify(self):
        """
        Проверяет на наличие новых оценок у пользователя.
        При наличии таковых: добавляет их в БД и уведомляет пользователя.
        """
        await self.check_marks()
        if self.new_marks:
            await self.add_marks_to_db()
            await self.notify()
    
    async def add_marks_to_db(self) -> None:
        "Добавляет новые оценки в БД."
        bulk_add_marks(self.session, self.new_marks)
    
    async def notify(self) -> None:
        "Уведомляет пользователя о наличии новых отметок."
        await send_notification_message(self.user, self.new_marks)
    
    async def check_marks(self):
        "Проверяет, что поставили ли пользователю новые оценки."
        report = await get_marks(self.notification_days[self.THIRD_WEEK],
                                 datetime.today(),
                                 self.user)
        for subject in report:
            await self.obtain_new_subject_marks(subject)
    
    async def obtain_new_subject_marks(self, subject: SubjectMarks):
        """
        Получает новые оценки у предмета.
        :param subject SubjectMarks: предмет из выписки оценок.
        """
        if self.is_amount_report_marks_more_amount_in_db(subject):
            await self.find_new_marks()
    
    async def find_new_marks(self):
        "Находит новые оценки."
        for date in self.notification_days:
            await self.check_for_new_marks(date)
    
    async def check_for_new_marks(self, date):
        "Проверяет, что новые отметки существуют."
        diary = await get_study_diary(self.user, date)
        if not diary:
            return

        for lessons in diary.values():
            await self.append_new_marks_if_exists(lessons)

    async def append_new_marks_if_exists(self, lessons: list[Lesson]):
        "Добавляет новые оценки в список, если таковые существуют."
        for lesson in lessons:
            await self.append_new_lesson_marks_if_not_exists(lesson)

    async def append_new_lesson_marks_if_not_exists(self, lesson: Lesson):
        "Добавляет новые оценки предмета, если таковых нет в БД."
        marks = self.make_list_marks(lesson)
        for mark in marks:
            self.append_new_mark_if_not_exists(self.build_mark(lesson, mark))

    def append_new_mark_if_not_exists(self, mark: Mark):
        "Добавляет новую оценку, если такой нет в БД"
        if not is_mark_exists(self.session, mark):
            self.new_marks.append(mark)
        
    def make_list_marks(self, lesson: Lesson) -> list[int]:
        "Создает общий список оценок."
        marks = []
        for mark in lesson.marksRaw:
            marks.append(mark)
        for absence in lesson.absenceRaw:
            mark = self.transfrom_absence_to_integer(absence)
            if not mark:
                marks.append(mark)
        return marks

    def transfrom_absence_to_integer(self, absence: str) -> Optional[int]:
        "Переделывает пропуск из журнального формата в нумерной."
        return self.MARKS.get(absence)

    def build_mark(self, lesson: Lesson, mark: int):
        "Делает модель оценки для БД"
        return Mark(subject=lesson.subject,
                    lesson_number=lesson.lessonNumber,
                    mark=mark, date=parse_date(lesson.date),
                    parcipiant_id=self.user.current_parcipiant().parcipiant_id)

    def is_amount_report_marks_more_amount_in_db(self, subject):
        "Проверяет, что количество оценок в БД меньше, чем в выписке."
        marks_amount = get_count_grades(self.session, subject.name,
                                        self.notification_days[self.THIRD_WEEK],
                                        self.user.current_parcipiant())
        return subject.marks and len(subject.marks) > (marks_amount + len(self.new_marks))
