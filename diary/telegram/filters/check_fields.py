import re
from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.types import Message
from emoji import EMOJI_DATA
from diary.config import EMAIL_REGEX, PHONE_NUMBER_REGEX, SNILS_REGEX

from diary.templates import render_template


class OnlyTextMessageFilter(BaseFilter):
    "Пользователь проходит авторизацию."
    async def __call__(self, message: Message) -> bool:
        """
        Проверяет, что сообщение состоит только из символов:
        латинского алфавита / кириллицы / знаки препинания.
        """ 
        if message.content_type is not types.ContentType.TEXT:
            await send_incorrect_data_message(message)
            return False

        if message.text in EMOJI_DATA:
            await send_incorrect_data_message(message)
            return False

        for letter in message.text:
            if letter in EMOJI_DATA:
                await send_incorrect_data_message(message)
                return False

        return True

class LoginFilter(OnlyTextMessageFilter):
    async def __call__(self, message: Message) -> bool:
        if not await super().__call__(message):
            return False

        if not is_login_correct(message.text):
            await send_incorrect_data_message(message)
            return False
        return True


def is_login_correct(login: str):
    return (bool(re.match(EMAIL_REGEX, login))
            or bool(re.match(PHONE_NUMBER_REGEX, login))
            or bool(re.match(SNILS_REGEX, login)))

async def send_incorrect_data_message(message: Message):
    await message.answer(await render_template(
        "incorrect_data.j2", {"field": "логин"}))
