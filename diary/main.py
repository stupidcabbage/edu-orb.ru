# username = "moxofem939@bnovel.com"
# password = "TESTtest1,"
import json
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

username = os.getenv("login")
password = os.getenv("password")
driver = 1
#
options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome()

url = "https://de.edu.orb.ru/#diary"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0 (Edition Yx GX)"
}

s = requests.Session()
# with open("cookies.json", "r") as f:
#     cookie = json.load(f)
# for cook in cookie:
#     s.cookies.set(cook['name'], cook['value'])
# r = s.get("https://de.edu.orb.ru/#diary")
# r = s.get("https://de.edu.orb.ru/edv/index/diary/A7A48C5F8B939B82826487956E3FA893?date=09.10.2023", headers=headers)
# print(r.text)
# with open("some.txt", "w") as f:
#     f.write(r.text)
cookie = False
if not cookie:
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
    iframe = driver.find_element(By.CSS_SELECTOR, "#panel-1074-body > iframe")
    driver.switch_to.frame(iframe)
    parciant_id = driver.find_element(By.ID, "participant")
    print(parciant_id.get_attribute("data-guid"))
    # time.sleep(2)
    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    # cookies = driver.get_cookies()
    # with open("cookies.json", 'w') as f:
    #     json.dump(cookies, f)

    # diary = driver.find_element(By.CLASS_NAME, "table.table-condensed.table-hover").text
    # a = re.split(r"\d\d.\d\d.\sПонедельник|\d\d.\d\d.\sВторник|\d\d.\d\d.\sСреда|\d\d.\d\d.\sЧетверг|\d\d.\d\d.\sПятница|\d\d.\d\d.\sСуббота", diary)
    # for i in a:
    #     print(i)
    # diary = driver.find_element(By.CLASS_NAME, "table.table-condensed.table-hover")
    # a = diary.find_elements(By.TAG_NAME, "tr")

    # for i in a:
    #     class_attr = i.get_attribute("class") 
    #     if not class_attr:
    #         print("Урок:", i.find_element(By.CLASS_NAME, "col-subject").find_element(By.CLASS_NAME, "subject-name").text)
    #         print("Тема урока:", i.find_element(By.CLASS_NAME, "col-topic").text)
    #         print("Домашнее задание:", i.find_element(By.CLASS_NAME, "col-homework").text)
    #     else:
    #         print(i.get_attribute("class"), i.text)

    # for element in diary:
        # try:
        #     print(element.find_element(By.CLASS_NAME, "subject_name").text, ":", element.find_element(By.CLASS_NAME, "col-homework").text)
        # except Exception:
        #     print(element.find_element(By.CLASS_NAME, "col-wday").text)
        # print("\n")
    # days = driver.find_elements(By.CLASS_NAME, "col-wday")
    # subjects = driver.find_elements(By.CLASS_NAME, "subject-name")
    # homeworks = driver.find_elements(By.CLASS_NAME, "col-homework")
    # for i, subject in enumerate(start=0, iterable=subjects):
    #     print(f"{subject.text}: {homeworks[i].text}")

