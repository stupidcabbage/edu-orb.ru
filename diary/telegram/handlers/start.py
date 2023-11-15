import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from diary.config import CURRENT_USER, db_session
from diary.db.services.users import get_user
from diary.telegram.handlers.message import send_message
from diary.telegram.keyboards import MENU_KEYBOARD, SIGNUP_KEYBOARD_AIOGRAM
from diary.telegram.middlewares.authorize import IsHasCurrentUser
from diary.templates import render_template

router = Router()
router.message.middleware(IsHasCurrentUser())


@router.callback_query(F.data == "start")
async def callback_start(callback: CallbackQuery):
    await start(callback.message, True)
    await callback.answer()


@router.message(CommandStart())
async def command_start(message: Message):
    await start(message)


async def start(message: Message, is_callback: bool = False):
    user = get_user(db_session, message.chat.id) 
    if not user:
        logging.info(f"Unathorized user send start command: {message.chat.id}")
        await send_message(await render_template("unauthorized_start.j2"),
                            message,
                            is_callback,
                            reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
        return

    await send_message(await render_template("authorized_start.j2",
                                               {"user": user.parcipiants_id[CURRENT_USER].name}),
                        message,
                        is_callback,
                        reply_markup=MENU_KEYBOARD())


