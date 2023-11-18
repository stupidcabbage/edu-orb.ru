import asyncio
import logging
import sys

import sentry_sdk
from aiogram import Dispatcher
from sentry_sdk.integrations.logging import LoggingIntegration

from diary.config import SENTRY_DSN, bot
from diary.telegram.handlers import (authorize, cancel, diary, help, marks,
                                     schedule, start, user)

HANDLERS = (diary.router, cancel.router, start.router, authorize.router,
            user.router, marks.router, schedule.router, help.router)

dp = Dispatcher()


#TODO: переписать логирование в отдельный файл.
def set_logging():
    "Устанавливает логирование в программе."
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("debug.log"),
                logging.StreamHandler(sys.stdout)
                ])
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.WARNING
                )
            ]
    )


async def main() -> None:
    for handler in HANDLERS:
        dp.include_router(handler)

    await dp.start_polling(bot)


if __name__ == "__main__":
    set_logging()
    asyncio.run(main())
