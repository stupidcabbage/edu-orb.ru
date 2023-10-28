from typing import Callable, Optional


class FieldDoesNotExists(Exception):
    "Ошибка не существующего поля при создании записи."
    def __init__(self, object: Optional[Callable] = None):
        if object:
            self.class_name = object.__name__
        else:
            self.class_name = "Unknown"

    def __str__(self):
        return f"Данного поля не существует в классе {self.class_name}"
