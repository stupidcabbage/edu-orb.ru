from dataclasses import dataclass
from typing import LiteralString


from diary.config import GOSUSLUGI_LOGIN, GOSUSLUGI_PASSWORD


@dataclass
class User:
    username: LiteralString
    password: LiteralString
    parcipiant_id: str | None = None
    cookies: dict | None = None


test_user = User(
        username=GOSUSLUGI_LOGIN,
        password=GOSUSLUGI_PASSWORD,
        parcipiant_id="A7A48C5F8B939B82826487956E3FA893",
        cookies={"PHPSESSID": "1cdefad789a784d074daae150d782b0f"})
