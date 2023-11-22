from aiogram import Router, types
from aiogram.filters import Command

from diary.config import TelebotBot

router = Router()

@router.message(Command("test"))
async def test(message: types.Message):
    bot = TelebotBot()
    print(bot)
    bot.send_message(message.from_user.id, "test")
