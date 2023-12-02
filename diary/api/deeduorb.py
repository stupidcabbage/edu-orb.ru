import datetime

from diary.api.request import EduOrbRequest
from diary.api.validators import DiaryEduOrbValidator
from diary.api.marksparser import MarksParser
from diary.db.models.users import User
from diary.services.time import format_date_with_weekday
from diary.api.parcipiant import EduOrbParcipiant

WeekDayWithDate = str

class DeEduOrb:
    def __init__(self, user: User) -> None:
        self.parcipiant: EduOrbParcipiant = self.transform_user_to_parcipiant(user)

    def transform_user_to_parcipiant(self, user: User):
        if not isinstance(user, User):
            raise TypeError("Должна передаваться модель пользователя из БД!")

        return EduOrbParcipiant(
                parcipiant_id=user.current_parcipiant().parcipiant_id,
                phpsessid=user.phpsessid)

    async def get_day_diary(self, *, date: datetime.datetime):
        diary = await self.get_diary(date=date)
        return self.get_weekday_from_diary(diary=diary, date=date)

    async def get_diary(self, *, date: datetime.datetime):
        response = await EduOrbRequest(self.parcipiant).get_json_index_diary(date)
        diary = await DiaryEduOrbValidator(response).get_diary_object()
        return diary

    async def get_marks(self, *, period: tuple[datetime.datetime,
                                               datetime.datetime]):
        html_data = await EduOrbRequest(self.parcipiant).get_marks_table(period)
        marks = await MarksParser(html_data).get_marks()
        return marks

    def get_weekday_from_diary(self, *, diary, date: datetime.datetime):
        return diary.get(format_date_with_weekday(date))
