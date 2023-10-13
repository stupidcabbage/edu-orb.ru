from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import ContentType, Message

from handlers.keyboards import SIGNUP_CORRECT_KEYBOARD 
from templates import render_template

import re


EMAIL_REGEX = r"^\S+@\S+\.\S+$"
PHONE_NUMBER_REGEX = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
SNILS_REGEX = r"^\d{1,3}(\s*\d{3})*$"


router = Router()


class SignUp(StatesGroup):
    login = State()
    password = State()
    correct_data = State()
    oauth2 = State()


@router.callback_query(F.data == "signup")
async def signup(callback: types.CallbackQuery,
                 state: FSMContext):
    if not (await state.get_data()).get("password"):
        await callback.message.answer(await render_template("signup.j2"))

    await callback.message.answer(await render_template("login.j2"))
    await state.set_state(SignUp.login)
    await callback.answer()


@router.message(SignUp.login)
async def get_login(message: Message,
                    state: FSMContext):
    if not is_correct_login(message):
        await message.answer(await render_template(
            "incorrect_data.j2", {"field": "логин"}))
        return

    await state.update_data(login=message.text)
    user_data = await state.get_data()

    if not user_data.get("password"):
        await set_password_state_with_message(message, state)
        return

    await check_correctness_of_data(message, user_data, state)



@router.message(SignUp.password)
async def get_password(message: Message,
                       state: FSMContext):
    if not message_is_text(message):
        await message.answer(await render_template(
            "incorrect_data.j2", {"field": "пароль"}))
        return

    user_data = await state.update_data(password=message.text)
    await check_correctness_of_data(message, user_data, state)


@router.callback_query(F.data == "yes_correct_data")
async def correct_data(callback: types.CallbackQuery,
                       state: FSMContext):
    user_data = await state.get_data()
    await callback.message.answer(f"{user_data['login']}, {user_data.get('password')}")
    await callback.message.delete()
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "password_incorrect")
async def password_incorrect(callback: types.CallbackQuery,
                             state: FSMContext):
    await callback.message.delete()
    await set_password_state_with_message(callback.message, state)
    await callback.answer()


def is_correct_login(message: Message) -> bool:
    if not message_is_text(message):
        return False

    login: str = message.text
    return (bool(re.match(EMAIL_REGEX, login))
            or bool(re.match(PHONE_NUMBER_REGEX, login))
            or bool(re.match(SNILS_REGEX, login)))


async def check_correctness_of_data(message: Message,
                                    user_data: dict,
                                    state: FSMContext) -> None:
    user_data = await state.get_data()
    await message.answer(
           text=await render_template("correct_data_question.j2", user_data),
            reply_markup=SIGNUP_CORRECT_KEYBOARD())
    await state.set_state()


def message_is_text(message: Message) -> bool:
    return message.content_type is ContentType.TEXT


async def set_password_state_with_message(message: Message,
                                          state: FSMContext):
    await message.answer(await render_template("password.j2"))
    await state.set_state(SignUp.password)
