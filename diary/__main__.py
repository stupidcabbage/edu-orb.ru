import asyncio
import logging
import sys

from aiogram import Dispatcher
from diary.config import bot
from diary.telegram.handlers import authorize, cancel, diary, start

HANDLERS = (diary.router, cancel.router, start.router, authorize.router)

dp = Dispatcher()


async def main() -> None:
    for handler in HANDLERS:
        dp.include_router(handler)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
