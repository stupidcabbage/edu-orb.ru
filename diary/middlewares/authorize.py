from collections.abc import Awaitable, Callable
from typing import Any, Dict, Union

from aiogram import BaseMiddleware
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, TelegramObject

from diary.db.services.users import get_user
from diary.config import db_session



class IsAuthorizedMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]) -> Any:
        if not get_user(db_session, event.chat.id):
            await event.answer("Ты не авторизован!")
            return

        return await handler(event, data)

class AuthorizeFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, state: FSMContext) -> Union[bool, Dict[str, Any]]:
        if await state.get_state():
            await callback.answer("Ты проходишь авторизацию!",
                                  show_alert=True)
            return False
        return True


class AuthorizeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]) -> Any:
        if await data["state"].get_state():
            await event.answer("Ты проходишь авторизацию!")
            return

        return await handler(event, data)

