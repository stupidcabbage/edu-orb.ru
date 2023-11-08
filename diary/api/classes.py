from pydantic import BaseModel


class PreviosHomewok(BaseModel):
    date: str
    homework: str


class Lesson(BaseModel):
    subject: str
    teacher: str
    date: str
    marksRaw: list[int]
    absenceRaw: list[str]
    lessonNumber: int
    lessonTime: str
    homework: str | None
    previousHomework: PreviosHomewok | None
    topic: str | None


class SchoolPeriod(BaseModel):
    name: str
    dateBegin: str
    dateEnd: str


class Data(BaseModel):
    diary: dict[str, list[Lesson]] | list[None]
    edu_periods: list[SchoolPeriod] | list[None]


class Diary(BaseModel):
    success: bool
    message: str
    data: Data
