from aiogram import types
from telebot import types as ttypes


def CANCEL_KEYBOARD():
    "ReplyKeyboard для отмены действия."
    buttons = [[types.KeyboardButton(text="/cancel")]] 
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons,
                                         resize_keyboard=True,
                                         input_field_placeholder="Хотите отменить действие?",
                                         one_time_keyboard=True)
    return keyboard


def SIGNUP_KEYBOARD_TELEBOT():
    "InlineKeyboard для повторной регистрации."
    buttons = [[ttypes.InlineKeyboardButton(
        text="🚪Попробовать снова",
        callback_data="signup")]]
    keyboard = ttypes.InlineKeyboardMarkup(keyboard=buttons)
    return keyboard


def SIGNUP_KEYBOARD_AIOGRAM():
    "InlineKeyboard для регистрации."
    buttons = [[types.InlineKeyboardButton(
            text="🚪Зарегистрироваться",
            callback_data="signup")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def SIGNUP_CORRECT_KEYBOARD():
    "InlineKeyboard для подтверждения корректности данных авторизации."
    buttons = [
            [types.InlineKeyboardButton(text="Да, они верны! ✅", 
                                        callback_data="yes_correct_data")],
            [types.InlineKeyboardButton(text="Исправить логин!",
                                        callback_data="login_incorrect"),
            types.InlineKeyboardButton(text="Исправить пароль!",
                                       callback_data="password_incorrect")]
            ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
