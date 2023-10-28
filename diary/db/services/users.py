from loguru import logger
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, IntegrityError

from diary.db.exceptions import FieldDoesNotExists
from diary.db.models import User
from diary.db.sessions import DBsession


def add_user(session: DBsession, model: User, need_flush: bool = True):
    try:
        session.add_model(model, need_flush)
        logger.info(f"Создал модель пользователя: {model}, need_flush={need_flush}")
    except IntegrityError as e:
        logger.warning(f"Не получилось создать пользователя: {e}")
        raise FieldDoesNotExists(User)
    except DatabaseError as e:
        logger.warning(f"Не получилось создать пользователя: {e}")
        raise


def get_user(session: DBsession, telegram_id: int):
    stmt = select(User).where(User.telegram_id == telegram_id)
    return session.scalar(stmt)
