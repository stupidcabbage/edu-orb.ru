from datetime import datetime
from typing import Sequence

from sqlalchemy import func, select

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


def get_count_grades(
        session: DBsession, subject: str, date: datetime,
        parcipiant: ParcipiantsID) -> int:
    """
    Возвращает кол-во оценок (не считая пропуски, болезни),
    начиная с переданной даты. 

    :param session DBsession: Сессия БД.
    :param subject str: Предмет, по которому производится выборка.
    :param date datetime: Дата, с которой производится выборка.
    :param parcipiant ParcipiantsID: Оценки ученика. 
    :param lesson_number int: Номер урока.
    """
    stmt = (
            select(func.count(Mark.id)).
            where(Mark.subject == subject).
            where(date <= Mark.date).
            where(Mark.parcipiant == parcipiant).
            where(5 >= Mark.mark)
    )
    return session.scalar(stmt)


def _get_count_absence_subject(
        x: int, session: DBsession, subject: str, date: datetime,
        parcipiant: ParcipiantsID) -> int:
    """
    Возвращает кол-во переданного absence, начиная с переданной даты. 

    :param session DBsession: Сессия БД.
    :param subject str: Предмет, по которому производится выборка.
    :param date datetime: Дата, с которой производится выборка.
    :param parcipiant ParcipiantsID: Оценки ученика. 
    :param lesson_number int: Номер урока.
    """
    stmt = (
            select(func.count(Mark.id)).
            where(Mark.subject == subject).
            where(date <= Mark.date).
            where(Mark.parcipiant == parcipiant).
            where(x == Mark.mark)
    )
    return session.scalar(stmt)


def get_count_noshow_subject(
        session: DBsession, subject: str, date: datetime,
        parcipiant: ParcipiantsID) -> int:
    """
    Возвращает кол-во неявок по определенному предмету,
    начиная с переданной даты. 

    :param session DBsession: Сессия БД.
    :param subject str: Предмет, по которому производится выборка.
    :param date datetime: Дата, с которой производится выборка.
    :param parcipiant ParcipiantsID: Оценки ученика. 
    :param lesson_number int: Номер урока.
    """
    return _get_count_absence_subject(6, session, subject, date, parcipiant)


def get_count_illes_subject(
        session: DBsession, subject: str, date: datetime,
        parcipiant: ParcipiantsID) -> int:
    """
    Возвращает кол-во болезней по определенному предмету,
    начиная с переданной даты. 

    :param session DBsession: Сессия БД.
    :param subject str: Предмет, по которому производится выборка.
    :param date datetime: Дата, с которой производится выборка.
    :param parcipiant ParcipiantsID: Оценки ученика. 
    :param lesson_number int: Номер урока.
    """
    return _get_count_absence_subject(8, session, subject, date, parcipiant)


def get_count_passes_subject(
        session: DBsession, subject: str, date: datetime,
        parcipiant: ParcipiantsID) -> int:
    """
    Возвращает кол-во пропусков по определенному предмету,
    начиная с переданной даты. 

    :param session DBsession: Сессия БД.
    :param subject str: Предмет, по которому производится выборка.
    :param date datetime: Дата, с которой производится выборка.
    :param parcipiant ParcipiantsID: Оценки ученика. 
    :param lesson_number int: Номер урока.
    """
    return _get_count_absence_subject(7, session, subject, date, parcipiant)


def is_mark_exists(session: DBsession, mark: Mark):
    """
    Возвращает True, если оценка существует. False - если не существует.

    :param session DBsession: Сессия БД.
    :param mark Mark: Отметка
    """
    stmt = (
            select(func.count()).
            select_from(Mark).
            where(Mark.subject == mark.subject).
            where(Mark.date == mark.date).
            where(Mark.parcipiant_id == mark.parcipiant_id).
            where(Mark.lesson_number == mark.lesson_number)
    )
    return session.scalar(stmt)

def bulk_add_marks(session: DBsession, models: list[Mark], need_flush: bool = False):
    "Добавить оценки списком."
    for mark in models:
        session.add_model(mark, need_flush)
    session.commit_session(True)


def add_mark(session: DBsession, model: Mark, need_flush: bool = False):
    "Добавить в БД модель оценки пользователя"
    session.add_model(model, need_flush)
    session.commit_session(True)
