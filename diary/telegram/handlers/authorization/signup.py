from aiogram import types, F
from aiogram.fsm.context import FSMContext

from diary.telegram.handlers.authorization import router
from .state_serivice import update_last_message_state
from diary.telegram.keyboards.cancel import INLINE_CANCEL_KEYBOARD
from diary.telegram.states.signup import SignUp
from diary.templates import render_template


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
