import logging

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
        logging.info(f"Created model: {model}")
        
        if need_flush:
            self._session.flush([model])

    def rollback(self):
        logging.info(f"Session rollback")
        self._session.rollback()

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
            logging.info(f"Commit session")
        except Exception as e:
            self.rollback()
            logging.critical(f"{__name__} {e}")
            raise
        
        if need_close:
            self.close_session()

    def execute(self, stmt):
        self._session.execute(stmt)

    def close_session(self):
        try:
            logging.info(f"Close session")
            self._session.close()
        except IntegrityError as e:
            logging.critical(f"{__name__} {e}")
            raise
        except DataError as e:
            logging.critical(f"{__name__} {e}")
            raise
