import asyncio
from config import db_session
from db.services.users import get_user
from diary.api.schoolperiods import get_school_periods

NIKITA = 1176535980
VANYA = 1122659029
user = get_user(db_session, VANYA)

async def main():
    a = await get_school_periods(user)
    print(a)

asyncio.run(main())
