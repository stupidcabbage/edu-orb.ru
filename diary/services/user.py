from dataclasses import dataclass

from diary.config import GOSUSLUGI_LOGIN, GOSUSLUGI_PASSWORD


@dataclass
class User:
    username: str
    password: str
    telegram_id: int
    parcipiant_id: str | None = None
    cookies: dict | None = None


test_user = User(
        username=GOSUSLUGI_LOGIN,
        password=GOSUSLUGI_PASSWORD,
        telegram_id=1122659029,
        parcipiant_id="A7A48C5F8B939B82826487956E3FA893",
        cookies={"PHPSESSID": "1cdefad789a784d074daae150d782b0f"})
