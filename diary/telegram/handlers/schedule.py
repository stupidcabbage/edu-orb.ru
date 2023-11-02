from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from diary.api.diary import get_lessons
from diary.config import db_session
from diary.db.models import User
from diary.db.services.users import get_user
from diary.services.time import parse_pagination_date
from diary.telegram.handlers.message import (make_lesson_message, send_diary,
                                             send_no_lessons)
from diary.telegram.keyboards.diary import ScheduleCallbackFactory
from diary.telegram.middlewares import (AuthorizeMiddleware,
                                        IsAuthorizedAndHasCurrentUser)

router = Router()
router.message.middleware(AuthorizeMiddleware())
router.message.middleware(IsAuthorizedAndHasCurrentUser())


@router.message(Command("schedule"))
async def command_schedule(message: Message,
                           command: Command) -> None:
    await get_schedule(message, command)


@router.callback_query(F.data == "schedule")
async def callback_schedule(callback: CallbackQuery):
    await get_schedule(callback.message, is_callback=True)
    await callback.answer()


async def get_schedule(message: Message,
                       command: Command | None = None,
                       is_callback: bool = False):
    await make_lesson_message(message, ScheduleCallbackFactory, command, is_callback)


@router.callback_query(ScheduleCallbackFactory.filter())
async def pagination_lesson(callback: CallbackQuery,
                            callback_data: ScheduleCallbackFactory):
    user: User = get_user(db_session, callback.message.chat.id)
    diary = await get_lessons(user, callback_data.date)
    date = parse_pagination_date(callback_data.date)
    if not diary:
        await send_no_lessons(callback.message, date, ScheduleCallbackFactory, True)
        return
    await send_diary(callback.message, diary, date, ScheduleCallbackFactory, True)
