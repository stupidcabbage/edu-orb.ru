import logging
from typing import Optional, Sequence

from sqlalchemy import delete, select, update

from diary.db.models import User
from diary.db.models.users import Mark, ParcipiantsID
from diary.db.sessions import DBsession


def add_user(session: DBsession, model: User, need_flush: bool = True):
    """
    добавляет пользователя в бд.
    
    :param session dbsession: сессия бд.
    :param user user: модель пользователя, которую создаем.
    :param need_flush: нужда в проверке.
    """
    session.add_model(model, need_flush)
    session.commit_session(need_close=True)

def set_notification_status(session: DBsession, user: User, status: bool = False):
    """
    Установить статус уведомлений

    :param session DBsession: сессия БД.
    :param user User: пользователь, у которого меняем параметр.
    :param status bool: новое состояние.
    """
    logging.info(f"Update notification status for {user.telegram_id} to {status}")
    stmt = (
            update(User).
            where(User.telegram_id == user.telegram_id).
            values(notification_status=status)
    )
    session.execute(stmt)
    session.commit_session(True)


def delete_user(session: DBsession,
                model: User) -> None:
    """
    Удалить пользователя (а также все объекты, связанные с ним) из БД

    :param session DBsession: сессия БД.
    :param user User: пользователь, у которого меняем параметр.
    """
    logging.info(f"Deleted user: {model}")
    user_detele_stmt = delete(User).where(User.telegram_id == model.telegram_id)
    marks_stmt = (
            delete(Mark).
            where(Mark.parcipiant_id == model.current_parcipiant().parcipiant_id)
    )
    parcipiants_stmt = delete(ParcipiantsID).where(ParcipiantsID.user_id == model.telegram_id)

    session.execute(user_detele_stmt)
    session.execute(marks_stmt)
    session.execute(parcipiants_stmt)
    session.commit_session(need_close=True)

def get_user_for_notification(session: DBsession) -> Sequence[User]:
    "Возвращает список пользователей, которые подписаны на уведомления."
    stmt = select(User).where(User.notification_status == True)
    return session.scalars(stmt).all()

def get_user(session: DBsession, telegram_id: int) -> Optional[User]:
    """
    Получить модель пользователя из БД.

    :param session DBsession: сессия БД.
    :param telegram_id int: Уникальный айди пользователя в телеграмм.
    """
    stmt = select(User).where(User.telegram_id == telegram_id)
    return session.scalar(stmt)
