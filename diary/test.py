import asyncio
from datetime import datetime

from api.marks import get_marks
from config import db_session
from db.services.users import get_user

NIKITA = 1176535980
VANYA = 1122659029
user = get_user(db_session, VANYA)

async def main():
    start_time = datetime.now()
    marks = await get_marks("01.09.2023", "28.10.2023", user)
    end_time = datetime.now()
    for i in marks:
        print(i)
    print(end_time - start_time)

asyncio.run(main())
