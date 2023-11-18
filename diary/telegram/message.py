import logging
from diary.config import bot

async def send_message(message: str, chat_id: int):
    logging.info(f"Sent message to {chat_id}")
    await bot.send_message(chat_id, message)
    await bot.session.close()
