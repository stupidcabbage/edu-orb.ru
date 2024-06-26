from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message

from diary.api.diary import get_lessons
from diary.config import db_session
from diary.db.models import User
from diary.db.services.users import get_user
from diary.services.time import DateNotCorrect, get_weekday_russian, parse_date
from diary.telegram.handlers.message import (send_diary, send_diary_message,
                                             send_message, send_no_lessons)
from diary.telegram.keyboards.diary import (BACK_START_KEYBOARD,
                                            DiaryCallbackFactory)
from diary.telegram.middlewares import (AuthorizeMiddleware,
                                        IsAuthorizedAndHasCurrentUser)
from diary.templates import render_template

router = Router()
router.message.middleware(AuthorizeMiddleware())
router.message.middleware(IsAuthorizedAndHasCurrentUser())



@router.message(Command("diary"))
async def command_diary(message: Message,
                        command: CommandObject) -> None:
    if command.args:
        try:
            date = parse_date(command.args)
            await send_diary_message(message, date, DiaryCallbackFactory, False)

        except DateNotCorrect:
            await send_message(await render_template("incorrect_date.j2"), message, False, BACK_START_KEYBOARD())
            return
    await send_diary_message(message, parse_date("Понедельник"), DiaryCallbackFactory, False)


@router.callback_query(F.data == "diary")
async def callback_diary(callback: CallbackQuery):

    if get_weekday_russian(datetime.today()) in ("Суббота, Воскресенье"):
        await send_diary_message(callback.message, parse_date("Понедельник"),
                                 DiaryCallbackFactory, True)
        await callback.answer()
        return
    await send_diary_message(callback.message,
                             datetime.today(),
                             DiaryCallbackFactory,
                             True)
    await callback.answer()


@router.callback_query(DiaryCallbackFactory.filter())
async def pagination_lesson(callback: CallbackQuery,
                            callback_data: DiaryCallbackFactory):
    user: User = get_user(db_session, callback.message.chat.id)
    date = parse_date(callback_data.date)
    diary = await get_lessons(user, date)
    if not diary:
        await send_no_lessons(callback.message, date, DiaryCallbackFactory, True)
        await callback.answer()
        return

    await send_diary(callback.message, diary, date, DiaryCallbackFactory, True)
    await callback.answer()
