from abc import ABC
from datetime import datetime
from diary.api.diary import get_study_diary
from diary.api.marks import SubjectMarks, get_marks
from diary.db.models import User
from diary.db.services.marks import get_count_db_subject_marks

from diary.db.services.users import get_user_for_notification
from diary.db.sessions import DBsession
from diary.services.time import get_notification_days


class MarkNotification(ABC):
    """
    Уведомления о новых оценках.

    :param session DBsession: Сессия для работы с БД.
    """
    def __init__(self, session: DBsession):
        self.session = session
        self.users = []

    async def start_poiling(self):
        "Старт проверки новых оценок."
        self.users = get_user_for_notification(self.session)
        await self.check_new_marks()
    
    async def check_new_marks(self):
        for user in self.users:
            worker = MarkNotificationWorker(self.session, user)
            return worker.check_marks()


class MarkNotificationWorker(MarkNotification):
    THIRD_WEEK = -1

    def __init__(self, session: DBsession, user: User):
        self.session = session
        self.user = user
        self.new_marks = []
        self.notification_days = get_notification_days()

    async def check_marks(self):
        report = await get_marks(self.notification_days[self.THIRD_WEEK],
                                 datetime.today(),
                                 self.user)
        for subject in report:
            await self.obtain_new_subject_marks(subject)

    async def obtain_new_subject_marks(self, subject: SubjectMarks):
        if self.is_amount_report_marks_more_amount_in_db(subject):
            await self.find_new_marks()
    
    async def find_new_marks(self):
        for date in self.notification_days:
            await self.check_for_new_marks(date)
    
    async def check_for_new_marks(self, date):
        diary = await get_study_diary(self.user, date)
        if not diary:
            return

        for lessons in diary.values():
            self.append_new_marks_if_exists(lessons)

    def append_new_marks_if_exists(self, lessons: list[Lesson]):
        for lesson in lessons:
            pass



    def is_amount_report_marks_more_amount_in_db(self, subject):
        marks_amount = get_count_db_subject_marks(self.session, subject,
                                                  self.notification_days[self.THIRD_WEEK],
                                                  self.user.current_parcipiant())
        return subject.marks and len(subject.marks) > (marks_amount + len(self.new_marks))












