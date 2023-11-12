import asyncio
import datetime
import logging
import os
import re
import threading
import time

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from emoji import EMOJI_DATA
from telebot.types import ReplyKeyboardRemove as TReplyKeyboardRemove

from diary.api.parcipiants import get_parcipiants
from diary.config import (BASE_DIR, EMAIL_REGEX, OAUTH2_REGEX,
                          PHONE_NUMBER_REGEX, SNILS_REGEX, db_session,
                          second_bot)
from diary.db.models import AuthorizeUser
from diary.db.models.users import User
from diary.db.services.users import add_user, get_user
from diary.selenium_parser.BasePages import SearchHelper
from diary.telegram.filters import AuthorizeFilter, IsAuthorizedFilter
from diary.telegram.keyboards import (CANCEL_KEYBOARD, SIGNUP_CORRECT_KEYBOARD,
                                      SIGNUP_KEYBOARD_TELEBOT)
from diary.telegram.states import SignUp
from diary.templates import render_template

router = Router()


@router.callback_query(F.data == "signup",
                       AuthorizeFilter(),
                       IsAuthorizedFilter())
async def signup(callback: types.CallbackQuery,
                 state: FSMContext):
    "Авторизация."
    password = (await state.get_data()).get("password")
    if not password:
        await callback.message.edit_text(await render_template("signup.j2"))
    
    await callback.message.answer(await render_template("login.j2"),
                                  reply_markup=CANCEL_KEYBOARD())
    await state.set_state(SignUp.login)


@router.message(SignUp.login)
async def get_login(message: types.Message,
                    state: FSMContext):
    "Логин."
    if not _is_correct_login(message):
        await message.answer(await render_template(
            "incorrect_data.j2", {"field": "логин"}))
        return

    await state.update_data(login=message.text)
    password = (await state.get_data()).get("password")

    if not password:
        await _set_password_state_with_message(message, state)
        return
    
    await _check_correctness_of_data(state, message)


@router.message(SignUp.password)
async def get_password(message: types.Message,
                       state: FSMContext):
    "Пароль."
    if not _is_correct_password(message):
        await message.answer(await render_template(
            "incorrect_data.j2", {"field": "пароль"}))
        return

    await state.update_data(password=message.text)
    await _check_correctness_of_data(state, message)


async def run_code_poiling(state: FSMContext, data: str):
    "Запускает пойлинг с ожиданием кода подтверждения."
    time_end = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M")

    while time_end != datetime.datetime.now().strftime("%H:%M"):
        value = (await state.get_data()).get(data)
        if value:
            return value
        time.sleep(5)
    return None


async def restart_authorize(user: AuthorizeUser,
                            state: FSMContext,
                            error: str):
    "Прекращение авторизации при некорректных появлении ошибок."
    second_bot.send_message(
            user.telegram_id,
            await render_template("incorrect_authorization.j2",
                                  {"error": error}),
            reply_markup=SIGNUP_KEYBOARD_TELEBOT())
    await state.clear()


