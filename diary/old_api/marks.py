from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from diary.api.exceptions import ParcipiantNotFound, TableDoesntExists
from diary.old_api.response import get_text_response
from diary.config import CURRENT_USER
from diary.db.models import User
from diary.services.time import format_date

ROW_VALUES = "td"
"Строчки оценок"
SUBJECTS_ROWS = 4
"Значение, с которого начинают идти оценки."

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX"
}

COLUMNS = {
    "column1": "name",
    "column2": "marks",
    "column3": "middle_marks",
    "column4": "noshow",
    "column5": "passes",
    "column6": "illes"
}
"Значение колонок и аттрибутов класса Subject"


#DO сделать datetime
@dataclass
class SubjectMarks:
    """
    Класс оценок по определенному предмету.
    :param name Optional[str]: Название предмета.
    :param marks list[int]: Оценки.
    :param middle_marks float: Средний балл.
    :param noshow int: Количество неявок.
    :param passes int: Количество пропусков.
    :param illes int: Количество пропусков по болезни.
    """
    name: Optional[str] = None
    "Название предмета"
    marks: Optional[list[int]] = None
    "Оценки"
    middle_marks: float = 0.0
    "Средний балл"
    noshow: int = 0
    "Неявка"
    passes: int = 0
    "Пропуск"
    illes: int = 0
    "Болезнь"
        
    def _to_list(self, value) -> list[int] | None:
        if self._value_exists(value):
            return list(map(int, value.split(", ")))
        return []

    def _to_int(self, value) -> Optional[int]:
        if self._value_exists(value):
            return int(value)
        return 0

    def _to_float(self, value) -> Optional[float]:
        if self._value_exists(value):
            return float(value)
        return 0.0
    
    def _value_exists(self, value):
        return value and value != "нет"

    def __setattr__(self, key, value):
        if key == "marks":
            self.__dict__[key] = self._to_list(value)
        elif key in ("noshow", "passes", "illes"):
            self.__dict__[key] = self._to_int(value)
        elif key == "middle_marks":
            self.__dict__[key] = self._to_float(value)
        else:
            super().__setattr__(key, value)

async def get_marks(date_begin: datetime, date_end: datetime, user: User) -> list[SubjectMarks]:
    """
    Возвращает оценки ввиде списка, состоящего из объектов вида SubjectMarks.
    :param date_begin datetime: Дата начала выборки (DD.MM.YYYY).
    :param date_end datetime: Дата конца выборки (DD.MM.YYYY).
    :param user User: Пользователь, который делает запрос.
    """
    html_text = await get_marks_html(format_date(date_begin), format_date(date_end), user)
    return await make_list_subjects(html_text)


async def get_marks_html(date_begin: str, date_end: str, user: User):
    """
    Возвращает оценки в формате HTML.
    :param date_begin str: Дата начала выборки (DD.MM.YYYY).
    :param date_end str: Дата конца выборки (DD.MM.YYYY).
    :param user User: Пользователь, который делает запрос.
    """
    cookies = {"PHPSESSID": f"{user.phpsessid}"}
    parcipiant_id = user.parcipiants_id[CURRENT_USER].parcipiant_id
    url = f"https://de.edu.orb.ru/edv/index/report/marks/{parcipiant_id}?begin={date_begin}&end={date_end}&format=html"
    return await get_text_response(url, cookies)


async def make_list_subjects(html_text) -> list[SubjectMarks]:
    "Парсит информацию с HTML."
    soup = BeautifulSoup(html_text, "lxml")
    table = soup.find("table", id="sheet0")

    if not table:
        if soup.text == "Ученик не найден":
            raise ParcipiantNotFound
        raise TableDoesntExists

    rows = table.find_all("tr")[SUBJECTS_ROWS:]
    subjects = []
    for row in rows:
        subject = await make_subject(row)
        if subject:
            subjects.append(subject)

    return subjects


async def make_subject(row: Tag) -> SubjectMarks:
    "Возвращает объект класса SubjectMarks с полученных данных строки."
    row = row.find_all(ROW_VALUES)
    subject = SubjectMarks()
    for column in row:
        attribute_name = column.get("class")[0]
        subject_field = COLUMNS.get(attribute_name)
        if not subject_field:
            continue
        setattr(subject, subject_field, column.text)

    return subject
