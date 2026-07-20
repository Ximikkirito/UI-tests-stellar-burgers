import allure
import pytest

from pages.main_page import MainPage
from pages.feed_page import FeedPage
from pages.login_page import LoginPage

BUN_NAME = "Краторная булка N-200i"
FILLING_NAME = "Биокотлета из марсианской Магнолии"

def _create_order(driver, authorized_user) -> str:
    # Авторизация через UI
    login_page = LoginPage(driver).open()

    # login() сам дожидается редиректа со страницы /login (см. LoginPage)
    login_page.login(
        "21312312312312@mail.ru",
        "1234567"
    )

    # Переходим на главную
    page = MainPage(driver).open()

    # Собираем бургер
    page.add_ingredient_to_order(BUN_NAME)
    page.add_ingredient_to_order(FILLING_NAME)

    # конструкторе (счётчик обновился), прежде чем оформлять заказ
    page.wait_ingredient_counter_at_least(FILLING_NAME, 1)

    # Оформляем заказ
    page.submit_order()

    order_number = page.get_order_number_from_modal()

    # page.close_modal()

    return order_number



@allure.epic("Stellar Burgers")
@allure.feature("Лента заказов")
class TestOrderFeedCounters:

    @allure.story("Счётчик «Выполнено за всё время» увеличивается при создании заказа")
    @pytest.mark.feed
    def test_total_done_counter_increases(self, driver, authorized_user):
        feed_before = FeedPage(driver).open()
        total_before = feed_before.get_total_done()

        _create_order(driver, authorized_user)

        feed_after = FeedPage(driver).open()
        total_after = feed_after.get_total_done()
        assert total_after >= total_before + 1, (
            f"Счётчик «Выполнено за всё время» должен увеличиться: было {total_before}, стало {total_after}"
        )

    @allure.story("Счётчик «Выполнено за сегодня» увеличивается при создании заказа")
    @pytest.mark.feed
    def test_today_done_counter_increases(self, driver, authorized_user):
        feed_before = FeedPage(driver).open()
        today_before = feed_before.get_today_done()

        _create_order(driver, authorized_user)

        feed_after = FeedPage(driver).open()
        today_after = feed_after.get_today_done()
        assert today_after >= today_before + 1, (
            f"Счётчик «Выполнено за сегодня» должен увеличиться: было {today_before}, стало {today_after}"
        )


@allure.epic("Stellar Burgers")
@allure.feature("Лента заказов")
class TestOrderInProgress:

    @allure.story("Номер оформленного заказа появляется в блоке «В работе»")
    @pytest.mark.feed
    def test_new_order_appears_in_progress_block(self, driver, authorized_user):
        order_number = _create_order(driver, authorized_user)

        feed_page = FeedPage(driver).open()
        assert feed_page.order_in_progress(order_number), (
            f"Заказ №{order_number} должен появиться в блоке «В работе»"
        )


