from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


from diary.selenium_parser.BaseApp import BasePage
from diary.services.user import User



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
    LOCATOR_LATER_BUTTON = (By.CLASS_NAME, "plain-button-inline")
    "Кнопка пропуска подключения входа с подтверждением."


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


class SearchHelper(BasePage):
    def open_diary(self):
        "Открывает дневник."
        self.click_on_diary_button()
        self.switch_to_diary_iframe()
    
    def go_to_gosuslugi_login_page(self):
        "Переходит на страницу авторизации через гос услуги."
        self.find_element(EduSearchLocators.LOCATOR_LOGIN_BUTTON).click() 
    
    def switch_to_diary_iframe(self):
        "Переходит на фрейм с данными из электронного дневника."
        iframe = self.find_element(EduSearchLocators.LOCATOR_DIARY_IFRAME)
        self.driver.switch_to.frame(iframe)
    
    def click_on_diary_button(self):
        "Открывает фрейм электронного дневника."
        return self.find_element(
                EduSearchLocators.LOCATOR_DIARY_BUTTON).click()
    
    def get_participant_id(self):
        "Возвращает уникальный айди пользователя."
        return self.find_element(
                EduSearchLocators.LOCATOR_PARTICIPANT_ID).get_attribute("data-guid")

    def authorize(self, user: User) -> None:
        "Производит авторизацию через гос услуги, используя логин/пароль."
        self.find_element(
                GosUslugiSearchLocators.LOCATOR_LOGIN_INPUT_FIELD).send_keys(user.username)
        self.find_element(GosUslugiSearchLocators.LOCATOR_PASSWORD_INPUT_FIELD).send_keys(user.password)
        self.find_element(GosUslugiSearchLocators.LOCATOR_LOGIN_BUTTON).click()

    def send_authenticator_code(
            self, authenticator_code: str) -> None:
        "Вписывает код двухэтапной авторизации в поле ввода."
        elements = self.find_elements(
                GosUslugiSearchLocators.LOCATOR_OF_OAUTH2_INPUT_FIELDS)
        for i, field in enumerate(elements, start=0):
            field.send_keys(authenticator_code[i])
    
    def user_has_oauth2(self):
        "Проверяет наличие двухэтапной аутентификации."
        try:
            self.find_element(GosUslugiSearchLocators.LOCATOR_OF_OAUTH2_INPUT_FIELDS,
                             time=1)
        except TimeoutException:
            return False
        return True
    
    def skip_oauth2(self) -> None:
        "Пропускает просьбу о подключении двухэтапной аутентификации."
        self.find_element(GosUslugiSearchLocators.LOCATOR_LATER_BUTTON).click()

    def check_anomaly(self) -> bool | str:
        try:
            anomaly_text = self.driver.find_element(By.XPATH, "/html/body/esia-root/esia-reaction/div/div/div/div/p/text()")
            return True
        except NoSuchElementException:
            return False


    def _get_curent_cookie(self, name_cookie: str):
        "Возвращает определеннный куки."
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie.get("name") == name_cookie:
                return cookie
        else:
            raise COOKIE_DOESNT_EXISTS


    def get_phpsessid(self):
        "Возвращает PHPSESSID cookie."
        return self._get_curent_cookie("PHPSESSID")

    def get_x1_sso_cookie(self):
        "Возвращает X1_SSO cookie."
        return self._get_curent_cookie("X1_SSO")
