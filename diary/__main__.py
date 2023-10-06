from diary.selenium_parser.BasePages import SearchHelper
from diary.services.user import test_user


def get_parcipiant_id():
    driver = SearchHelper()
    driver.go_to_diary_page()
    driver.go_to_gosuslugi_login_page()
    driver.authorize(test_user)
    authorize_keys = int(input())
    driver.send_authenticator_code(authorize_keys)
    driver.open_diary()
    parcipiant_id = driver.get_participant_id()
    print(parcipiant_id)
    
    

get_parcipiant_id()
