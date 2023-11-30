import asyncio
import logging
import sys
from typing import NoReturn

from aiogram import Dispatcher

from diary.old_api.notification import MarkNotification
from diary.config import AiogramBot
from diary.telegram.handlers import (authorize, cancel, diary, help, marks,
                                     schedule, start, test, user)
from diary.telegram.handlers.notifications import notification

HANDLERS = (diary.router, cancel.router, start.router, authorize.router,
            user.router, marks.router, schedule.router, help.router,
            notification.router, test.router)

dp = Dispatcher()


#TODO: переписать логирование в отдельный файл.
#TODO: разделить по классам и функциям.
def set_logging():
    "Устанавливает логирование в программе."
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("debug.log"),
                logging.StreamHandler(sys.stdout)
                ])
    # sentry_sdk.init(
        # dsn=SentryDSNToken().token(),
        # traces_sample_rate=1.0,
        # profiles_sample_rate=1.0,
        # integrations=[
            # LoggingIntegration(
                # level=logging.INFO,
                # event_level=logging.WARNING
                # )
            # ]
    # )

def start_notification_poiling():
    worker = MarkNotification()
    asyncio.run(worker.start_poiling())

async def main() -> NoReturn:
    for handler in HANDLERS:
        dp.include_router(handler)

    await dp.start_polling(AiogramBot())


if __name__ == "__main__":
    set_logging()
    # process = multiprocessing.Process(target=start_notification_poiling)
    # process.start()
    asyncio.run(main())
