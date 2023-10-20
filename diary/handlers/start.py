from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(CommandStart())
async def command_start(message: Message,
                        state: FSMContext):
    if await state.get_data():
        await message.answer("Ты проходишь авторизацию!")
        return

    if message.from_user.id != 11226590290:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="🚪Зарегистрироваться",
            callback_data="signup"))
        await message.answer("Привет, похоже ты здесь впервые!",
                             reply_markup=builder.as_markup())
        return
    await message.answer(f"Привет, хозяин!")
