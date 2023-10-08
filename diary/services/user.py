from dataclasses import dataclass
from typing import LiteralString
from dotenv import load_dotenv
import os


load_dotenv()


@dataclass
class User:
    username: LiteralString
    password: LiteralString
    parcipiant_id: str | None = None

test_user = User(
        username=os.getenv("login"),
        password=os.getenv("password")
        )
