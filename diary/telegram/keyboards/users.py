from aiogram import types

from diary.db.models import User


def MAKE_PARCIPIANT_KEYBOARD(user: User):
    parcipiants = user.parcipiants_id

    buttons = []
    for i, parcipiant in enumerate(parcipiants):
        buttons.append([types.InlineKeyboardButton(text=f"{parcipiant.name}",
                                                  callback_data=f"parcipiant_{i}")])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
