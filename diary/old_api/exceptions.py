import logging


class TableDoesntExists(Exception):
    "Возвращает ошибку, если таблица не найдена."
    def __str__(self):
        message = "Таблица не найдена."
        logging.error(message)
        return message


class ParcipiantNotFound(Exception):
    "Возврашает ошибку, если при запросе ученик не найден."
    def __str__(self):
        message = "Ученик не найден. Возможно токен устарел?"
        logging.error(message)
        return message

class UnknownServerResponse(Exception):
    pass
