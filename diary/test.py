from selenium_parser.BasePages import SearchHelper


def authorize_to_gosuslugi(driver, user):
    driver.go_to_diary_page()
    driver.go_to_gosuslugi_login_page()
    driver.authorize(user)


def check_anomaly_while_authorize(driver, message):
    anomaly = driver.check_anomaly()
    if type(anomaly) == str:
        driver.fix_captcha_anomaly(input("Введите код из проверки капчи: "))
    elif anomaly:
        driver.fix_photo_anomaly(input("Введите код из проверки фото капчи: "))
    else:
        return (None)

def make_oauth2(driver, message):
    elements = driver.user_has_oauth2()
    if elements:
        # запрос кода
        driver.send_authenticator_code(input("Введите код двухфакторной аутентификации"), elements)
    else:
        driver.skip_oauth2()


def get_id(driver):
    driver.open_diary()
    cookie = driver.get_phpsessid()
    parcipiant_id = driver.get_participant_id()
    return parcipiant_id, cookie

def test(user):
   driver = SearchHelper()
   authorize_to_gosuslugi(driver, user)
   anomaly = driver.check_anomaly(user.telegram_id)
