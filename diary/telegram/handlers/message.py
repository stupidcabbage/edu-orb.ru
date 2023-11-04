from datetime import datetime
from typing import Optional, Union

from aiogram.filters import CommandObject
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from diary.api.classes import Lesson
from diary.api.diary import get_lessons
from diary.config import db_session
from diary.db.models.users import User
from diary.db.services.users import get_user
from diary.services.time import DateNotCorrect, format_date, get_weekday, parse_date
from diary.telegram.keyboards.diary import (BACK_START_KEYBOARD,
                                            MAKE_DAYS_KEYBOARD,
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


async def command_lesson_message(message: Message,
                                 command: Optional[CommandObject] = None):
    if command.args:
        try:
            raw_date = parse_date(command.args)
            date = format_date(raw_date)
            await send_diary_message(message, date, DiaryCallbackFactory, True)

        except DateNotCorrect:
            await send_message(await render_template("incorrect_date.j2"), message, is_callback, BACK_START_KEYBOARD())
            return


async def callback_message(callback: CallbackQuery):
    if get_weekday(datetime.today()) in ("Суббота, Воскресенье"):
        await send_diary_message(callback.message, parse_date("Понедельник"),
                                 DiaryCallbackFactory, True)
        return
    await send_diary_message(callback.message,
                             datetime.today(),
                             DiaryCallbackFactory,
                             True)


async def make_lesson_message(message: Message,
                              factory: Union[ScheduleCallbackFactory, DiaryCallbackFactory],
                              command: CommandObject | None = None,
                              is_callback: bool = False) -> None:
    user: User = get_user(db_session, message.chat.id)
    if not command or not command.args:
        diary = await get_lessons(user)
        date = datetime.today()
        if not diary:
            diary = await get_lessons(user, format_date(parse_date("понедельник")))

            if not diary:
                await send_no_lessons(message, date, factory, is_callback)
                return
        
        await send_diary(message,
                          diary=diary,
                          date=date,
                          factory=factory,
                          is_callback=is_callback)
        return 

    try:
        raw_date = parse_date(command.args)
        date = format_date(raw_date)
    except DateNotCorrect:
        await send_message(await render_template("incorrect_date.j2"), message, is_callback, BACK_START_KEYBOARD())
        return

    diary = await get_lessons(user, date)
    if not diary:
        await send_no_lessons(message, raw_date, factory, is_callback)
        return
    await send_diary(message,
                      diary=diary,
                      date=raw_date,
                      factory=factory,
                      is_callback=is_callback)


async def send_diary_message(message: Message, date: datetime, factory, is_callback: bool = False):
    user: User = get_user(db_session, message.chat.id)
    diary = await get_lessons(user, format_date(date))
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
