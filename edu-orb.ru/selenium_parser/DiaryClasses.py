from typing import Iterable
from dataclasses import dataclass
import datetime


@dataclass
class Homework:
    "Домашнее задание."
    task: str
    "Задание."
    attachments: str | None = None # Path
    "Путь до файлов с вложениями."


@dataclass
class Lesson:
    "Урок."
    count: int
    "Какой урок по счету в расписании."
    subject: str
    "Название предмета."
    topic: str | None = None
    "Тема урока."
    homework: Homework | None = None 
    "Домашнее задание."
    mark: int | None = None
    "Оценка за урок."


@dataclass
class WorkDay:
    date: datetime.datetime
    "Дата урока."
    lessons: Iterable[Lesson]
    "Уроки."
