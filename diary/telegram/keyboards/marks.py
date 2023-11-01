from aiogram import types
from diary.api.classes import SchoolPeriod
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class SchoolPeriodCallbackFactory(CallbackData, prefix="period"):
    date_begin: str
    date_end: str


def MARKS_KEYBOARD():
    buttons = [[types.InlineKeyboardButton(text="Назад", callback_data="start")],]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def MAKE_SCHOOL_PERIOD_KEYBOARD(school_periods: list[SchoolPeriod]):
    builder = InlineKeyboardBuilder()
    for period in school_periods:
        builder.button(text=f"{period.name}",
                       callback_data=SchoolPeriodCallbackFactory(date_begin=period.dateBegin,
                                                                 date_end=period.dateEnd))
    builder.button(text="Назад", callback_data="start")
    builder.adjust(2)
    return builder.as_markup()
