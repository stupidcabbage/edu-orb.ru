from aiogram import types
from telebot import types as ttypes


def SIGNUP_KEYBOARD_TELEBOT():
    "Telebot InlineKeyboard для повторной регистрации."
    buttons = [[ttypes.InlineKeyboardButton(
        text="🚪Попробовать снова",
        callback_data="signup")]]
    keyboard = ttypes.InlineKeyboardMarkup(keyboard=buttons)
    return keyboard


def SIGNUP_KEYBOARD_AIOGRAM():
    "Aiogram InlineKeyboard для регистрации."
    buttons = [[types.InlineKeyboardButton(
            text="🚪Зарегистрироваться",
            callback_data="signup")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def SIGNUP_CORRECT_KEYBOARD():
    "Aiogram InlineKeyboard для подтверждения корректности данных авторизации."
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
