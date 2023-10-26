from typing import Callable, Optional


class FieldDoesNotExists(Exception):
    "Ошибка не существующего поля при создании записи."
    def __init__(self, class_name: Optional[Callable] = None):
        if class_name:
            self.class_name = class_name.__name__
        else:
            self.class_name = "Unknown"

    def __str__(self):
        return f"Данного поля не существует в классе {self.class_name}"
