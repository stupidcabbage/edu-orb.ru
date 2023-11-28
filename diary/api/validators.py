import datetime
import logging
from enum import Enum
from typing import NoReturn, Optional, Union

from pydantic import BaseModel, Field, ValidationError, field_serializer, field_validator

from diary.api.exceptions import ParcipiantNotFound, UnknownServerResponse
from diary.db.models import User
from diary.services.time import parse_date

WeekdayWithDate = str

class EduOrbDiaryObject():
    def __init__(self, user: User, date: datetime.datetime, data: dict):
        self.user = user
        self.date = date
        self.data = data

    async def get_diary_object(self):
        response = await self.validate_diary()
        return await self.get_diary_from_response(response)
    
    async def get_diary_from_response(self, response: "DiaryDataResponse"):
        if self.is_lessons_exists(response):
            return response.data.diary
        return {}
    
    async def validate_diary(self):
        try:
            return DiaryDataResponse.model_validate(self.data)
        except ValidationError:
            response = FailEduOrbResponse.model_validate(self.data)
            await self.raise_bad_reponse_exception(response)
        except Exception as e:
            logging.error(
                    f"Unknow validation error. User: {self.user}. Error: {e}") 
            raise 

    async def raise_bad_reponse_exception(self, response: "FailEduOrbResponse") -> NoReturn:
        error = response.message
        match error:
            case self.EduOrbBadResponse.ParcipiantNotFound.value:
                raise ParcipiantNotFound
            case _:
                logging.error(
                        f"Unknow server response. User: {self.user}. Error: {error}")
                raise UnknownServerResponse
    
    class EduOrbBadResponse(Enum):
        ParcipiantNotFound = "Ученик не найден"

    def is_lessons_exists(self, response: "DiaryDataResponse"):
        return (isinstance(response.data, DiaryData) and
                isinstance(response.data.diary, dict))
    
class BaseEduOrbResponse(BaseModel):
    success: bool
    message: str

class DiaryData(BaseModel):
    diary: Union[dict[WeekdayWithDate, list["Lesson"]], list[None]]

class FailEduOrbResponse(BaseEduOrbResponse):
    pass

class DiaryDataResponse(BaseEduOrbResponse):
    data: DiaryData


class PreviosHomewok(BaseModel):
    date: str
    homework: str


class Lesson(BaseModel):
    """
    Attributes:
        date The lesson date
    """
    subject: str
    teacher: str
    date: datetime.datetime
    grades: list[int] = Field(alias="marksRaw")
    absences: list[str] = Field(alias="absenceRaw")
    lesson_number: int = Field(alias="lessonNumber")
    lesson_time: str = Field(alias="lessonTime")
    homework: Optional[str]
    previous_homework: Optional[PreviosHomewok] = Field("previousHomework")
    topic: Optional[str]
    
    @field_validator("date", mode="before")
    def validate_date(cls, date):
        return parse_date(date)
