from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.message import Message

from diary.handlers.authorize import SignUp
from diary.templates import render_template

router = Router()


@router.message(Command("cancel"))
async def cancel(message: Message,
                 state: FSMContext):
    if not await state.get_state():
        await message.reply(await render_template("nothing_to_cancel.j2"),
                            reply_markup=ReplyKeyboardRemove())
        return

    if await state.get_state() in (SignUp.anomaly, SignUp.oauth2):
        await message.reply(await render_template("denied_cancel.j2"),
                            reply_markup=ReplyKeyboardRemove())
        return

    await message.reply(await render_template("success_cancel.j2"),
                        reply_markup=ReplyKeyboardRemove())
    await state.clear()