async def authorize_gosuslugi(driver: SearchHelper,
                              user: AuthorizeUser,
                              state: FSMContext):
    driver.go_to_diary_page()
    driver.go_to_gosuslugi_login_page()
    driver.authorize(user)
    if driver.authorize_not_success():
        await restart_authorize(user,
                                state,
                                "Введен неправильный логин или пароль.")
        return

    anomaly = driver.check_anomaly(user.telegram_id)
    if anomaly:
        code = await _get_anomaly_code_and_send_message(user, state)
        if not code:
            await restart_authorize(user,
                                    state,
                                    "Истекло время ожидания кода.")
            return

        if anomaly == "TEXT_CAPTCHA":
            driver.fix_captcha_anomaly(code)
        elif anomaly == "PHOTO_CAPTCHA":
            driver.fix_photo_anomaly(code)


    elements = driver.user_has_oauth2()

    if elements:
        code = await _get_oauth2_code_and_send_message(user, state)
        if not code:
            await restart_authorize(user,
                                    state,
                                    "Истекло время ожидания кода.")
            return
        driver.send_authenticator_code(code, elements)
    else:
        await restart_authorize(user,
                                state,
                                "Отсутсвует двуфакторная аутентификация.")
        return
    
    if driver.check_oauth2_error():
        await restart_authorize(user, state,
                                "Введен неправильный код двухфакторной аутентификации.")
        return

    anomaly = driver.check_anomaly(user.telegram_id)
    if anomaly:
        code = await _get_anomaly_code_and_send_message(user, state)
        if not code:
            await restart_authorize(user,
                                    state,
                                    "Истекло время ожидания кода.")
            return

        if anomaly == "TEXT_CAPTCHA":
            driver.fix_captcha_anomaly(code)
        elif anomaly == "PHOTO_CAPTCHA":
            driver.fix_photo_anomaly(code)
    
    if driver.authorize_not_success():
        await restart_authorize(user, state,
                                "Введен неправильный логин или пароль")
        return

    driver.diary_is_open()
    phpsessid = driver.get_phpsessid().get("value")
    driver.driver.quit()
    db_user = User(telegram_id=user.telegram_id,
                   phpsessid=phpsessid)
    parcipiant_id = await get_parcipiants(db_user)
    db_user.parcipiants_id = parcipiant_id
    try:
        add_user(db_session, db_user, need_flush=False)
        db_session.commit_session(need_close=True)
    except Exception:
        logging.critical(f"Incorrect create user: {user}")
        db_session.rollback()
        await restart_authorize(user, state,
                                "Некорректное добавление пользователя.")
        return
    if len(parcipiant_id) > 1:
        second_bot.send_message(user.telegram_id,
                                await render_template("chose_user.j2"))
        await state.clear()
        return
    db_user = get_user(db_session, user.telegram_id)
    second_bot.send_message(user.telegram_id,
                            await render_template("success_authorize.j2",
                                                 {"user": db_user.parcipiants_id[0].name}),
                            reply_markup=TReplyKeyboardRemove())
    await state.clear()


def wrap_async_func(user: AuthorizeUser, state: FSMContext):
    driver = SearchHelper()
    try:
        asyncio.run(authorize_gosuslugi(driver, user, state))
    except Exception as e:
        logging.warning(e)
        asyncio.run(restart_authorize(user, state,
                                      "Неизвестная ошибка при авторизации."))
        driver.driver.quit()


@router.callback_query(F.data == "yes_correct_data")
async def correct_data(callback: types.CallbackQuery,
                       state: FSMContext):
    "Начало авторизации на гос услуги."
    user_data = await state.get_data()
    user = AuthorizeUser(username=user_data["login"],
                password=user_data["password"],
                telegram_id=callback.message.chat.id)

    await callback.message.edit_text(await render_template("try_authorize.j2"))
    _thread = threading.Thread(target=wrap_async_func, args=(user, state))
    _thread.start()
    await callback.answer()


@router.message(SignUp.oauth2)
async def oauth2(message: types.Message,
                 state: FSMContext):
    "Код двухфакторной аутентификации."
    if not _is_correct_oauth2(message):
        second_bot.send_message(
                message.chat.id,
                await render_template("incorrect_data.j2", {"field": "код двухфакторной аутентификации"}))
        return

    await state.update_data(oauth2=message.text.lower())


@router.message(SignUp.anomaly)
async def anomaly(message: types.Message,
                  state: FSMContext):
    "Аномалии."
    if not _is_correct_anomaly(message):
        second_bot.send_message(
                message.chat.id,
                await render_template("incorrect_data.j2", {"field": "код"}))
        return

    await state.update_data(anomaly=message.text.lower())


