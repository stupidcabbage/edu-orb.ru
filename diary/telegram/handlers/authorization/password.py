from aiogram import F, types
from aiogram.fsm.context import FSMContext
from diary.telegram.filters.check_fields import OnlyTextMessageFilter
from diary.telegram.handlers.authorization import router
from diary.telegram.handlers.authorization.new_authorize import delete_previous_messages
from diary.telegram.handlers.authorization.state_serivice import send_check_correctness_data_message
from diary.telegram.keyboards.cancel import INLINE_CANCEL_KEYBOARD
from diary.telegram.states.signup import SignUp
from diary.templates import render_template


@router.callback_query(F.data == "password_incorrect")
async def password_incorrect(callback: types.CallbackQuery,
                             state: FSMContext):
    "Перезапись пароля на гос услугах при авторизации."
    await callback.message.edit_text(
            await render_template("password.j2"),
            reply_markup=INLINE_CANCEL_KEYBOARD())
    await state.set_state(SignUp.password)
    await callback.answer()


@router.message(SignUp.password, OnlyTextMessageFilter())
async def get_password(message: types.Message,
                       state: FSMContext):
    await delete_previous_messages(message, state)
    await state.update_data(password=message.text)
    await send_check_correctness_data_message(state, message)
