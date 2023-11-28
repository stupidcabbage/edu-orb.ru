from aiogram import F, Router, types

from diary.old_api.notification import MarkNotification
from diary.config import db_session
from diary.db.models.users import User
from diary.db.services.marks import get_five_last_marks
from diary.db.services.users import get_user, set_notification_status
from diary.telegram.keyboards import (BACK_TO_START_KEYBOARD,
                                      NOTIFICATION_MENU_KEYBOARD)
from diary.telegram.middlewares import (AuthorizeMiddleware,
                                        IsAuthorizedMiddleware)
from diary.templates import render_template

router = Router()
router.message.middleware(AuthorizeMiddleware())
router.message.middleware(IsAuthorizedMiddleware())
router.callback_query.middleware(IsAuthorizedMiddleware())


@router.callback_query(F.data == "help_notification")
async def help_noitification(callback: types.CallbackQuery):
    await callback.message.edit_text(await render_template("help_notification.j2"),
                                     reply_markup=BACK_TO_START_KEYBOARD())
    await callback.answer()


@router.callback_query(F.data == "notification_menu")
async def notification_menu(callback: types.CallbackQuery):
    user: User = get_user(db_session, callback.from_user.id)
    await callback.message.edit_text(await render_template("notification_menu.j2"),
                                     reply_markup=NOTIFICATION_MENU_KEYBOARD(user.notification_status))
    await callback.answer()


@router.callback_query(F.data == "turnoff_notification")
async def turnoff_notification(callback: types.CallbackQuery):
    user: User = get_user(db_session, callback.from_user.id)
    set_notification_status(db_session, user, False)
    await callback.message.edit_text(await render_template("turnoff_notification.j2"),
                                     reply_markup=NOTIFICATION_MENU_KEYBOARD(user.notification_status))
    await callback.answer()


@router.callback_query(F.data == "history_notification")
async def history_notification(callback: types.CallbackQuery):
    user: User = get_user(db_session, callback.from_user.id)
    parcipiant = user.current_parcipiant()
    marks = get_five_last_marks(db_session, parcipiant)
    await callback.message.edit_text(await render_template("history_notification.j2",
                                                           {"marks": marks}),
                                    reply_markup=BACK_TO_START_KEYBOARD())
    await callback.answer()


@router.callback_query(F.data == "turnon_notification")
async def turnon_notification(callback: types.CallbackQuery):
    user: User = get_user(db_session, callback.from_user.id)
    await callback.answer("Добавляем оценки за последние три недели.")

    try:
        await MarkNotification().add_user(user)
    except Exception:
        await callback.message.edit_text(await render_template("incorrect_turnon_notification.j2"),
                                         reply_markup=BACK_TO_START_KEYBOARD())
        await callback.answer()
        return

    set_notification_status(db_session, user, True)
    await callback.message.edit_text(await render_template("turnon_notification.j2"),
                                     reply_markup=NOTIFICATION_MENU_KEYBOARD(user.notification_status))
    await callback.answer()


