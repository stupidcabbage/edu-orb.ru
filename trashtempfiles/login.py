import requests
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class EduSearchLocators:
    "Стандартные искомые элементы электронного дневника."
    LOCATOR_LOGIN_BUTTON = (By.LINK_TEXT, "Вход через ГИС ЕЛК")
    "Кнопка авторизации через гос-услуги."
    LOCATOR_DIARY_BUTTON = (By.ID, 'Дневник учащегося-shortcut')
    "Кнопка дневника учащегося."
    LOCATOR_DIARY_IFRAME = (By.CSS_SELECTOR, "#panel-1074-body > iframe")
    "Фрейм дневника."
    LOCATOR_DAY = (By.CLASS_NAME, "col-wday")
    "Колонка дня недели. (DD.MM. WEEKDAY)."
    LOCATOR_SUBJECT_NAME = (By.CLASS_NAME, "subject-name")
    "Колонка названия предмета."
    LOCATOR_HOMEWORK = (By.CLASS_NAME, "col-homework")
    "Колонка с домашним заданием."
    LOCATOR_OF_ALL_DIARY_ELEMENTS = (By.TAG_NAME, "tr")
    "Список всех элементов дневника."
username = "moxofem939@bnovel.com"
password = "TESTtest1,"


options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome()

url = "https://de.edu.orb.ru/#diary"
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")
button = soup.find('a', class_="btn btn-danger btn-block btn-auth-esia")
login_url = button.attrs["href"]

driver.get(login_url)

driver.find_element(By.ID, "login").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.CLASS_NAME, "plain-button.plain-button_wide").click() # авторизуемся через гос услуги
time.sleep(1)
input_fields = driver.find_elements(By.XPATH, "//input[@type='tel']")
authenticator_code = input()
for i, field in enumerate(input_fields, start=0):
    field.send_keys(int(authenticator_code[i]))
time.sleep(20)
    fields = driver.find_element(By.CLASS_NAME, "plain-button-inline").click() # если нет кода авторизации

