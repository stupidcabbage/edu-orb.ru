from typing import Optional

from aiogram.types import InlineKeyboardMarkup, Message


async def send_message(text: str,
                        message: Optional[Message] = None,
                        is_callback: bool = False,
                        reply_markup: Optional[InlineKeyboardMarkup] = None):
    sending = message.answer
    if is_callback:
        sending = message.edit_text

    await sending(text, reply_markup=reply_markup)
