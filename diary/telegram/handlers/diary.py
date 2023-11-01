from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message
from diary.api.classes import Lesson

from diary.api.diary import get_lessons
from diary.config import db_session
from diary.db.models.users import User
from diary.db.services.users import get_user
from diary.services.time import DateNotCorrect, format_date, parse_date, parse_pagination_date
from diary.telegram.handlers.message import send_message
from diary.telegram.keyboards.diary import BACK_START_KEYBOARD, MAKE_DIARY_KEYBOARD, DiaryCallbackFactory
from diary.telegram.middlewares.authorize import (
    AuthorizeMiddleware, IsAuthorizedAndHasCurrentUser)
from diary.templates import render_template

router = Router()
router.message.middleware(AuthorizeMiddleware())
router.message.middleware(IsAuthorizedAndHasCurrentUser())



@router.message(Command("diary"))
async def command_diary(message: Message,
                        command: CommandObject) -> None:
    await lessons(message, command)


@router.callback_query(F.data == "diary")
async def callback_diary(callback: CallbackQuery):
    await lessons(callback.message, is_callback=True)
    await callback.answer()


@router.callback_query(DiaryCallbackFactory.filter())
async def pagination_lesson(callback: CallbackQuery,
                            callback_data: DiaryCallbackFactory):
    user: User = get_user(db_session, callback.message.chat.id)
    diary = await get_lessons(user, callback_data.date)
    date = parse_pagination_date(callback_data.date)
    if not diary:
        await _send_no_lessons(callback.message, date, True)
        return

    await _send_diary(callback.message, diary, date, True)



async def lessons(message: Message,
                  command: CommandObject | None = None,
                  is_callback: bool = False) -> None:
    user: User = get_user(db_session, message.chat.id)
    print(command)
    if not command or not command.args:
        diary = await get_lessons(user)
        date = datetime.today()
        if not diary:
            diary = await get_lessons(user, format_date(parse_date("понедельник")))

            if not diary:
                await _send_no_lessons(message, date, is_callback)
                return

        await _send_diary(message, diary, date, is_callback)
        return 

    try:
        raw_date = parse_date(command.args)
        date = format_date(raw_date)
    except DateNotCorrect:
        await send_message(await render_template("incorrect_date.j2"), message, is_callback, BACK_START_KEYBOARD())
        return

    diary = await get_lessons(user, date)
    if not diary:
        await _send_no_lessons(message, raw_date, is_callback)
        return
    
    await _send_diary(message, diary, raw_date, is_callback)


async def _send_no_lessons(message: Message,
                           date: datetime,
                           is_callback: bool = False):
    keyboard = MAKE_DIARY_KEYBOARD(date)
    await send_message(await render_template("nolessons.j2", {"date": format_date(date)}),
                       message,
                       is_callback,
                       reply_markup=keyboard)

async def _send_diary(message: Message, diary: list[Lesson],
                      date: datetime,
                      is_callback: bool = False) -> None:
    await send_message(await render_template("diary.j2", {"diary": diary}),
                       message, is_callback, MAKE_DIARY_KEYBOARD(date))
