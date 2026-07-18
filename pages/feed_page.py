import allure
import time
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FeedPage(BasePage):
    """Раздел «Лента заказов».

    """

    url = BasePage.url + "/feed"

    STATUS_BOX = (By.XPATH, "//div[contains(@class,'OrderFeed_orderStatusBox')]")
    # 1-й <ul> в блоке статусов = колонка "Готовы"
    READY_ORDER_NUMBERS = (
        By.XPATH,
        "(//div[contains(@class,'OrderFeed_orderStatusBox')]//ul)[1]//li",
    )
    # 2-й <ul> в блоке статусов = колонка "В работе"
    IN_PROGRESS_ORDER_NUMBERS = (
        By.XPATH,
        "(//div[contains(@class,'OrderFeed_orderStatusBox')]//ul)[2]//li",
    )

    # Счётчики — число лежит в <p class="OrderFeed_number__...">,
    # следующем сразу за подписью с соответствующим текстом.
    TOTAL_COUNTER = (
        By.XPATH,
        "//p[contains(text(),'Выполнено за все время')]"
        "/following-sibling::p[contains(@class,'OrderFeed_number')]",
    )
    TODAY_COUNTER = (
        By.XPATH,
        "//p[contains(text(),'Выполнено за сегодня')]"
        "/following-sibling::p[contains(@class,'OrderFeed_number')]",
    )

    # Строка заказа в общей ленте (лог всех заказов слева):
    # <li class="OrderHistory_listItem__..."><a href="/feed/{id}">
    #   <p class="text text_type_digits-default">#0389988</p> ...
    FEED_ORDER_ROWS = (By.XPATH, "//li[contains(@class,'OrderHistory_listItem')]")

    @allure.step("Получить значение счётчика «Выполнено за всё время»")
    def get_total_done(self) -> int:
        text = self.wait_text_not_empty(self.TOTAL_COUNTER)
        return int(text) if text.isdigit() else 0

    @allure.step("Получить значение счётчика «Выполнено за сегодня»")
    def get_today_done(self) -> int:
        text = self.wait_text_not_empty(self.TODAY_COUNTER)
        return int(text) if text.isdigit() else 0

    @allure.step("Получить список номеров заказов из блока «В работе»")
    def get_in_progress_order_numbers(self) -> list:
        elements = self.find_all(self.IN_PROGRESS_ORDER_NUMBERS)
        return [el.text.strip().lstrip("#") for el in elements]

    @allure.step("Проверить, что заказ №{order_number} есть в блоке «В работе»")
    def order_in_progress(self, order_number: str) -> bool:
        order_number = order_number.lstrip("#")

        for _ in range(15):
            if order_number in self.get_in_progress_order_numbers():
                return True

            time.sleep(1)
            self.driver.refresh()

        return False
