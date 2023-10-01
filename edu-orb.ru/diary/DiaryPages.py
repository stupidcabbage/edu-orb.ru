from BaseApp import BasePageEduOrbRu

from selenium.webdriver.common.by import By


class EduSearchLocators:
    "Стандартные искомые элементы электронного дневника."
    LOCATOR_LOGIN_BUTTON = (By.LINK_TEXT, "Вход через ГИС ЕЛК")
    LOCATOR_DIARY_BUTTON = (By.ID, 'Дневник учащегося-shortcut')
    LOCATOR_DIARY_IFRAME = (By.CSS_SELECTOR, "#panel-1074-body > iframe")
    LOCATOR_DAY = (By.CLASS_NAME, "col-wday")
    LOCATOR_SUBJECT_NAME = (By.CLASS_NAME, "subject-name")
    LOCATOR_HOMEWORK = (By.CLASS_NAME, "col-homework")


class SearchDiaryHelper(BasePageEduOrbRu):
    def open_diary(self):
        "Открывает дневник."
        self.click_on_diary_button()
        self.switch_to_diary_iframe()

    def switch_to_diary_iframe(self):
        "Переходит на фрейм с данными из электронного дневника."
        iframe = self.find_element(EduSearchLocators.LOCATOR_DIARY_IFRAME)
        self.driver.switch_to.frame(iframe)
    
    def click_on_diary_button(self):
        "Запускает фрейм электронного дневника."
        return self.find_element(
                EduSearchLocators.LOCATOR_DIARY_BUTTON).click()

