from aiogram.fsm.state import State, StatesGroup


class SignUp(StatesGroup):
    "Авторизация."
    login = State()
    password = State()
    correct_data = State()
    anomaly = State()
    oauth2 = State()
    last_bot_message = State()
