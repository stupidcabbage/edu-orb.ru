from BaseApp import BasePageGosUslugi
from services.user import User

from selenium.webdriver.common.by import By


class GosUslugiSearchLocators:
    "Стандартные искомые элементы для гос услуг."
    LOCATOR_LOGIN_INPUT_FIELD = (By.ID, "login")
    "Поле ввода логина пользователя."
    LOCATOR_PASSWORD_INPUT_FIELD = (By.ID, "password")
    "Поле ввода пароля пользователя."
    LOCATOR_LOGIN_BUTTON = (By.CLASS_NAME, "plain-button.plain-button_wide")
    "Кнопка входа в гос услуги"
    LOCATOR_OF_OAUTH2_INPUT_FIELDS = (By.XPATH, "//input[@type='tel']")
    "Поля ввода для кода двухэтапной аутентификации."


class SearchGosUslugiHelper(BasePageGosUslugi):
    def authorize(self, user: User) -> None:
        "Производит авторизацию через гос услуги, используя логин/пароль."
        self.find_element(
                GosUslugiSearchLocators.LOCATOR_LOGIN_BUTTON).send_keys(user.username)
        self.find_element(GosUslugiSearchLocators.LOCATOR_PASSWORD_INPUT_FIELD).send_keys(user.password)
        self.find_element(GosUslugiSearchLocators.LOCATOR_LOGIN_BUTTON).click()
