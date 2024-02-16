from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from diary.telegram.states import SignUp
from diary.telegram.keyboards.signup import SIGNUP_KEYBOARD_AIOGRAM
from diary.templates import render_template

router = Router()


@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery,
                 state: FSMContext):
    if not await state.get_state():
        await callback.message.answer(await render_template("nothing_to_cancel.j2"),
                                     reply_markup=ReplyKeyboardRemove())
        await callback.answer()
        return

    if await state.get_state() in (SignUp.anomaly, SignUp.oauth2):
        await callback.message.answer(await render_template("denied_cancel.j2"),
                            reply_markup=ReplyKeyboardRemove())
        await callback.answer()
        return

    await callback.message.answer(await render_template("success_cancel.j2"),
                        reply_markup=SIGNUP_KEYBOARD_AIOGRAM())
    await callback.answer()
    await state.clear()

