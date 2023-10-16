import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

GOSUSLUGI_LOGIN = os.getenv("login")
GOSUSLUGI_PASSWORD = os.getenv("password")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = "5665742116:AAFBdCmms0jGzxKwuobykHZi-40-dpWrjyw"


TEMPLATES_DIR = BASE_DIR / "templates"
