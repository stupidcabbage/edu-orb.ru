from aiogram import types
from aiogram.fsm.context import FSMContext
from diary.telegram.filters.check_fields import LoginFilter
from diary.telegram.handlers.authorization import router
from diary.telegram.keyboards.cancel import INLINE_CANCEL_KEYBOARD
from diary.templates import render_template
from .state_serivice import delete_previous_messages, send_check_correctness_data_message, update_last_message_state
from diary.telegram.states.signup import SignUp


@router.callback_query(F.data == "login_incorrect")
async def login_incorrect(callback: types.CallbackQuery,
                          state: FSMContext):
    await callback.message.edit_text(await render_template("login.j2"),
                                     reply_markup=INLINE_CANCEL_KEYBOARD())
    await callback.answer()
    await state.set_state(SignUp.login)


@router.message(SignUp.login, LoginFilter())
async def get_login(message: types.Message,
                    state: FSMContext) -> None:
    await delete_previous_messages(message, state)
    await state.update_data(login=message.text)

    if not await is_password_already_written(state):
        await send_password_form(message, state)
        return

    await send_check_correctness_data_message(state, message)


async def is_password_already_written(state: FSMContext) -> bool:
    return bool((await state.get_data()).get("password"))


async def send_password_form(message: types.Message,
                             state: FSMContext) -> None:
    last_bot_message = await message.answer(await render_template("password.j2"),
                                            reply_markup=INLINE_CANCEL_KEYBOARD())
    await update_last_message_state(last_bot_message, state)
    await state.set_state(SignUp.password)
