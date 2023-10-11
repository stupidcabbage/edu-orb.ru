from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from templates import render_template
from api.diary import get_diary as gd

router = Router()

@router.message(Command("diary"))
async def get_diary(message: Message) -> None:
    diary = gd()
    new_diary = {"data": diary}
    await message.answer(await render_template("diary.j2", new_diary))
