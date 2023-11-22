from diary.config import AiogramBot
from diary.db.models import Mark, User
from diary.telegram.keyboards import BACK_TO_START_KEYBOARD
from diary.templates import render_template


async def send_notification_message(user: User, marks: list[Mark]):
    await AiogramBot().send_message(
            user.telegram_id,
            await render_template("notification.j2", data={"marks": marks}),
            reply_markup=BACK_TO_START_KEYBOARD())
