import os
from pathlib import Path


from aiogram import Bot
from dotenv import load_dotenv

from aiogram.enums import ParseMode

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GOSUSLUGI_LOGIN = os.getenv("login")
GOSUSLUGI_PASSWORD = os.getenv("password")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = "5665742116:AAFBdCmms0jGzxKwuobykHZi-40-dpWrjyw"

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

TEMPLATES_DIR = BASE_DIR / "templates"
