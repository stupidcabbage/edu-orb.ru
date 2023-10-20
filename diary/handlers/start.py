from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from diary.middlewares.authorize import AuthorizeMiddleware

router = Router()
router.message.middleware(AuthorizeMiddleware())


@router.message(CommandStart())
async def command_start(message: Message):
    if message.from_user.id != 11226590290:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="🚪Зарегистрироваться",
            callback_data="signup"))
        await message.answer("Привет, похоже ты здесь впервые!",
                             reply_markup=builder.as_markup())
        return
    await message.answer(f"Привет, хозяин!")
