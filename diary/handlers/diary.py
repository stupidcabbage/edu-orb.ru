from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dateparser import parse

from api.diary import get_lessons
from services.user import test_user
from templates import render_template

router = Router()


def parse_date(date: str) -> str | None:
    parsed_date = parse(date,
                        settings={"TIMEZONE": "Asia/Yekaterinburg",
                                  "PREFER_DATES_FROM": "future"})
    if not parsed_date:
        return None
    return parsed_date.strftime("%d.%m.%Y")


@router.message(Command("diary"))
async def get_tomorrow_lessons(message: Message,
                               command: CommandObject) -> None:
    if not command.args:
        diary = await get_lessons(test_user)
        if not diary:
            diary = await get_lessons(test_user, parse_date("понедельник"))
        await message.answer(await render_template("diary.j2", {"diary": diary}))
    else:
        date = parse_date(command.args)
        if not date:
            await message.answer("Время указано неправильно!")
        else:
            diary = await get_lessons(test_user, date)
            if not diary:
                await message.answer(await render_template("nolessons.j2", {"date": date}))
                await message.answer_sticker("https://i.imgur.com/gYYgAih.mp4")
            else:
                await message.answer(await render_template("diary.j2", {"diary": diary}))
