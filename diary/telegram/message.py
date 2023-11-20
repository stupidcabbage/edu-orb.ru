import logging

from diary.config import bot, second_bot


async def aiogram_send_message(message: str, chat_id: int, reply_markup=None):
    logging.info(f"Sent message to {chat_id}")
    await bot.send_message(chat_id, message, reply_markup=reply_markup)
    await bot.session.close()

def telebot_send_message(message, chat_id: int):
    logging.info(f"Sent message to {chat_id}")
    second_bot.send_message(chat_id, message)
