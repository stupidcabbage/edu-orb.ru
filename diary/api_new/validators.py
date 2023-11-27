import datetime
import logging
from enum import Enum
from typing import NoReturn, Union

from pydantic import BaseModel, ValidationError

from diary.api_new.exceptions import ParcipiantNotFound, UnknownServerResponse
from diary.db.models import User

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
        if response.data:
            return DiaryDataResponse.data.diary
        return None
    
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
