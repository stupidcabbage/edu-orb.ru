import datetime
from typing import Literal, Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from diary.config import BASE_DIR
from diary.db.models import AuthorizeUser as User
from diary.selenium_parser.BaseApp import BasePage


class COOKIE_DOESNT_EXISTS(Exception):
    "Исключение, если в искоемые cookie отсутствует"
    pass


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
    LOCATOR_OF_ANOMALY_PHOTO_INPUT_FIELD = (By.XPATH, "//input[@type='text']")
    "Поле ввода кода фото капчи."
    LOCATOR_OF_ANOMALY_TEXT_INPUT_FIELD = (By.XPATH, "//input[@class='input__field']")
    "Поле ввод кода текстовой капчи."
    LOCATOR_OF_ANOMALY_PHOTO_BUTTON = (By.XPATH, "//button[@class='code-entry__button button']")
    "Кнопка подтверждения фото капчи."
    LOCATOR_OF_ANOMALY_TEXT_BUTTON = (By.XPATH, "//button[@class='input__button anomaly__button']")
    "Кнопка подтверждения текстовой капчи."
    LOCATOR_OF_OAUTH2_ANOMALY = (By.XPATH, "//div[@class='error-label mt-4 mb-4']")
    "Класс ошибки при неправильном вводе кода двухфакторной аутентификации."
    LOCATOR_OF_ANOMALY_CLASS = (By.CLASS_NAME, "anomaly")
    "Класс аномалий."
    LOCATOR_OF_IMAGE_CAPTCHA = (By.CLASS_NAME, "esia-captcha__image")
    "Фотография с капчой."
    LOCATOR_OF_TEXT_CAPTCHA = (By.XPATH, "//p[@class='anomaly__plain-text abstract-request-information__text']")
    "Вопрос текстовой каптчи."


class EduSearchLocators:
    "Стандартные искомые элементы электронного дневника."
    LOCATOR_LOGIN_BUTTON = (By.LINK_TEXT, "Вход через ГИС ЕЛК")
    "Кнопка авторизации через гос-услуги."
    LOCATOR_DIARY_BUTTON = (By.ID, 'Дневник учащегося-shortcut')
    "Кнопка дневника учащегося."
    LOCATOR_DIARY_IFRAME = (By.CSS_SELECTOR, "#panel-1074-body > iframe")
    "Фрейм дневника."
    LOCATOR_PARTICIPANT_ID = (By.ID, "participant")
    "Уникальный айди пользователя."
    LOCATOR_OF_MENU_BUTTON = (By.ID, "button-1061-btnInnerEl")


class SearchHelper(BasePage):
    def go_to_gosuslugi_login_page(self):
        "Переходит на страницу авторизации через гос услуги."
        self.find_element(EduSearchLocators.LOCATOR_LOGIN_BUTTON).click() 
    
    def open_diary(self):
        "Открывает дневник."
        self.driver.get("https://de.edu.orb.ru/edv/index/participant")

    def diary_is_open(self):
        """
        Проверяет, что пользователь после страницы авторизации
        перешел на сайт дневника.
        """
        try:
            return self.find_element(EduSearchLocators.LOCATOR_OF_MENU_BUTTON)
        except TimeoutException:
            return False
    
    def get_participant_id(self) -> Optional[str]:
        "Возвращает уникальный айди пользователя."
        return self.find_element(
                EduSearchLocators.LOCATOR_PARTICIPANT_ID).get_attribute("data-guid")
    
    def make_exception_screenshot(self) -> None:
        "Делает скриншот экрана в случае возникновения ошибки."
        filename = f"{datetime.datetime.now().strftime('exception_%d.%m.%y_%H_%M_%S')}.png"
        self.make_fullscreen_screenschot(f"{BASE_DIR}/temp/{filename}")


    def authorize(self, user: User) -> None:
        "Производит авторизацию через гос услуги, используя логин/пароль."
        self.find_element(
                GosUslugiSearchLocators.LOCATOR_LOGIN_INPUT_FIELD).send_keys(user.username)
        self.find_element(GosUslugiSearchLocators.LOCATOR_PASSWORD_INPUT_FIELD).send_keys(user.password)
        self.find_element(GosUslugiSearchLocators.LOCATOR_LOGIN_BUTTON).click()

    def send_authenticator_code(
            self, authenticator_code: str, elements: list[WebElement]) -> None:
        "Вписывает код двухэтапной авторизации в поле ввода."
        for i, field in enumerate(elements, start=0):
            field.send_keys(authenticator_code[i])

    def user_has_oauth2(self) -> list[WebElement] | Literal[False]:
        "Проверяет наличие двухэтапной аутентификации."
        try:
            return self.find_elements(
                    GosUslugiSearchLocators.LOCATOR_OF_OAUTH2_INPUT_FIELDS,
                    time=15)
        except TimeoutException:
            return False
    
    def fix_photo_anomaly(self, code: str) -> None:
        "Решает фото каптчу."
        self.find_element(GosUslugiSearchLocators.LOCATOR_OF_ANOMALY_PHOTO_INPUT_FIELD).send_keys(code)
        self.find_element(GosUslugiSearchLocators.LOCATOR_OF_ANOMALY_PHOTO_BUTTON).click()

    def fix_captcha_anomaly(self, code: str) -> None:
        "Решает текстовую каптчу."
        self.find_element(GosUslugiSearchLocators.LOCATOR_OF_ANOMALY_TEXT_INPUT_FIELD).send_keys(code)
        self.find_element(GosUslugiSearchLocators.LOCATOR_OF_ANOMALY_TEXT_BUTTON).click()
    
    def check_oauth2_error(self):
        "Проверяет, что код OAUTH2 введен корректно."
        try:
            self.find_element(GosUslugiSearchLocators.LOCATOR_OF_OAUTH2_ANOMALY, time=3)
            return True
        except TimeoutException:
            return False

    def check_anomaly(self, telegram_id: int):
        "Проверяет на наличие аномалий при авторизации."
        try:
            self.find_element(GosUslugiSearchLocators.LOCATOR_OF_ANOMALY_CLASS, time=2)
            try:
                self.find_element(GosUslugiSearchLocators.LOCATOR_OF_IMAGE_CAPTCHA, time=2).screenshot(f"{BASE_DIR}/temp/{telegram_id}.png")
                return "PHOTO_CAPTCHA"
            except TimeoutException:
                self.find_element(GosUslugiSearchLocators.LOCATOR_OF_TEXT_CAPTCHA, time=2).screenshot(f"{BASE_DIR}/temp/{telegram_id}.png")
                return "TEXT_CAPTCHA"
        except TimeoutException:
            return False


    def _get_curent_cookie(self, name_cookie: str):
        "Возвращает определеннный куки."
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie.get("name") == name_cookie:
                return cookie
        raise COOKIE_DOESNT_EXISTS

    def authorize_not_success(self) -> bool:
        try:
            self.find_element((By.XPATH, "//div[@class='error-label']"), time=1)
            return True
        except TimeoutException:
            return False

    def get_phpsessid(self):
        "Возвращает PHPSESSID cookie."
        return self._get_curent_cookie("PHPSESSID")
