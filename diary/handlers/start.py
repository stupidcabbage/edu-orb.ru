from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    if message.from_user.id != 11226590290:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="🚪Зарегистрироваться",
            callback_data="signup"))
        await message.answer("Привет, похоже ты здесь впервые!",
                             reply_markup=builder.as_markup())
        await message.answer_photo("blob:https://esia.gosuslugi.ru/fcf30a93-c676-4201-b97a-d7c1d924afca")
    else:
        await message.answer(f"Привет, хозяин!")
