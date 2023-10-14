from typing import Tuple

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    "Общий интерфейс работы с  веб-сайтами."
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("headless")
        self.options.add_argument("--window-size=212,550")
        # self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.driver = webdriver.Chrome(options=self.options)
        self.base_login_url = "https://de.edu.orb.ru/login"
        self.diary_url = "https://de.edu.orb.ru/#diary"

    def find_element(self, locator: Tuple[str, str], time=10) -> WebElement:
        """
        Возвращает первый найденный элемент по заданным параметрам."
        :param locator: Искомый элемент.
        :param time int: Максимальное время поиска элемента.
        """
        return WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located(locator),
                message=f"Не удалось найти элемент {locator}.")

    def find_elements(self, locator: Tuple[str, str], time=10) -> list[WebElement]:
        """
        Нахождение элементов на сайте.
        :param locator: Искомые элементы.
        :param time int: Максимальное время поиска элементов.
        """
        return WebDriverWait(self.driver, time).until(
                EC.presence_of_all_elements_located(locator),
                message=f"Не удалось найти элементы {locator}.")
    
    def get_cookies(self):
        "Возвращает все куки браузера."
        return self.driver.get_cookies()

    def go_to_login_page(self):
        "Загружает страницу авторизации сайта https://de.edu.orb.ru/."
        return self.driver.get(self.base_login_url)

    def go_to_diary_page(self):
        "Загружает страницу дневника учащегося сайта https://de.edu.orb.ru/."
        return self.driver.get(self.diary_url)
