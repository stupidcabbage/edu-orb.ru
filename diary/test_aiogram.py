import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import diary

TOKEN = "6578207532:AAG1LuO53xhl3sKEeChzCrrLJADY2CdcvzA"


HANDLERS = (diary.router, )

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    for handler in HANDLERS:
        dp.include_router(handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
