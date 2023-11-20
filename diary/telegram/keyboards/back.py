from aiogram import types


def BACK_TO_START_KEYBOARD():
    buttons = [[types.InlineKeyboardButton(text="Назад", callback_data="start")],]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

