from sqlalchemy import create_engine, select
from db.models.users import User, ParcipiantsID
from sqlalchemy.orm import Session


engine = create_engine("sqlite+pysqlite:///:memory:")

User.metadata.create_all(engine)
ParcipiantsID.metadata.create_all(engine)

parcipiant_id=[ParcipiantsID(parcipiant_id="asdasd")]
user = User(telegram_id=1,
            parcipiants_id=parcipiant_id)

with Session(engine) as session:
    session.add(user)
    session.commit()


session = Session(engine)

stmt = select(User) 
print(stmt)
user = session.scalars(stmt).all()
print(user[0].parcipiants_id)
