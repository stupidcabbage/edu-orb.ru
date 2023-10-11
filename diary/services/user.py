from dataclasses import dataclass
from typing import LiteralString


from diary.config import GOSUSLUGI_LOGIN, GOSUSLUGI_PASSWORD


@dataclass
class User:
    username: LiteralString
    password: LiteralString
    parcipiant_id: str | None = None


test_user = User(
        username=GOSUSLUGI_LOGIN,
        password=GOSUSLUGI_PASSWORD)
