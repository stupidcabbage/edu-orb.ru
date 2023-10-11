from dataclasses import dataclass
from typing import LiteralString
from dotenv import load_dotenv

from diary.config import GOSUSLUGI_LOGIN, GOSUSLUGI_PASSWORD


load_dotenv()


@dataclass
class User:
    username: LiteralString
    password: LiteralString
    parcipiant_id: str | None = None


test_user = User(
        username=GOSUSLUGI_LOGIN,
        password=GOSUSLUGI_PASSWORD))
