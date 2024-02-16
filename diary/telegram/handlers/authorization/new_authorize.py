from contextlib import suppress
from aiogram import F, Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from diary.config import AiogramBotSender
from diary.telegram.filters.check_fields import LoginFilter, OnlyTextMessageFilter
from diary.telegram.keyboards.cancel import INLINE_CANCEL_KEYBOARD
from diary.telegram.keyboards.signup import SIGNUP_CORRECT_KEYBOARD
from diary.telegram.states.signup import SignUp

from diary.templates import render_template

router = Router()


@router.callback_query(F.data == "signup")
async def signup(callback: types.CallbackQuery,
                 state: FSMContext):
    "Авторизация."
    last_bot_message = await callback.message.answer(
            await render_template("login.j2"),
            reply_markup=INLINE_CANCEL_KEYBOARD())

    await update_last_message_state(last_bot_message, state)
    await state.set_state(SignUp.login)
    await callback.answer()

@router.message(SignUp.login, LoginFilter())
async def get_login(message: types.Message,
                    state: FSMContext) -> None:
    await delete_previous_messages(message, state)
    await state.update_data(login=message.text)

    if not await is_password_already_written(state):
        await send_password_form(message, state)
        return

    await _check_correctness_of_data(state, message)

async def is_password_already_written(state: FSMContext) -> bool:
    return bool((await state.get_data()).get("password"))

async def send_password_form(message: types.Message,
                             state: FSMContext) -> None:
    last_bot_message = await message.answer(await render_template("password.j2"),
                                       reply_markup=INLINE_CANCEL_KEYBOARD())
    await update_last_message_state(last_bot_message, state)
    await state.set_state(SignUp.password)
    
@router.message(SignUp.password, OnlyTextMessageFilter())
async def get_password(message: types.Message,
                       state: FSMContext):
    await delete_previous_messages(message, state)
    await state.update_data(password=message.text)
    await _check_correctness_of_data(state, message)

async def delete_previous_messages(message: types.Message,
                                   state: FSMContext) -> None:
    with suppress(TelegramBadRequest):
        last_bot_message = (await state.get_data()).get("last_bot_message")
        await AiogramBotSender().delete_message(chat_id=message.from_user.id,
                                                message_id=last_bot_message)
        await message.delete()

async def _check_correctness_of_data(
        state: FSMContext, message: types.Message) -> None:
    "Сообщение с просьбой для проверки правильности введеных данных."
    user_data = await state.get_data()
    last_bot_message = await message.answer(
            await render_template("correct_data_question.j2", user_data),
            reply_markup=SIGNUP_CORRECT_KEYBOARD())

    await update_last_message_state(last_bot_message, state)
    await state.set_state()

@router.callback_query(F.data == "login_incorrect")
async def login_incorrect(callback: types.CallbackQuery,
                          state: FSMContext):
    await callback.message.edit_text(await render_template("login.j2"),
                                     reply_markup=INLINE_CANCEL_KEYBOARD())
    await callback.answer()
    await state.set_state(SignUp.login)

@router.callback_query(F.data == "password_incorrect")
async def password_incorrect(callback: types.CallbackQuery,
                             state: FSMContext):
    "Перезапись пароля на гос услугах при авторизации."
    await callback.message.edit_text(
            await render_template("password.j2"),
            reply_markup=INLINE_CANCEL_KEYBOARD())
    await state.set_state(SignUp.password)
    await callback.answer()

async def update_last_message_state(message: types.Message,
                           state: FSMContext) -> None:
    await state.update_data({"last_bot_message": message.message_id})
