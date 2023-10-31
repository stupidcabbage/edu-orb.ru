from collections.abc import Awaitable, Callable
from typing import Any, Optional, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from diary.config import CURRENT_USER, db_session
from diary.db.models.users import User
from diary.db.services.users import get_user
from diary.telegram.keyboards.signup import SIGNUP_KEYBOARD_AIOGRAM
from diary.templates import render_template


class IsAuthorizedMiddleware(BaseMiddleware):
    "Пользователь уже авторизован."
    async def __call__(
            self,
            handler: Callable[[Union[CallbackQuery, Message], dict[str, Any]], Awaitable[Any]],
            event: Union[CallbackQuery, Message],
            data: dict[str, Any]) -> Any:
        message = event
        if isinstance(event, CallbackQuery):
            user_id = event.message.chat.id
            message = event.message
        else:
            user_id = event.chat.id

        user = get_user(db_session, user_id)
        if not await _is_user_authorized(user, message):
            return

        return await handler(event, data)


class IsHasCurrentUser(BaseMiddleware):
    "Имеется ли выбранный пользователь."
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]) -> Any:
        user = get_user(db_session, event.chat.id)
        
        if user and not await _is_user_has_current_status(user, event):
            return
        
        return await handler(event, data)


class IsAuthorizedAndHasCurrentUser(BaseMiddleware):
    "Авторизован и имеется ли выбранный пользователь."
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]) -> Any:
        user = get_user(db_session, event.chat.id)

        if not await _is_user_authorized(user, event):
            return
        
        if not await _is_user_has_current_status(user, event):
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


async def _is_user_has_current_status(user: User, event: Message) -> bool:
    "Проверяет, что у пользователя стоит хотя бы один current_status для работы."
    if not user.parcipiants_id[CURRENT_USER].is_current:
        await event.answer(await render_template("no_current_user_middleware.j2"))
        return False
    return True


async def _is_user_authorized(user: Optional[User], event: Message) -> bool:
    "Проверяет, что пользователь авторизован - иначе отправляет ошибку."
    if not user:
        await event.answer(await render_template("unauthorized_middleware.j2"),
                           reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
        return False
    return True
