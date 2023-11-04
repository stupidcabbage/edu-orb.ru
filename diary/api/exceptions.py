class TableDoesntExists(Exception):
    "Возвращает ошибку, если таблица не найдена."
    def __str__(self):
        return f"Таблица не найдена."


class ParcipiantNotFound(Exception):
    "Возврашает ошибку, если при запросе ученик не найден."
    def __str__(self):
        return f"Ученик не найден. Возможно токен устарел?"

