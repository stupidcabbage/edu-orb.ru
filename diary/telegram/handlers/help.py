from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from diary.telegram.handlers.message import send_message
from diary.telegram.keyboards.diary import BACK_START_KEYBOARD
from diary.templates import render_template

router = Router()


@router.message(Command("help"))
async def command_help(message: Message) -> None:
    await get_help(message)


@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    await get_help(callback.message, is_callback=True)
    await callback.answer()


async def get_help(message: Message,
                   is_callback: bool = False) -> None:
    await send_message(await render_template("help.j2"),
                       message, is_callback,
                       BACK_START_KEYBOARD())
