from aiogram import types


def MENU_KEYBOARD():
    "Aiogram InlineKeyboard меню"
    buttons = [
            [types.InlineKeyboardButton(text="📝Домашнее задание", 
                                        callback_data="diary")],
            [types.InlineKeyboardButton(text="📔Отметки",
                                        callback_data="marks"),
            types.InlineKeyboardButton(text="📇Расписание",
                                       callback_data="schedule")],
            [types.InlineKeyboardButton(text="🔖Профиль",
                                        callback_data="user"),
             types.InlineKeyboardButton(text="📰 Возможности",
                                        callback_data="help")]
            ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
