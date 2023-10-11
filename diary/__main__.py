import json

from diary.selenium_parser.BasePages import SearchHelper
from diary.services.user import test_user


def write_cookie_to_file(cookies, file: str = "cookies.json"):
    with open(file, "w") as f:
        json.dump(cookies, f)


def get_parcipiant_id():
    driver = SearchHelper()
    driver.go_to_diary_page()
    driver.go_to_gosuslugi_login_page()
    driver.authorize(test_user)
    authorize_keys = int(input())
    driver.send_authenticator_code(authorize_keys)
    driver.open_diary()
    cookie = driver.get_phpsessid()
    write_cookie_to_file(cookie)
    

get_parcipiant_id()
