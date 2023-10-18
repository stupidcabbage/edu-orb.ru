import asyncio
import logging
import sys

from aiogram import Dispatcher

from diary.handlers import authorize, diary, start
from diary.config import bot

HANDLERS = (diary.router, start.router, authorize.router, )

dp = Dispatcher()

async def main() -> None:
    for handler in HANDLERS:
        dp.include_router(handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
