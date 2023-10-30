from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from diary.config import db_session
from diary.db.services.users import get_user
from diary.telegram.keyboards.signup import SIGNUP_KEYBOARD_AIOGRAM
from diary.templates import render_template


class IsAuthorizedMiddleware(BaseMiddleware):
    "Пользователь уже авторизован."
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]) -> Any:
        if not get_user(db_session, event.chat.id):
            await event.answer(await render_template("unauthorized_middleware.j2"),
                               reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
            return

        return await handler(event, data)


class AuthorizeMiddleware(BaseMiddleware):
    "Пользователь проходит авторизацию."
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]) -> Any:
        if await data["state"].get_state():
            await event.answer("Ты проходишь авторизацию!")
            return

        return await handler(event, data)

