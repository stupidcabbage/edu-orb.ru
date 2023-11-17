from diary.config import bot

async def send_message(message: str, chat_id: int):
    await bot.send_message(chat_id, message)
