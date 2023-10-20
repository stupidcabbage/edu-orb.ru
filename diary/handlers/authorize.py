import asyncio
import re
import threading
import time

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ContentType, FSInputFile, Message
from pydantic import Extra

from diary.config import BASE_DIR, second_bot
from diary.handlers.keyboards import SIGNUP_CORRECT_KEYBOARD
from diary.selenium_parser.BasePages import SearchHelper
from diary.services.files import delete_file
from diary.services.user import User
from diary.templates import render_template
from diary.config import EMAIL_REGEX, PHONE_NUMBER_REGEX, SNILS_REGEX, OAUTH2_REGEX


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
    if not _is_correct_login(message):
        await message.answer(await render_template(
            "incorrect_data.j2", {"field": "логин"}))
        return

    await state.update_data(login=message.text)
    user_data = await state.get_data()

    if not user_data.get("password"):
        await _set_password_state_with_message(message, state)
        return
    
    await _check_correctness_of_data(state, message)


@router.message(SignUp.password)
async def get_password(message: Message,
                       state: FSMContext):
    if not _message_is_text(message):
        await message.answer(await render_template(
            "incorrect_data.j2", {"field": "пароль"}))
        return
    await state.update_data(password=message.text)
    await _check_correctness_of_data(state, message)


async def get_code(state: FSMContext,
                   data: str):
    while True:
        value = (await state.get_data()).get(data)
        if value:
            return value
        time.sleep(5)


async def restart_authorize(user: User,
                            state: FSMContext,
                            error: str):
    second_bot.send_message(
            user.telegram_id,
            await render_template("incorrect_authorization.j2",
                                  {"error": error}))
    await state.clear()


async def authorize_gosuslugi(user: User,
                              state: FSMContext):
    driver = SearchHelper()
    driver.go_to_diary_page()
    driver.go_to_gosuslugi_login_page()
    driver.authorize(user)

    if driver.authorize_not_success():
        await restart_authorize(user,
                                state,
                                "Введен неправильный логин или пароль.")
        return

    anomaly = driver.check_anomaly(user.telegram_id)
    if anomaly == "TEXT_CAPTCHA":
        code = await _get_anomaly_code_and_send_message(user, state)
        driver.fix_captcha_anomaly(code)

    elif anomaly == "PHOTO_CAPTCHA":
        code = await _get_anomaly_code_and_send_message(user, state)
        driver.fix_photo_anomaly(code)
    elements = driver.user_has_oauth2()

    if elements:
        code = await _get_oauth2_code_and_send_message(user, state)
        driver.send_authenticator_code(code, elements)
    else:
        driver.skip_oauth2()
    
    if driver.check_oauth2_error():
        await restart_authorize(user, state,
                                "Введен неправильный код двухфакторной аутентификации.")
        return

    anomaly = driver.check_anomaly(user.telegram_id)
    if anomaly == "TEXT_CAPTCHA":
        code = await _get_anomaly_code_and_send_message(user, state)
        driver.fix_captcha_anomaly(code)

    elif anomaly == "PHOTO_CAPTCHA":
        code = await _get_anomaly_code_and_send_message(user, state)
        driver.fix_photo_anomaly(code)
    
    if driver.authorize_not_success():
        await restart_authorize(user, state,
                                "Введен неправильный логин или пароль")
        return

    driver.diary_is_open()
    parcipiant_id = driver.get_phpsessid()
    driver.open_diary()
    parcipiant_id = driver.get_participant_id()
    second_bot.send_message(user.telegram_id,
                                  text=parcipiant_id)
    await state.clear()


def wrap_async_func(user: User, state: FSMContext):
    try:
        asyncio.run(authorize_gosuslugi(user, state))
    except Exception:
        second_bot.send_message(user.telegram_id,
                                "Похоже во время авторизации что-то пошло не так :(")


@router.callback_query(F.data == "yes_correct_data")
async def correct_data(callback: types.CallbackQuery,
                       state: FSMContext):
    user_data = await state.get_data()
    user = User(username=user_data["login"],
                password=user_data["password"],
                telegram_id=callback.message.chat.id)
    await callback.message.edit_text(f"Пытаюсь войти...")
    _thread = threading.Thread(target=wrap_async_func, args=(user, state))
    _thread.start()
    await callback.answer()


@router.message(SignUp.oauth2)
async def oauth2(message: Message,
                 state: FSMContext):
    if not _is_correct_oauth2(message):
        second_bot.send_message(message.chat.id,
                                await render_template("incorrect_data.j2", {"field": "код двухфакторной аутентификации"}))
        return

    await state.update_data(oauth2=message.text.lower())


@router.message(SignUp.anomaly)
async def anomaly(message: Message,
                  state: FSMContext):
    await state.update_data(anomaly=message.text.lower())


@router.callback_query(F.data == "login_incorrect")
async def login_incorrect(callback: types.CallbackQuery,
                          state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(await render_template("login.j2"))
    await callback.answer()
    await state.set_state(SignUp.login)


@router.callback_query(F.data == "password_incorrect")
async def password_incorrect(callback: types.CallbackQuery,
                             state: FSMContext):
    await callback.message.delete()
    await _set_password_state_with_message(callback.message, state)
    await callback.answer()


def _is_correct_oauth2(message: Message) -> bool:
    if not _message_is_text(message):
        return False
    
    oauth2: str = message.text
    return bool(re.match(OAUTH2_REGEX, oauth2))


def _is_correct_login(message: Message) -> bool:
    if not _message_is_text(message):
        return False

    login: str = message.text
    return (bool(re.match(EMAIL_REGEX, login))
            or bool(re.match(PHONE_NUMBER_REGEX, login))
            or bool(re.match(SNILS_REGEX, login)))


async def _check_correctness_of_data(
        state: FSMContext, message: Message) -> None:

    user_data = await state.get_data()
    await message.answer(
            await render_template("correct_data_question.j2", user_data),
            reply_markup=SIGNUP_CORRECT_KEYBOARD())
    await state.set_state()


def _message_is_text(message: Message) -> bool:
    return message.content_type is ContentType.TEXT


async def _set_password_state_with_message(message: Message,
                                          state: FSMContext):
    await message.answer(await render_template("password.j2"))
    await state.set_state(SignUp.password)


async def _get_anomaly_code_and_send_message(
        user: User, state: FSMContext) -> str:
    """
    Отправляет сообщение с обнаружением аномалии и ставит на ожидание получение кода.
    :param user User: пользователь, проходящий регистрацию.
    :param state FSMContext
    :param anomaly str | None: обнаруженная аномалия. Если None - значит фото аномалия.
    """
    second_bot.send_message(
            user.telegram_id,
            await render_template("captcha.j2"))

    path_to_code = f"{BASE_DIR}/temp/{user.telegram_id}.png"
    with open(path_to_code, "rb") as f:
        second_bot.send_photo(
                chat_id=user.telegram_id,
                photo=f)
    delete_file(path_to_code)

    await state.set_state(SignUp.anomaly)
    return await get_code(state, "anomaly")


async def _get_oauth2_code_and_send_message(
        user: User,
        state: FSMContext) -> str:
    """
    Отправляет сообщение с обнаружением OAUTH2 и ставит на ожидание получение кода.
    :param user User: пользователь, проходящий регистрацию.
    :param state FSMContext
    """
    second_bot.send_message(
            user.telegram_id,
            text=await render_template("oauth2.j2"))
    await state.set_state(SignUp.oauth2)
    return await get_code(state, "oauth2")
