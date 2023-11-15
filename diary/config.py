import os
from pathlib import Path

from aiogram import Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot

from diary.db.sessions import DBsession

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GOSUSLUGI_LOGIN = os.getenv("login")
GOSUSLUGI_PASSWORD = os.getenv("password")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
SENTRY_DSN = os.getenv("DSN")

bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
second_bot = TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="html")

CURRENT_USER = 0

EMAIL_REGEX = r"^\S+@\S+\.\S+$"
PHONE_NUMBER_REGEX = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
SNILS_REGEX = r"^\d{1,3}(\s*\d{3})*$"
OAUTH2_REGEX = r"^\d\d\d\d\d\d$"

TEMPLATES_DIR = BASE_DIR / "templates"
PATH_TO_DB = f"{BASE_DIR.parent}/db.sqlite3"


engine = create_engine(f"sqlite+pysqlite:///{PATH_TO_DB}")
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
db_session = DBsession(session_factory())
