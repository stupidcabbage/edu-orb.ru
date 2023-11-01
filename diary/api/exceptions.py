class TableDoesntExists(Exception):
    def __str__(self):
        return f"Таблица не найдена."


class ParcipiantNotFound(Exception):
    def __str__(self):
        return f"Ученик не найден. Возможно токен устарел?"

