from sqlalchemy import update

from diary.config import db_session
from diary.db.models.users import ParcipiantsID
from diary.db.sessions import DBsession


def change_current_status(session: DBsession,
                          telegram_id: int,
                          parcipiant_id: str,
                          is_current: bool) -> None:
    stmt = (
            update(ParcipiantsID)
            .where(ParcipiantsID.user_id == telegram_id)
            .where(ParcipiantsID.parcipiant_id == parcipiant_id)
            .values(is_current = is_current)
            )
    session.execute(stmt)
 

def change_user_current_status(user, parcipiant_number):
    for i, parcipiant_id in enumerate(user.parcipiants_id):
        is_current = False
        if i == int(parcipiant_number):
            is_current = True
        change_current_status(db_session,
                              user.telegram_id,
                              parcipiant_id=parcipiant_id.parcipiant_id,
                              is_current=is_current)
    db_session.commit_session()
