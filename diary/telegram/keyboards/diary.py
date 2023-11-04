from datetime import datetime, timedelta
from typing import Union
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from loguru import logger

from diary.services.time import format_date


class DiaryCallbackFactory(CallbackData, prefix="paginate_diary"):
    date: str


class ScheduleCallbackFactory(CallbackData, prefix="paginate_schedule"):
    date: str


def BACK_START_KEYBOARD():
    buttons = [[types.InlineKeyboardButton(text="Назад", callback_data="start")],]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def MAKE_DAYS_KEYBOARD(date: datetime,
                       factory: Union[DiaryCallbackFactory, ScheduleCallbackFactory]):
    logger.critical("started making keyboard")
    builder = InlineKeyboardBuilder()
    before_day = format_date(date - timedelta(days=1))
    logger.critical(before_day)
    after_day = format_date(date + timedelta(days=1))
    logger.critical(after_day)
    builder.button(text=f"{before_day}",
                   callback_data=factory(date=before_day))
    builder.button(text="X",
                   callback_data="start")
    builder.button(text=f"{after_day}",
                   callback_data=factory(date=after_day))
    logger.critical("added buttons")
    builder.button(text="Назад", callback_data="start")
    builder.adjust(3)
    return builder.as_markup()
