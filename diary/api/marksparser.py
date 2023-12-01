from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup, Tag

from diary.api.exceptions import ParcipiantNotFound, TableDoesntExists


@dataclass
class SubjectMarks:
    "Класс оценок по определенному предмету,"
    name: Optional[str] = None
    marks: Optional[list[int]] = None
    middle_marks: float = 0.0
    noshow: int = 0
    passes: int = 0
    illes: int = 0
        
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

class MarksParser:
    TABLE_FIELDS = "tr"
    "Все поля таблицы с данными."
    ROW_VALUES = "td"
    "Строчки оценок"
    SUBJECTS_ROWS = 4
    "Значение, с которого начинают идти оценки."
    COLUMNS = {
        "column1": "name",
        "column2": "marks",
        "column3": "middle_marks",
        "column4": "noshow",
        "column5": "passes",
        "column6": "illes"
    }
    "Значение колонок и аттрибутов класса Subject"

    def __init__(self, html_data: str):
        self.html_data = html_data
        self.soup = BeautifulSoup(self.html_data, "lxml")
        self.subjects = []

    async def get_marks(self) -> list[SubjectMarks]:
        self.table = await self.find_marks_table()
        await self.find_subjects_marks()
        return self.subjects

    async def find_subjects_marks(self) -> None:
        rows = await self.find_all_table_rows()

        for row in rows:
            await self.append_subjects(row)
    
    async def find_all_table_rows(self):
        return self.table.find_all(self.TABLE_FIELDS)[self.SUBJECTS_ROWS:]
    
    async def append_subjects(self, row):
        subject = await self.make_subject(row)
        if subject:
            self.subjects.append(subject)

    async def make_subject(self, row: Tag) -> SubjectMarks:
        "Возвращает объект класса SubjectMarks с полученных данных строки."
        row = row.find_all(self.ROW_VALUES)
        subject = SubjectMarks()
        for column in row:
            attribute_name = column.get("class")[0]
            subject_field = self.COLUMNS.get(attribute_name)
            if not subject_field:
                continue
            setattr(subject, subject_field, column.text)

        return subject

    async def find_marks_table(self):
        table = self.soup.find("table", id="sheet0")
        self.check_table_for_validity(table)
        return table

    def check_table_for_validity(self, table):
        if not table:
            raise TableDoesntExists

        if self.soup.text == "Ученик не найден":
            raise ParcipiantNotFound
