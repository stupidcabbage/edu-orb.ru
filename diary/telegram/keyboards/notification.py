from typing import Optional

from aiogram import types


def NOTIFICATION_MENU_KEYBOARD(notification_status: Optional[bool]):
    "Aiogram InlineKeyboard меню для уведомлений у кого они выключены."
    if notification_status:
        turn = types.InlineKeyboardButton(text="Выключить",
                                   callback_data="turnoff_notification")
    else:
        turn = types.InlineKeyboardButton(text="Включить",
                                          callback_data="turnon_notification")

    buttons = [
            [types.InlineKeyboardButton(text="История", 
                                        callback_data="history_notification")],
            [turn,
            types.InlineKeyboardButton(text="Подробнее",
                                       callback_data="help_notification")],
            [types.InlineKeyboardButton(text="Назад",
                                        callback_data="start")]
            ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

