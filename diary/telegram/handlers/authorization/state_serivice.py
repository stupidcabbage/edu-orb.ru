from contextlib import suppress
from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from diary.config import AiogramBotSender
from diary.telegram.keyboards.signup import SIGNUP_CORRECT_KEYBOARD
from diary.templates import render_template

async def delete_previous_messages(message: types.Message,
                                   state: FSMContext) -> None:
    with suppress(TelegramBadRequest):
        last_bot_message = (await state.get_data()).get("last_bot_message")
        await AiogramBotSender().delete_message(chat_id=message.from_user.id,
                                                message_id=last_bot_message)
        await message.delete()

async def send_check_correctness_data_message(state: FSMContext,
                                              message: types.Message) -> None:
    user_data = await state.get_data()
    last_bot_message = await message.answer(
            await render_template("correct_data_question.j2", user_data),
            reply_markup=SIGNUP_CORRECT_KEYBOARD())

    await update_last_message_state(last_bot_message, state)
    await state.set_state()

async def update_last_message_state(message: types.Message,
                                    state: FSMContext) -> None:
    await state.update_data({"last_bot_message": message.message_id})
