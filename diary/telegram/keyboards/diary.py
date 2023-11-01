from datetime import datetime, timedelta
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from diary.services.time import format_date


class DiaryCallbackFactory(CallbackData, prefix="paginate_diary"):
    date: str


def BACK_START_KEYBOARD():
    buttons = [[types.InlineKeyboardButton(text="Назад", callback_data="start")],]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def MAKE_DIARY_KEYBOARD(date: datetime):
    builder = InlineKeyboardBuilder()
    before_day = format_date(date - timedelta(days=1))
    after_day = format_date(date + timedelta(days=1))

    builder.button(text=f"{before_day}",
                   callback_data=DiaryCallbackFactory(date=before_day))
    builder.button(text="X",
                   callback_data="start")
    builder.button(text=f"{after_day}",
                   callback_data=DiaryCallbackFactory(date=after_day))

    builder.button(text="Назад", callback_data="start")
    builder.adjust(3)
    return builder.as_markup()
