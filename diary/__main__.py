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
    anomaly = driver.check_anomaly()
    print(anomaly)
    if type(anomaly) == str:
        driver.fix_captcha_anomaly(input("Введите код из проверки капчи: "))
    elif anomaly:
        driver.fix_photo_anomaly(input("Введите код из проверки фото капчи: "))
    else:
        print(None)
    elements = driver.user_has_oauth2()
    if elements:
        driver.send_authenticator_code(input("Введите код двухфакторной аутентификации"), elements)
    else:
        driver.skip_oauth2()
    driver.open_diary()
    cookie = driver.get_phpsessid()
    parcipiant_id = driver.get_participant_id()
    return cookie, parcipiant_id

print(get_parcipiant_id())
