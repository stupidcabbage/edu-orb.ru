from telebot import logging

from diary.api.exceptions import ParcipiantNotFound
from diary.db.models.users import User
from diary.telegram.handlers.notifications.send_notification import \
    send_token_expired_notification


def exception_token_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ParcipiantNotFound:
            await update_active_status_and_notify(kwargs['user'])
    return wrapper

async def update_active_status_and_notify(user: User):
    logging.warning(
            f"Token has expired for user: {user}. Changed activate status.")
    # update_active_status(user)
    await send_token_expired_notification(user)
