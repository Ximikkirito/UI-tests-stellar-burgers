import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница входа /login  """
    url = BasePage.url + "/login"

    FORM = (By.CSS_SELECTOR, "form.Auth_form__3qKeq")
    EMAIL_INPUT = (By.CSS_SELECTOR, "form.Auth_form__3qKeq input[type='text']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "form.Auth_form__3qKeq input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//form[contains(@class,'Auth_form')]//button[text()='Войти']")

    @allure.step("Войти на сайт под тестовым пользователем")
    def login(self, email: str, password: str):
        self.find(self.EMAIL_INPUT).send_keys(email)
        self.find(self.PASSWORD_INPUT).send_keys(password)
        self.find_clickable(self.LOGIN_BUTTON).click()
        self.wait_for_url_contains_not("/login")
        return self
