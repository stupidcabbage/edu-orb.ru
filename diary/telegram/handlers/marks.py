from aiogram import F, Router, types
from aiogram.filters import Command

from diary.api.marks import get_marks as gm
from diary.api.schoolperiods import get_school_periods
from diary.config import db_session
from diary.db.services.users import get_user
from diary.telegram.handlers.message import send_message
from diary.telegram.keyboards.marks import (MAKE_SCHOOL_PERIOD_KEYBOARD,
                                            MARKS_KEYBOARD,
                                            SchoolPeriodCallbackFactory)
from diary.telegram.middlewares import (AuthorizeMiddleware,
                                        IsAuthorizedMiddleware)
from diary.templates import render_template

router = Router()
router.message.middleware(AuthorizeMiddleware())
router.message.middleware(IsAuthorizedMiddleware())
router.callback_query.middleware(IsAuthorizedMiddleware())


@router.callback_query(F.data == "marks")
async def callback_marks(callback: types.CallbackQuery):
    await _choose_period_marks(callback.message,
                               is_callback=True)
    await callback.answer()


@router.message(Command("marks"))
async def command_marks(message: types.Message):
    await _choose_period_marks(message)


async def _choose_period_marks(message: types.Message,
                     is_callback: bool = False) -> None:
    user = get_user(db_session, message.chat.id)
    school_periods = await get_school_periods(user)
    await send_message(await render_template("chose_period.j2"),
                       message, is_callback,
                       MAKE_SCHOOL_PERIOD_KEYBOARD(school_periods))


@router.callback_query(SchoolPeriodCallbackFactory.filter())
async def get_marks(callback: types.CallbackQuery,
                    callback_data: SchoolPeriodCallbackFactory):
    user = get_user(db_session, callback.message.chat.id)
    
    marks = await gm(parse_date(callback_data.date_begin), parse_date(callback_data.date_end), user)
    await callback.message.edit_text(await render_template("marks.j2",
                                                           {"marks": marks}),
                                     reply_markup=MARKS_KEYBOARD())
    await callback.answer()
