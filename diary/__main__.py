import asyncio
import logging
import sys

from aiogram import Dispatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from diary.config import bot
from diary.db.sessions import DBsession
from diary.handlers import authorize, cancel, diary, start

HANDLERS = (diary.router, cancel.router, start.router, authorize.router)

dp = Dispatcher()

async def main() -> None:
    for handler in HANDLERS:
        dp.include_router(handler)

    await dp.start_polling(bot)

def start_db():
    engine = create_engine("sqlite+pysqlite:///db.sqlite3")
    session_factory = sessionmaker(bind=engine)
    db_session = DBsession(session_factory())
    return db_session

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    db_session = start_db()
    asyncio.run(main())
