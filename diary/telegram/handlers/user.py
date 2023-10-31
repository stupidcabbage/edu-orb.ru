from aiogram import F, Router, types
from aiogram.filters import Command

from diary.config import CURRENT_USER, db_session
from diary.db.services.parcipiants import change_user_current_status
from diary.db.services.users import delete_user, get_user
from diary.telegram.handlers.message import send_message
from diary.telegram.keyboards import (MAKE_PARCIPIANT_KEYBOARD, MENU_KEYBOARD,
                                      USER_MENU_KEYBOARD)
from diary.telegram.keyboards.signup import SIGNUP_KEYBOARD_AIOGRAM
from diary.telegram.keyboards.users import INCORRECT_LOGOUT
from diary.telegram.middlewares import (AuthorizeMiddleware,
                                        IsAuthorizedMiddleware)
from diary.templates import render_template

router = Router()
router.message.middleware(AuthorizeMiddleware())
router.message.middleware(IsAuthorizedMiddleware())
router.callback_query.middleware(IsAuthorizedMiddleware())


@router.callback_query(F.data == "change_user")
async def callback_change_user(callback: types.CallbackQuery):
    await _change_user(callback.message,
                       is_callback=True)
    await callback.answer()


@router.message(Command("change_user"))
async def command_change_user(message: types.Message):
    await _change_user(message)


@router.callback_query(F.data.startswith("parcipiant_"))
async def user_changed(callback: types.CallbackQuery):
    user = get_user(db_session, callback.from_user.id)
    parcipiant_number = callback.data.split("_")[1]

    change_user_current_status(user, parcipiant_number)

    await callback.message.edit_text(await render_template(
                                     "success_changed_user.j2",
                                     {"user": user.parcipiants_id[CURRENT_USER].name}),
                                     reply_markup=MENU_KEYBOARD())
    await callback.answer()


@router.callback_query(F.data == "logout")
async def logout(callback: types.CallbackQuery):
    user = get_user(db_session, callback.from_user.id)
    try:
        delete_user(db_session, user)
    except Exception:
        await callback.message.edit_text(await render_template("incorrect_logout.j2"),
                                         reply_markup=INCORRECT_LOGOUT())
        await callback.answer()
        return

    await callback.message.edit_text(await render_template("logout.j2"),
                                     reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
    await callback.answer()


@router.callback_query(F.data == "user")
async def user_menu(callback: types.CallbackQuery):
    user = get_user(db_session, callback.message.chat.id)

    await callback.message.edit_text(await render_template(
                                     "user_menu.j2",
                                     {"parcipiant": user.parcipiants_id[CURRENT_USER]}),
                                     reply_markup=USER_MENU_KEYBOARD())
    await callback.answer()


async def _change_user(message: types.Message,
                       is_callback: bool = False):
    user = get_user(db_session, message.chat.id)
    await send_message(await render_template("change_user.j2"),
                       message,
                       is_callback,
                       reply_markup=MAKE_PARCIPIANT_KEYBOARD(user))
