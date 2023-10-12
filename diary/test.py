from api.diary import get_lessons

from services.user import test_user
import asyncio


async def test_aio():
    a = await get_lessons(date="10.10.2023", user=test_user)
    print(a)
asyncio.run(test_aio())

