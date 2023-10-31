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


def INCORRECT_LOGOUT():
    buttons = [[types.InlineKeyboardButton(text="Назад", callback_data="start")],]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def USER_MENU_KEYBOARD():
    buttons = [
            [types.InlineKeyboardButton(text="Назад", 
                                        callback_data="start")],
            [types.InlineKeyboardButton(text="Сменить ребенка",
                                        callback_data="change_user"),
            types.InlineKeyboardButton(text="Выйти из аккаунта",
                                       callback_data="logout")]
            ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
