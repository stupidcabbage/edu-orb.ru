from typing import Any, Dict, Union

from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from diary.config import db_session
from diary.db.services.users import get_user


class AuthorizeFilter(BaseFilter):
    "Пользователь проходит авторизацию."
    async def __call__(self, callback: CallbackQuery,
                       state: FSMContext) -> Union[bool, Dict[str, Any]]:
        if await state.get_state():
            await callback.answer("Ты проходишь авторизацию!",
                                  show_alert=True)
            return False
        return True


class IsAuthorizedFilter(BaseFilter):
    "Пользователь уже авторизован."
    async def __call__(self, callback: CallbackQuery) -> Union[bool, Dict[str, Any]]:
        if get_user(db_session, callback.message.chat.id):
            await callback.answer("Ты уже авторизован!",
                                  show_alert=True)
            return False
        return True
