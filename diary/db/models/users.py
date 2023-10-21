from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base


class User(Base):
    "Модель пользователя"
    __tablename__ = "user_account"
    
    telegram_id: Mapped[int] = mapped_column(primary_key=True,
                                             unique=True)
    "Уникальный telegram_id пользователя."
    phpsessid: Mapped[Optional[str]] = mapped_column()
    "Cookie пользователя для входа."
    parcipiants_id: Mapped[List["ParcipiantsID"]] = relationship(back_populates="user")
    "Уникальные айди пользователей на сайте дневника."
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    "Дата первого отправленного сообщения в бота."
    is_admin: Mapped[bool] = mapped_column(default=False)
    "Является ли пользователем администратором."
    
    def __repr__(self) -> str:
        return f"Пользователь id={self.telegram_id!r} parcipiants_id={self.parcipiants_id!r}"


class ParcipiantsID(Base):
    "Уникальные айди пользователей на сайте дневника."
    __tablename__ = "parcipiants_id"
    
    parcipiant_id: Mapped[str] = mapped_column(primary_key=True)
    "Уникальный айди пользователя на сайте дневника для получения данных."
    is_current: Mapped[bool] = mapped_column(default=True)
    "Статус использования данного ID прямо сейчас"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.telegram_id"))
    "Telegram ID пользователя, владеющим данным parcipiant_id"
    user: Mapped["User"] = relationship(back_populates="parcipiants_id")

    def __repr__(self) -> str:
        return f"ID пользователя = {self.user_id!r} с parcipiant_id={self.parcipiant_id!r}, is_currect={self.is_current!r}"
