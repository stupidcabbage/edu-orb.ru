import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from aiogram import Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot

from diary.db.sessions import DBsession

load_dotenv()


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class EnvToken(ABC):
    @abstractmethod
    def token(self) -> str:
        pass
    
    def get_token_from_env(self, key: str, default = None) -> Any:
        return os.getenv(key, default)

    def raise_exception_if_token_does_not_exists(self,
                                                 token: Optional[str]) -> Optional[TypeError]:
        if not token:
            raise self.ObligatoryTokenDoesNotExists

    class ObligatoryTokenDoesNotExists(Exception):
        def __str__(self):
            return "Obligatory token does not exists! Check env file."


class TelegramToken(EnvToken):
    def token(self) -> str:
        token = self.get_token_from_env("BOT_TOKEN")
        self.raise_exception_if_token_does_not_exists(token)
        return token


class SentryDSNToken(EnvToken):
    def token(self) -> str:
        token = self.get_token_from_env("SENTRY_DSN")
        self.raise_exception_if_token_does_not_exists(token)
        return token


class AiogramBot(Bot):
    def __init__(self, *args, **kwargs):
        self.env_token = TelegramToken().token()
        self.parse_mode = ParseMode.HTML
        super().__init__(self.env_token, parse_mode=self.parse_mode, *args, **kwargs)

class AiogramBotSender(AiogramBot, metaclass=MetaSingleton):
    pass

class TelebotBot(TeleBot, metaclass=MetaSingleton):
    def __init__(self, *args, **kwargs):
        self.env_token = TelegramToken().token()
        self.parse_mode = "HTML"
        super().__init__(self.env_token, parse_mode=self.parse_mode, *args, **kwargs)


BASE_DIR = Path(__file__).resolve().parent

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
