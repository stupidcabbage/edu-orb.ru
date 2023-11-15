import logging
from typing import Optional, Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from diary.db.models import Mark
from diary.db.models.users import ParcipiantsID
from diary.db.sessions import DBsession


def get_db_subject_marks(session: DBsession,
                 subject: str,
                 date: datetime,
                 parcipiant: ParcipiantsID) -> Sequence[Mark]:
    """
    Получить из БД оценки пользователя по определенному предмету

    :param session DBsession: Сессия БД.
    :param subject str: Предмет, по которому производится выборка.
    :param date datetime: Дата, с которой производится выборка.
    :param parcipiant ParcipiantsID: Оценки ученика. 
    """
    stmt = (
            select(Mark).
            where(Mark.subject == subject).
            where(Mark.date == date).
            where(Mark.parcipiant == parcipiant)
    )
    return session.scalars(stmt).all()


def is_subject_mark_exists(session: DBsession, mark: Mark) -> bool:
    """
    Возвращает True, если оценка существует. False - если не существует.

    :param session DBsession: Сессия БД.
    :param subject str: Предмет, по которому производится выборка.
    :param date datetime: Дата, с которой производится выборка.
    :param parcipiant ParcipiantsID: Оценки ученика. 
    :param lesson_number int: Номер урока.
    """
    stmt = (
            select(Mark).
            where(Mark.subject == mark.subject).
            where(Mark.date == mark.date).
            where(Mark.parcipiant == mark.parcipiant).
            where(Mark.lesson_number == mark.lesson_number)
    ).exists()
    return session.query(stmt)


def add_mark(session: DBsession, model: Mark, need_flush: bool = False):
    "Добавить в БД модель оценки пользователя"
    session.add_model(model, need_flush)
    try:
        session.commit_session(True)
    except Exception:
        session.rollback()
