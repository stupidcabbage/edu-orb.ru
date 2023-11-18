from diary.db.models.users import Mark, User
from diary.telegram.message import telebot_send_message
from diary.templates import render_template


async def send_notification_message(user: User, marks: list[Mark]):
    telebot_send_message(
            await render_template("notification.j2", data={"marks": marks}),
            user.telegram_id)
