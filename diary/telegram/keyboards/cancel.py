from aiogram import types


def CANCEL_KEYBOARD():
    "Aiogram ReplyKeyboard для отмены действия."
    buttons = [[types.KeyboardButton(text="/cancel")]] 
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons,
                                         resize_keyboard=True,
                                         input_field_placeholder="Хотите отменить действие?",
                                         one_time_keyboard=True)
    return keyboard
