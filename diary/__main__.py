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
    # print(driver.check_anomaly())
    if driver.user_has_oauth2():
        authorize_keys = input("Введите ключ двухэтапной аутентификации.")
        driver.send_authenticator_code(authorize_keys)
    else:
        driver.skip_oauth2()
    driver.open_diary()
    cookie = driver.get_phpsessid()
    return cookie
    

print(get_parcipiant_id())
