from aiogram import F, Router, types
from aiogram.filters import Command

from diary.config import CURRENT_USER, db_session
from diary.db.services.parcipiants import change_user_current_status
from diary.db.services.users import get_user
from diary.telegram.keyboards import MAKE_PARCIPIANT_KEYBOARD
from diary.telegram.keyboards.menu import MENU_KEYBOARD
from diary.telegram.middlewares import (AuthorizeMiddleware,
                                        IsAuthorizedMiddleware)
from diary.templates import render_template

router = Router()
router.message.middleware(IsAuthorizedMiddleware())
router.message.middleware(AuthorizeMiddleware())


@router.callback_query(F.data == "change_user")
async def callback_change_user(callback: types.CallbackQuery):
    await _change_user(callback.message)
    await callback.answer()


@router.message(Command("change_user"))
async def command_change_user(message: types.Message):
    await _change_user(message)


async def _change_user(message: types.Message):
    user = get_user(db_session, message.chat.id)
    await message.answer(await render_template("change_user.j2"),
                         reply_markup=MAKE_PARCIPIANT_KEYBOARD(user))


@router.callback_query(F.data.startswith("parcipiant_"))
async def user_changed(callback: types.CallbackQuery):
    user = get_user(db_session, callback.message.chat.id)
    parcipiant_number = callback.data.split("_")[1]

    change_user_current_status(user, parcipiant_number)

    await callback.message.edit_text(await render_template("success_changed_user.j2",
                                                           {"user": user.parcipiants_id[CURRENT_USER].name}),
                                     reply_markup=MENU_KEYBOARD())
    await callback.answer()

