from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from api.diary import get_diary as gd
from templates import render_template

router = Router()

@router.message(Command("diary"))
async def get_diary(message: Message) -> None:
    diary = gd()
    new_diary = {"data": diary}
    await message.answer(await render_template("diary.j2", new_diary))
