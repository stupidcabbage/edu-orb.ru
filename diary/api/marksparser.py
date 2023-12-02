from dataclasses import dataclass, field
from typing import Optional

from bs4 import BeautifulSoup, Tag

from diary.api.exceptions import ParcipiantNotFound, TableDoesntExists


@dataclass
class SubjectMarks:
    "Выписка по определенному предмету,"
    name: Optional[str] = None
    grades: list[int] = field(default_factory=list)
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
        if key == "grades":
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
        "column2": "grades",
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
        subject = SubjectMarks()

        mark_rows = await self.find_all_row_marks(row)
        for column in mark_rows:
            self.set_values_to_subject_marks_if_field_exists(subject, column)

        return subject

    async def find_all_row_marks(self, row: Tag) -> list[Tag]:
        return row.find_all(self.ROW_VALUES)
    
    def set_values_to_subject_marks_if_field_exists(self,
                                                    subject: SubjectMarks,
                                                    column: Tag) -> None:
        subject_field = self.get_subject_field_from_column(column)
        if not subject_field:
            return
        setattr(subject, subject_field, column.text)

    def get_subject_field_from_column(self, column: Tag):
        attribute_name = self.get_attribute_name_from_column(column)
        return self.COLUMNS.get(attribute_name)

    def get_attribute_name_from_column(self, column: Tag):
        return column.get("class")[0]

    async def find_marks_table(self):
        table = self.soup.find("table", id="sheet0")
        self.check_table_for_validity(table)
        return table

    def check_table_for_validity(self, table):
        if self.soup.text == "Ученик не найден":
            raise ParcipiantNotFound

        if not table:
            raise TableDoesntExists
