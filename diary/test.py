from typing import Callable, Optional

from sqlalchemy import create_engine, select
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from db.models import Base
from db.models.users import ParcipiantsID, User

meta = Base.metadata

engine = create_engine("sqlite+pysqlite:///db.sqlite3")

session = Session(engine)


class FieldDoesNotExists(Exception):
    "Ошибка не существующего поля при создании записи."
    def __init__(self, class_name: Optional[Callable] = None):
        if class_name:
            self.class_name = class_name.__name__
        else:
            self.class_name = "Unknown"

    def __str__(self):
        return f"Данного поля не существует в классе {self.class_name}"

def init_models() -> None:
    "Создание всех моделей."
    meta.create_all(engine)


def create_user(**kwargs) -> None:
    "Создает модель пользователя в БД."
    try:
        user = User(**kwargs)
    except TypeError:
        raise FieldDoesNotExists(User)

    try:
        with session:
            session.add(user)
            session.commit()
    except DBAPIError as error:
        print(f"Ошибка при добавлении: {error}")


def get_user(telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id)
    return session.scalar(stmt)


def main():
    # init_models()

    parcipiant_id=[ParcipiantsID(parcipiant_id="asdasd")]

    print(create_user(telegram_id=2))
    print(get_user(2))



# if __name__ == "__main__":
#     main()
user = User(telegram_id=123)
print(user.telegram_id)

# User.metadata.create_all(engine)
# ParcipiantsID.metadata.create_all(engine)
#
# parcipiant_id=[ParcipiantsID(parcipiant_id="asdasd")]
# user = User(telegram_id=1,
#             parcipiants_id=parcipiant_id)
#
# with Session(engine) as session:
#     session.add(user)
#     session.commit()
#
#
# session = Session(engine)
#
# stmt = select(User) 
# print(stmt)
# user = session.scalars(stmt).all()
# print(user[0].parcipiants_id)
