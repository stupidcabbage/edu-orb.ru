from typing import Optional

from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.exc import DatabaseError, IntegrityError

from diary.db.exceptions import FieldDoesNotExists
from diary.db.models import User
from diary.db.models.users import ParcipiantsID
from diary.db.sessions import DBsession


def add_user(session: DBsession, model: User, need_flush: bool = True):
    try:
        session.add_model(model, need_flush)
        logger.info(f"Создал модель пользователя: {model}, need_flush={need_flush}")
        session.commit_session(need_close=True)
    except IntegrityError as e:
        logger.warning(f"Не получилось создать пользователя: {e}")
        session.rollback()
        raise FieldDoesNotExists(User)
    except DatabaseError as e:
        logger.warning(f"Не получилось создать пользователя: {e}")
        session.rollback()
        raise


def delete_user(session: DBsession,
                model: User) -> None:
    try:
        user_detele_stmt = delete(User).where(User.telegram_id == model.telegram_id)
        parcipiants_stmt = delete(ParcipiantsID).where(ParcipiantsID.user_id == model.telegram_id)

        session.execute(user_detele_stmt)
        session.execute(parcipiants_stmt)
        session.commit_session(need_close=True)
    except DatabaseError as e:
        logger.warning(f"Не получилось удалить пользователя: {e}")
        session.rollback()
        raise


def get_user(session: DBsession, telegram_id: int) -> Optional[User]:
    stmt = select(User).where(User.telegram_id == telegram_id)
    return session.scalar(stmt)
