class TableDoesntExists(Exception):
    "Возвращает ошибку, если таблица не найдена."
    def __str__(self):
        message = "Таблица не найдена."
        return message


class ParcipiantNotFound(Exception):
    "Возврашает ошибку, если при запросе ученик не найден."
    def __str__(self):
        message = "Ученик не найден. Возможно токен устарел?"
        return message

class UnknownServerResponse(Exception):
    pass

class PeriodHasIncorrectParametersCount(Exception):
    pass

class PeriodIsNotDatetime(Exception):
    pass
