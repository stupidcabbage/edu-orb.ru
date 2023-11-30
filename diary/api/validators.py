import datetime
import logging
from enum import Enum
from typing import NoReturn, Optional, Union

from pydantic import BaseModel, Field, ValidationError, field_validator

from diary.api.exceptions import ParcipiantNotFound, UnknownServerResponse
from diary.api.request import EduOrbRequest
from diary.db.models import User
from diary.services.time import parse_date

WeekdayWithDate = str

class DiaryEduOrb():
    def __init__(self, user: User):
        self.user = user

    async def get_full_diary(self, date: datetime.datetime):
        response = await self.get_json_diary(date)
        return self.validate(response)
    
    async def get_json_diary(self, date):
        return await EduOrbRequest(self.user).get_json_index_diary(date)

    def validate(self, response: dict):
        return DiaryEduOrbValidator.valdiate_diary(response)
    
    async def get_day_diary(self, date: datetime.datetime):
        diary = await self.get_full_diary(date)
        return self.get_current_day(diary, date)
    
    def get_current_day(self, diary, day: datetime.datetime):
        return diary




class DiaryEduOrbValidator():
    def __init__(self, data: dict):
        self.user = user
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
                    f"Unknown validation error. User: {self.user}. Error: {e}") 
            raise 

    async def raise_bad_reponse_exception(self, response: "FailEduOrbResponse") -> NoReturn:
        error = response.message
        match error:
            case self.EduOrbResponseErrors.ParcipiantNotFound.value:
                raise ParcipiantNotFound
            case _:
                logging.error(
                        f"Unknown server response. User: {self.user}. Error: {error}")
                raise UnknownServerResponse
    
    class EduOrbResponseErrors(Enum):
        ParcipiantNotFound = "Ученик не найден"

    def is_lessons_exists(self, response: "DiaryDataResponse"):
        return (isinstance(response.data, DiaryData) and
                isinstance(response.data.diary, dict))
    
class BaseEduOrbResponse(BaseModel):
    success: bool
    message: str

class DiaryData(BaseModel):
    #TODO: Сделать не list[Lesson], а namedtuple с количественной перменной.ё
    diary: Union[dict[WeekdayWithDate, list["Lesson"]], list[None]]

class FailEduOrbResponse(BaseEduOrbResponse):
    pass

class DiaryDataResponse(BaseEduOrbResponse):
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
