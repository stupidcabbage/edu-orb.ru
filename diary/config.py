import os
from pathlib import Path

from aiogram import Bot
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GOSUSLUGI_LOGIN = os.getenv("login")
GOSUSLUGI_PASSWORD = os.getenv("password")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = "5606704270:AAFOOtIVJX5PE7yDaAtggxXixld7Kmlxm1c"

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
second_bot = TeleBot(TOKEN, parse_mode="html")

EMAIL_REGEX = r"^\S+@\S+\.\S+$"
PHONE_NUMBER_REGEX = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
SNILS_REGEX = r"^\d{1,3}(\s*\d{3})*$"
OAUTH2_REGEX = r"^\d\d\d\d\d\d$"

TEMPLATES_DIR = BASE_DIR / "templates"
