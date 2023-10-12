from aiogram import types


def SIGNUP_CORRECT_KEYBOARD():
    "InlineKeyboard для подтверждения корректности данных авторизации."
    buttons = [
            [types.InlineKeyboardButton(text="Да, они верны! ✅", 
                                        callback_data="yes_correct_data")],
            [types.InlineKeyboardButton(text="Нужно исправить логин!",
                                        callback_data="signup"),
            types.InlineKeyboardButton(text="Нужно исправить пароль!",
                                       callback_data="password_incorrect")]
            ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
