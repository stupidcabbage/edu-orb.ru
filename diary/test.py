import asyncio

from db.services.users import get_user

from diary.api.deeduorb import DeEduOrb
from diary.config import db_session
from diary.services.time import parse_date

user = get_user(db_session, 1122659029)

date = parse_date("01.09.2023")
request = asyncio.run(DeEduOrb(user).get_diary(date=date))
print(request)

