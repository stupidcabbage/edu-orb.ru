from dataclasses import dataclass
from typing import LiteralString

import os


@dataclass
class User:
    username: LiteralString
    password: LiteralString


test_user = User(
        username=os.getenv("username"),
        password=os.getenv("password")
        )
