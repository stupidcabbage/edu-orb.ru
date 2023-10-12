from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from api.diary import get_lessons
from templates import render_template

from dateparser import parse
from services.user import test_user
router = Router()


@router.message(Command("diary"))
async def get_tomorrow_lessons(message: Message,
                               command: CommandObject) -> None:
    if not command.args:
        diary = await get_lessons(test_user)
        await message.answer(await render_template("diary.j2", {"diary": diary}))
    else:
        date = parse(command.args,
                     settings={"TIMEZONE": "Asia/Yekaterinburg",
                               "PREFER_DATES_FROM": "future"})
        if not date:
            await message.answer("Время указано неправильно!")
        else:
            diary = await get_lessons(test_user, date.strftime("%d.%m.%Y"))
            await message.answer(await render_template("diary.j2", {"diary": diary}))
