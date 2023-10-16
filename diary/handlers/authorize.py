import re
import threading

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ContentType, Message

from config import BASE_DIR
from handlers.keyboards import SIGNUP_CORRECT_KEYBOARD
from selenium_parser.BasePages import SearchHelper
from services.user import User
from templates import render_template

EMAIL_REGEX = r"^\S+@\S+\.\S+$"
PHONE_NUMBER_REGEX = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
SNILS_REGEX = r"^\d{1,3}(\s*\d{3})*$"


router = Router()

driver = SearchHelper()

class Test(StatesGroup):
    test = State()

class SignUp(StatesGroup):
    login = State()
    password = State()
    correct_data = State()
    text_anomaly = State()
    photo_anomaly = State()
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


async def test_3(message: Message,
                 state: FSMContext):
    print(1)
    while True:
        if (await state.get_data()).get("test"):
            message.answer("aaa")

@router.message(Test.test)
async def test_2(message: Message,
                 state: FSMContext):
    await state.update_data({"test": message.text.lower()})
    await message.answer("Принял!")


@router.message(Command("test"))
async def test(message: Message,
               state: FSMContext):
    await message.answer("Навали говна")
    await state.set_state(Test.test)
    threading.Thread(target=test_3, args=(message, state))

async def test_in_one_func(state: FSMContext,
                     user):
    driver = SearchHelper()
    authorize_to_gosuslugi(driver, user)
    anomaly = driver.check_anomaly(user.telegram_id)
    if type(anomaly) == str:
        await state.set_state()
        

def authorize_to_gosuslugi(driver, user):
    driver.go_to_diary_page()
    driver.go_to_gosuslugi_login_page()
    driver.authorize(user)


@router.callback_query(F.data == "yes_correct_data")
async def correct_data(callback: types.CallbackQuery,
                       state: FSMContext):
    user_data = await state.get_data()
    user = User(username=user_data["login"],
                password=user_data["password"],
                telegram_id = callback.message.from_user.id)
    await callback.message.edit_text(f"Пытаюсь войти...")
    await callback.answer()
    
    await callback.message.answer(parcipiant_id)

@router.message(SignUp.oauth2)
async def oauth2(message: Message,
                 state: FSMContext):
    elements = driver.user_has_oauth2()
    value = message.text.lower()
    driver.send_authenticator_code(value, elements)

    driver.open_diary()
    parcipiant_id = driver.get_participant_id()
    driver.driver.close()
    await message.answer(parcipiant_id)


@router.message(SignUp.photo_anomaly)
async def photo_anomaly(message: Message,
                        state: FSMContext):
    user_data = await state.get_data()
    driver: SearchHelper = user_data["driver"]
    value = message.text.lower()
    driver.fix_photo_anomaly(value)
    await state.set_state(SignUp.oauth2)


@router.message(SignUp.text_anomaly)
async def text_anomaly(message: Message,
                  state: FSMContext):
    user_data = await state.get_data()
    driver: SearchHelper = user_data["driver"]
    value = message.text.lower()
    driver.fix_captcha_anomaly(value)
    await state.set_state(SignUp.oauth2)

    

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
