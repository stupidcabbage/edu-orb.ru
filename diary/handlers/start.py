from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from diary.db.services.users import get_user
from diary.config import db_session
from diary.handlers.keyboards import SIGNUP_KEYBOARD_AIOGRAM
from diary.middlewares.authorize import AuthorizeMiddleware

router = Router()
router.message.middleware(AuthorizeMiddleware())


@router.message(CommandStart())
async def command_start(message: Message):
    if not get_user(db_session, message.chat.id):
        await message.answer("Привет, похоже ты здесь впервые!",
                             reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
        return

    await message.answer(f"Привет, хозяин!")
