import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers import authorize, diary, start

TOKEN = "5665742116:AAFBdCmms0jGzxKwuobykHZi-40-dpWrjyw"

HANDLERS = (diary.router, start.router, authorize.router, )


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    for handler in HANDLERS:
        dp.include_router(handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
