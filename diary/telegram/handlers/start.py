from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from diary.config import CURRENT_USER, db_session
from diary.db.services.users import get_user
from diary.telegram.keyboards import SIGNUP_KEYBOARD_AIOGRAM
from diary.telegram.keyboards import MENU_KEYBOARD
from diary.telegram.middlewares.authorize import IsHasCurrentUser
from diary.templates import render_template

router = Router()
router.message.middleware(IsHasCurrentUser())


@router.message(CommandStart())
async def command_start(message: Message):
    user = get_user(db_session, message.chat.id) 
    if not user:
        await message.answer(await render_template("unauthorized_start.j2"),
                             reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
        return

    await message.answer(await render_template("authorized_start.j2",
                                               {"user": user.parcipiants_id[CURRENT_USER].name}),
                         reply_markup=MENU_KEYBOARD())

