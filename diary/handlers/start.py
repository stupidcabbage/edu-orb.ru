from dataclasses import replace
from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import re


EMAIL_REGEX = r"^\S+@\S+\.\S+$"
PHONE_NUMBER_REGEX = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
SNILS_REGEX = r"^\d{1,3}(\s*\d{3})*$"

class SignUp(StatesGroup):
    login = State()
    password = State()
    correct_data = State()
    oauth2 = State()

router = Router()


def is_correct_login(login: str) -> bool:
    return (bool(re.match(EMAIL_REGEX, login))
            or bool(re.match(PHONE_NUMBER_REGEX, login))
            or bool(re.match(SNILS_REGEX, login)))


@router.message(CommandStart())
async def command_start(message: Message):
    if message.from_user.id != 11226590290:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="🚪Зарегистрироваться",
            callback_data="signup"))
        await message.answer("Привет, похоже ты здесь впервые!",
                             reply_markup=builder.as_markup())
    else:
        await message.answer(f"Привет, хозяин!")


@router.callback_query(F.data == "signup")
async def signup(callback: types.CallbackQuery,
                 state: FSMContext):
    user_data = await state.get_data()
    if not user_data.get("password"):
        await callback.message.answer("Похоже что ты крутой парень, раз решил регистрироваться.")
    await callback.message.answer("Введи свой логин от гос услуг.")
    await state.set_state(SignUp.login)
    await callback.answer()


def get_keyboad():
    buttons = [
            [types.InlineKeyboardButton(text="Да, они верны! ✅", callback_data="yes_correct_data")],
            [types.InlineKeyboardButton(text="Нужно исправить логин!", callback_data="signup"),
            types.InlineKeyboardButton(text="Нужно исправить пароль!", callback_data="password_incorrect")]
            ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


@router.message(SignUp.login)
async def get_login(message: Message,
                    state: FSMContext):
    if not is_correct_login(message.text):
        await message.answer("Похоже, что ты вводишь неправильный логин. Уверен во всех цифрах и буквах?")
    else:
        await state.update_data(login=message.text)
        user_data = await state.get_data()
        if not user_data.get("password"):
            await message.answer(
                    text="Увидел твой логин, отлично. Что насчет пароля, колись.")
            await state.set_state(SignUp.password)
        else:
            await message.answer(text=f"логин: {user_data['login']}, пароль: {user_data['password']}. Correct?",
                         reply_markup=get_keyboad())
            await state.set_state()



@router.message(SignUp.password)
async def get_password(message: Message,
                       state: FSMContext):
    user_data = await state.get_data()
    user_data = await state.update_data(password=message.text)
    await message.answer(text=f"логин: {user_data['login']}, пароль: {user_data['password']}. Correct?",
                         reply_markup=get_keyboad())
    await state.set_state()


@router.callback_query(F.data == "yes_correct_data")
async def correct_data(callback: types.CallbackQuery,
                       state: FSMContext):
    user_data = await state.get_data()
    await callback.message.answer(f"{user_data['login']}, {user_data.get('password')}")
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "password_incorrect")
async def password_incorrect(callback: types.CallbackQuery,
                             state: FSMContext):
    await state.set_state(SignUp.password)
    await callback.message.answer("Введи новый пароль, друг")
    await callback.answer()
