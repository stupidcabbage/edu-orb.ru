from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message
from dateparser import parse

from diary.api.diary import get_lessons
from diary.config import db_session
from diary.db.services.users import get_user
from diary.telegram.middlewares.authorize import (
    AuthorizeMiddleware, IsAuthorizedAndHasCurrentUser)
from diary.templates import render_template

router = Router()
router.message.middleware(AuthorizeMiddleware())
router.message.middleware(IsAuthorizedAndHasCurrentUser())


def parse_date(date: str) -> str | None:
    parsed_date = parse(date,
                        settings={"TIMEZONE": "Asia/Yekaterinburg",
                                  "PREFER_DATES_FROM": "future"})
    if not parsed_date:
        return None
    return parsed_date.strftime("%d.%m.%Y")


@router.message(Command("diary"))
async def command_diary(message: Message,
                        command: CommandObject) -> None:
    await lessons(message, command)


@router.callback_query(F.data == "diary")
async def callback_diary(callback: CallbackQuery):
    await lessons(callback.message)
    await callback.answer()


async def lessons(message: Message,
                  command: CommandObject | None = None) -> None:
    user = get_user(db_session, message.chat.id)
    if not command or not command.args:
        diary = await get_lessons(user)
        if not diary:
            diary = await get_lessons(user,
                                      parse_date("понедельник"))

            if not diary:
                await message.answer(await render_template("nolessons.j2", {"weekend": True}))
                await message.answer_sticker("https://i.imgur.com/gYYgAih.mp4")
                return

        await message.answer(await render_template("diary.j2", {"diary": diary}))
        return 
    
    date = parse_date(command.args)
    if not date:
        await message.answer("Время указано неправильно!")
        return

    diary = await get_lessons(user, date)
    if not diary:
        await message.answer(await render_template("nolessons.j2", {"date": date}))
        await message.answer_sticker("https://i.imgur.com/gYYgAih.mp4")
        return

    await message.answer(await render_template("diary.j2", {"diary": diary}))
