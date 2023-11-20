from diary.db.models import User, Mark
from diary.templates import render_template
from diary.telegram.message import aiogram_send_message
from diary.telegram.keyboards import BACK_TO_START_KEYBOARD

async def send_notification_message(user: User, marks: list[Mark]):
    await aiogram_send_message(
            await render_template("notification.j2", data={"marks": marks}),
            user.telegram_id,
            BACK_TO_START_KEYBOARD())
