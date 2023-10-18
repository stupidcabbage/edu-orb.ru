import asyncio
import re
import time
import threading
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ContentType, InputFile, Message

from diary.config import BASE_DIR, second_bot
from diary.handlers.keyboards import SIGNUP_CORRECT_KEYBOARD
from diary.selenium_parser.BasePages import SearchHelper
from diary.services.user import User
from diary.templates import render_template


EMAIL_REGEX = r"^\S+@\S+\.\S+$"
PHONE_NUMBER_REGEX = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
SNILS_REGEX = r"^\d{1,3}(\s*\d{3})*$"


router = Router()


class SignUp(StatesGroup):
    login = State()
    password = State()
    correct_data = State()
    anomaly = State()
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


async def get_code(state: FSMContext,
                   data: str):
    while True:
        print(await state.get_data())
        value = (await state.get_data()).get(data)
        if value:
            return value
        time.sleep(5)


async def authorize_gosuslugi(user: User,
                              state: FSMContext):
    driver = SearchHelper()
    driver.go_to_diary_page()
    driver.go_to_gosuslugi_login_page()
    driver.authorize(user)
    elements = driver.user_has_oauth2()
    anomaly = driver.check_anomaly(user.telegram_id)

    if type(anomaly) == str:
        await second_bot.send_message(
                user.telegram_id,
                await render_template("captcha.j2", {"captcha": anomaly}))
        await state.set_state(SignUp.anomaly)
        code = await get_code(state, "anomaly")
        driver.fix_captcha_anomaly(code)
    elif anomaly:
        await second_bot.send_message(
                user.telegram_id,
                await render_template("captcha.j2"))
        with open(f"{BASE_DIR}/temp/{user.telegram_id}.png", "rb") as photo:
            await second_bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=photo)
        await state.set_state(SignUp.anomaly)
        code = await get_code(state, "anomaly")
        driver.fix_photo_anomaly(code)

    if elements:
        await second_bot.send_message(user.telegram_id,
                                      text=await render_template("oauth2.j2"))
        await state.set_state(SignUp.oauth2)
        code = await get_code(state, "oauth2")
        driver.send_authenticator_code(code, elements)
    else:
        driver.skip_oauth2()

    driver.open_diary()
    parcipiant_id = driver.get_participant_id()
    await second_bot.send_message(user.telegram_id,
                           text=parcipiant_id)


def wrap_async_func(user, state):
        asyncio.run(authorize_gosuslugi(user, state))


@router.callback_query(F.data == "yes_correct_data")
async def correct_data(callback: types.CallbackQuery,
                       state: FSMContext):
    user_data = await state.get_data()
    user = User(username=user_data["login"],
                password=user_data["password"],
                telegram_id = callback.message.chat.id)
    await callback.message.edit_text(f"Пытаюсь войти...")
    _thread = threading.Thread(target=wrap_async_func, args=(user, state))
    _thread.start()
    await callback.answer()


@router.message(SignUp.oauth2)
async def oauth2(message: Message,
                 state: FSMContext):
    await state.update_data(oauth2=message.text.lower())


@router.message(SignUp.anomaly)
async def anomaly(message: Message,
                        state: FSMContext):
    await state.update_data(anomaly=message.text.lower())


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
