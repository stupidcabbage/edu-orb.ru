import datetime
import logging
from typing import NoReturn, Optional, Union

from pydantic import BaseModel, Field, ValidationError, field_validator

from diary.api.exceptions import ParcipiantNotFound, UnknownServerResponse
from diary.services.time import parse_date

WeekdayWithDate = str


class DiaryEduOrbValidator():
    def __init__(self, data: dict):
        self.data = data

    async def get_diary_object(self):
        response = await self.validate_diary_response()
        return await self.get_diary_from_response(response)
    
    async def validate_diary_response(self):
        try:
            return DiaryDataResponse.model_validate(self.data)
        except ValidationError:
            response = ErrorEduOrbResponse.model_validate(self.data)
            await self.raise_bad_reponse_exception(response)
        except Exception as e:
            logging.error(
                    f"Unknown validation error. Error: {e}") 
            raise 

    async def raise_bad_reponse_exception(self, response: "ErrorEduOrbResponse") -> NoReturn:
        error = response.message
        match error:
            case "Ученик не найден":
                logging.error("Validate error: Parcipiant Not Found.")
                raise ParcipiantNotFound
            case _:
                logging.error(
                        f"Unknown server response. Error: {error}")
                raise UnknownServerResponse

    async def get_diary_from_response(self, response: "DiaryDataResponse"):
        if self.is_lessons_exists(response):
            return response.data.diary
        return {}
    
    def is_lessons_exists(self, response: "DiaryDataResponse"):
        return (isinstance(response.data, DiaryData) and
                isinstance(response.data.diary, dict))


class DiaryData(BaseModel):
    #TODO: Сделать не list[Lesson], а namedtuple с количественной перменной.ё
    diary: Union[dict[WeekdayWithDate, list["Lesson"]], list[None]]


class ErrorEduOrbResponse(BaseModel):
    success: bool
    message: str


class DiaryDataResponse(BaseModel):
    success: bool
    message: str
    data: DiaryData


class PreviosHomewok(BaseModel):
    date: datetime.datetime
    homework: str

    @field_validator("date", mode="before")
    def validate_date(cls, date):
        return parse_date(date)


class Lesson(BaseModel):
    subject: str
    teacher: str
    date: datetime.datetime
    grades: list[int] = Field(alias="marksRaw")
    absences: list[str] = Field(alias="absenceRaw")
    lesson_number: int = Field(alias="lessonNumber")
    lesson_time: str = Field(alias="lessonTime")
    homework: Optional[str]
    previous_homework: Optional[PreviosHomewok] = Field(alias="previousHomework")
    topic: Optional[str]
    
    @field_validator("date", mode="before")
    def validate_date(cls, date):
        return parse_date(date)
