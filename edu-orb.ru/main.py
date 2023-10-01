import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# username = "moxofem939@bnovel.com"
# password = "TESTtest1,"

load_dotenv()

username = os.getenv("login")
password = os.getenv("password")

#
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome()

url = "https://de.edu.orb.ru/#diary"
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

cookies = None
if not cookies:
    driver.get(url)
    driver.find_element(By.LINK_TEXT, "Вход через ГИС ЕЛК").click()

    driver.find_element(By.ID, "login").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "plain-button.plain-button_wide").click() # авторизуемся через гос услуги

    time.sleep(1)
    input_fields = driver.find_elements(By.XPATH, "//input[@type='tel']")
    authenticator_code = input()
    for i, field in enumerate(input_fields, start=0):
        field.send_keys(int(authenticator_code[i]))

    button = WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.ID, 'Дневник учащегося-shortcut')))
    button.click()
    time.sleep(2)
    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    iframe = driver.find_element(By.CSS_SELECTOR, "#panel-1074-body > iframe")
    driver.switch_to.frame(iframe)
    diary = driver.find_elements(By.CLASS_NAME, "table.table-condensed.table-hover")
    for element in diary:
        print(element.text)
    # days = driver.find_elements(By.CLASS_NAME, "col-wday")
    # subjects = driver.find_elements(By.CLASS_NAME, "subject-name")
    # homeworks = driver.find_elements(By.CLASS_NAME, "col-homework")
    # for i, subject in enumerate(start=0, iterable=subjects):
    #     print(f"{subject.text}: {homeworks[i].text}")

