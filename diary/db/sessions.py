from loguru import logger
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from diary.db.models import Base


class DBsession(object):

    _session: Session

    def __init__(self, session: Session, *args, **kwargs):
        self._session = session

    def query(self, *entities, **kwargs):
        return self._session.query(*entities, **kwargs)
    
    def scalar(self, stmt):
        return self._session.scalar(stmt)
    
    def scalars(self, stmt):
        return self._session.scalars(stmt)

    def add_model(self, model: Base, need_flush: bool = False):
        self._session.add(model)
        logger.info("Создал модель")
        
        if need_flush:
            self._session.flush([model])
            logger.info("flushed")

    def delete_model(self, model: Base):
        if model is None:
            logger.warning(f"{__name__}: model is None")

        try:
            self._session.delete(model)
        except IntegrityError as e:
            logger.error(f"{__name__} {e}")
        except DataError as e:
            logger.error(f"{__name__} {e}")

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as e:
            logger.error(f"{__name__} {e}")
            raise
        except DataError as e:
            logger.error(f"{__name__} {e}")
            raise
        
        if need_close:
            self.close_session()

    def close_session(self):
        try:
            self._session.close()
        except IntegrityError as e:
            logger.error(f"{__name__} {e}")
            raise
        except DataError as e:
            logger.error(f"{__name__} {e}")
            raise