@router.callback_query(F.data == "login_incorrect")
async def login_incorrect(callback: types.CallbackQuery,
                          state: FSMContext):
    "Перезапись логина на гос услугах при авторизации."
    await callback.message.delete()
    await callback.message.answer(await render_template("login.j2"))
    await callback.answer()
    await state.set_state(SignUp.login)


@router.callback_query(F.data == "password_incorrect")
async def password_incorrect(callback: types.CallbackQuery,
                             state: FSMContext):
    "Перезапись пароля на гос услугах при авторизации."
    await callback.message.delete()
    await _set_password_state_with_message(callback.message, state)
    await callback.answer()


def _is_correct_password(message: types.Message) -> bool:
    "Проверка пароля для авторизации на гос услугах."
    return _message_is_text(message)

def _is_correct_anomaly(message: types.Message) -> bool:
    "Проверка кода аномалий для подтверждения личности на гос услугах."
    return _message_is_text(message)

def _is_correct_oauth2(message: types.Message) -> bool:
    """Проверка кода двухфакторной аутентификации 
    на гос услугах перед авторизацией."""
    if not _message_is_text(message):
        return False
    
    return bool(re.match(OAUTH2_REGEX, message.text))


def _is_correct_login(message: types.Message) -> bool:
    "Проверка логина пользователя на гос.услугах перед авторизацией."
    if not _message_is_text(message):
        return False

    login: str = message.text
    return (bool(re.match(EMAIL_REGEX, login))
            or bool(re.match(PHONE_NUMBER_REGEX, login))
            or bool(re.match(SNILS_REGEX, login)))


async def _check_correctness_of_data(
        state: FSMContext, message: types.Message) -> None:
    "Сообщение с просьбой для проверки правильности введеных данных."

    user_data = await state.get_data()
    await message.answer(
            await render_template("correct_data_question.j2", user_data),
            reply_markup=SIGNUP_CORRECT_KEYBOARD())
    await state.set_state()


def _message_is_text(message: types.Message) -> bool:
    """
    Проверяет, что сообщение состоит только из символов:
    латинского алфавита / кириллицы / знаки препинания.
    """
    if not message.content_type is types.ContentType.TEXT:
        return False
    
    if message.text in EMOJI_DATA:
        return False

    for letter in message.text:
        if letter in EMOJI_DATA:
            return False

    return True


async def _set_password_state_with_message(message: types.Message,
                                          state: FSMContext):
    "Отправляет сообщение для отправки пароля пользователем."
    await message.answer(await render_template("password.j2"),
                         reply_markup=CANCEL_KEYBOARD())
    await state.set_state(SignUp.password)


async def _get_anomaly_code_and_send_message(
        user: AuthorizeUser, state: FSMContext) -> str:
    """
    Отправляет сообщение с обнаружением аномалии и ставит на ожидание получение кода.
    :param user AuthorizeUser: пользователь, проходящий регистрацию.
    :param state FSMContext
    :param anomaly str | None: обнаруженная аномалия. Если None - значит фото аномалия.
    """
    second_bot.send_message(
            user.telegram_id,
            await render_template("captcha.j2"))

    path_to_file = f"{BASE_DIR}/temp/{user.telegram_id}.png"
    with open(path_to_file, "rb") as f:
        second_bot.send_photo(
                chat_id=user.telegram_id,
                photo=f)

    os.remove(path_to_file)

    await state.set_state(SignUp.anomaly)
    return await run_code_poiling(state, "anomaly")


async def _get_oauth2_code_and_send_message(
        user: AuthorizeUser,
        state: FSMContext) -> str:
    """
    Отправляет сообщение с обнаружением OAUTH2 и ставит на ожидание получение кода.
    :param user AuthorizeUser: пользователь, проходящий регистрацию.
    :param state FSMContext
    """
    second_bot.send_message(
            user.telegram_id,
            text=await render_template("oauth2.j2"))
    await state.set_state(SignUp.oauth2)
    return await run_code_poiling(state, "oauth2")
