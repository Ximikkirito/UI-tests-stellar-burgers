import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

BASE_URL = "https://stellarburgers.education-services.ru"


class BasePage:
    """Общий родитель для всех Page Object'ов проекта."""

    url = BASE_URL

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    # --- навигация -----------------------------------------------------
    @allure.step("Открыть страницу сайта")
    def open(self):
        self.driver.get(self.url)
        return self

    # --- обёртки над ожиданиями -----------------------------------------
    def find(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def find_clickable(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def is_visible(self, locator, timeout=None):
        try:
            WebDriverWait(self.driver, timeout or self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def is_invisible(self, locator, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def wait_text_not_empty(self, locator, timeout=None):
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda d: d.find_element(*locator).text.strip() != ""
        )
        return self.find(locator).text.strip()

    # --- работа с текущим URL страницы ----------------------------------
    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @allure.step("Дождаться, что открыт URL «{expected_url}»")
    def wait_for_url(self, expected_url: str, timeout=None):
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda d: d.current_url.rstrip("/") == expected_url.rstrip("/")
        )
        return self

    @allure.step("Дождаться, что URL содержит «{substring}»")
    def wait_for_url_contains(self, substring: str, timeout=None):
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda d: substring in d.current_url
        )
        return self

    @allure.step("Дождаться, что URL перестал содержать «{substring}»")
    def wait_for_url_contains_not(self, substring: str, timeout=None):
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda d: substring not in d.current_url
        )
        return self

    # --- авторизация без прохождения формы логина -----------------------
    @allure.step("Подставить в браузер токены авторизованного пользователя")
    def authorize(self, access_token: str, refresh_token: str):
        """Кладёт accessToken в cookie, refreshToken в localStorage и
        обновляет страницу, чтобы приложение подхватило авторизацию,
        минуя форму логина."""
        self.driver.get(self.url)  # нужен домен, чтобы установить cookie/localStorage
        # Подтверждено вручную (DevTools): значение cookie хранит "Bearer "
        # ВМЕСТЕ с токеном — префикс срезать не нужно.
        self.driver.add_cookie({"name": "accessToken", "value": access_token})
        self.driver.execute_script(
            "window.localStorage.setItem('refreshToken', arguments[0]);",
            refresh_token,
        )
        self.driver.refresh()
        return self

    # --- локаторы, общие для шапки сайта --------------------------------

    CONSTRUCTOR_LINK = (By.CSS_SELECTOR, "a[href='/']")
    FEED_LINK = (By.CSS_SELECTOR, "a[href='/feed']")

    @allure.step("Перейти в раздел «Конструктор»")
    def go_to_constructor(self):
        self.find_clickable(self.CONSTRUCTOR_LINK).click()
        return self

    @allure.step("Перейти в раздел «Лента заказов»")
    def go_to_feed(self):
        self.find_clickable(self.FEED_LINK).click()
        return self
