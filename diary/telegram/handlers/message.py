from datetime import datetime
from typing import Optional, Union

from aiogram.types import InlineKeyboardMarkup, Message

from diary.api.classes import Lesson
from diary.api.diary import get_lessons
from diary.config import db_session
from diary.db.models.users import User
from diary.db.services.users import get_user
from diary.services.time import format_date
from diary.telegram.keyboards.diary import (MAKE_DAYS_KEYBOARD,
                                            DiaryCallbackFactory,
                                            ScheduleCallbackFactory)
from diary.templates import render_template

TEMPLATES_NAME = {
    ScheduleCallbackFactory: "schedule.j2",
    DiaryCallbackFactory: "diary.j2"
}


async def send_message(text: str,
                        message: Optional[Message] = None,
                        is_callback: bool = False,
                        reply_markup: Optional[InlineKeyboardMarkup] = None):
    sending = message.answer
    if is_callback:
        sending = message.edit_text

    await sending(text, reply_markup=reply_markup)


async def send_diary_message(message: Message, date: datetime, factory, is_callback: bool = False):
    user: User = get_user(db_session, message.chat.id)
    diary = await get_lessons(user, date)
    if not diary:
        await send_no_lessons(message, date, factory, is_callback)
        return
    await send_diary(message,
                      diary=diary,
                      date=date,
                      factory=factory,
                      is_callback=is_callback)


async def send_no_lessons(message: Message,
                           date: datetime,
                           factory: Union[ScheduleCallbackFactory, DiaryCallbackFactory],
                           is_callback: bool = False):
    keyboard = MAKE_DAYS_KEYBOARD(date, factory)
    await send_message(await render_template("nolessons.j2", {"date": format_date(date)}),
                       message,
                       is_callback,
                       reply_markup=keyboard)


async def send_diary(message: Message, diary: list[Lesson],
                      date: datetime,
                      factory: Union[ScheduleCallbackFactory, DiaryCallbackFactory],
                      is_callback: bool = False) -> None:
    template_name = TEMPLATES_NAME[factory]
    await send_message(await render_template(template_name, {"diary": diary}),
                       message, is_callback, MAKE_DAYS_KEYBOARD(date, factory))
