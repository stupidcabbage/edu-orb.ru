from diary.config import AiogramBot
from diary.db.models import Mark, User
from diary.telegram.keyboards import (BACK_TO_START_KEYBOARD,
                                      SIGNUP_KEYBOARD_AIOGRAM)
from diary.templates import render_template


async def send_notification_message(user: User, marks: list[Mark]):
    await AiogramBot().send_message(
            user.telegram_id,
            await render_template("notification.j2", data={"marks": marks}),
            reply_markup=BACK_TO_START_KEYBOARD())
    await AiogramBot().session.close()

async def send_token_expired_notification(user: User):
    await AiogramBot().send_message(
            user.telegram_id,
            await render_template("token_expired_notification.j2"),
            reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
    await AiogramBot().session.close()
