from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


@dataclass
class AuthorizeUser:
    "Класс пользователя для авторизации"
    username: str
    password: str
    telegram_id: int


class User(Base):
    """
    Модель пользователя.

    :param telegram_id int: Уникальный telegram_id пользователя.
    :param phpsessid Optional[str]: Cookie пользователя для входа.
    :param parcipiants_id: List["ParcipiantsID"]: Уникальные айди пользователей на сайте дневника.
    :param created_at datetime: Дата первого отправленного сообщения в бота.
    :param is_admin bool: Является ли пользователем администратором.
    """
    __tablename__ = "user_account"
    __table_args__ = {'extend_existing': True}

    telegram_id: Mapped[int] = mapped_column(primary_key=True,
                                             unique=True)
    "Уникальный telegram_id пользователя."
    phpsessid: Mapped[Optional[str]] = mapped_column()
    "Cookie пользователя для входа."
    parcipiants_id: Mapped[List["ParcipiantsID"]] = relationship(back_populates="user",
                                                                 order_by="desc(ParcipiantsID.is_current)")
    "Уникальные айди пользователей на сайте дневника."
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    "Дата первого отправленного сообщения в бота."
    is_admin: Mapped[bool] = mapped_column(default=False)
    "Является ли пользователем администратором."
    
    def __repr__(self) -> str:
        return f"Пользователь id={self.telegram_id!r} parcipiants_id={self.parcipiants_id!r}"


class ParcipiantsID(Base):
    """
    Уникальные айди пользователей на сайте дневника.
        
    :param parcipiant_id str: Уникальный айди пользователя на сайте дневника для получения данных.
    :param is_current bool: Статус использования данного ID прямо сейчас.
    :param user_id int: Telegram ID пользователя, владеющим данным parcipiant_id.
    :param name str: Фамилия Имя Отчество
    :param grade str: Класс учащегося.
    :param school str: Школа учащегося.
    """
    __tablename__ = "parcipiants_id"
    __table_args__ = {'extend_existing': True}

    parcipiant_id: Mapped[str] = mapped_column(primary_key=True)
    "Уникальный айди пользователя на сайте дневника для получения данных."
    name: Mapped[Optional[str]] = mapped_column()
    "Фамилия Имя Отчество владельца айди"
    grade: Mapped[Optional[str]] = mapped_column()
    "Класс учащегося."
    school: Mapped[Optional[str]] = mapped_column()
    "Школа учащегося."
    is_current: Mapped[bool] = mapped_column(default=True)
    "Статус использования данного ID прямо сейчас"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.telegram_id"))
    "Telegram ID пользователя, владеющим данным parcipiant_id"
    user: Mapped["User"] = relationship(back_populates="parcipiants_id")

    def __repr__(self) -> str:
        return f"name={self.name!r} parcipiant_id={self.parcipiant_id!r}"
