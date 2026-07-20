import allure
import pytest

from pages.main_page import MainPage
from pages.feed_page import FeedPage

BUN_NAME = "Краторная булка N-200i"
FILLING_NAME = "Биокотлета из марсианской Магнолии"


@allure.epic("Stellar Burgers")
@allure.feature("Основная функциональность")
class TestConstructorNavigation:

    @allure.story("Переход по клику на «Конструктор»")
    @pytest.mark.constructor
    def test_click_constructor_link_opens_constructor(self, driver):
        page = MainPage(driver).open()
        page.go_to_feed()  # уходим со стартовой страницы
        page.wait_for_url_contains("/feed")
        page.go_to_constructor()
        page.wait_for_url(MainPage.url)
        assert page.current_url.rstrip("/") == MainPage.url.rstrip("/"), (
            "После клика на «Конструктор» должен открыться раздел конструктора"
        )

    @allure.story("Переход по клику на «Лента заказов»")
    @pytest.mark.constructor
    def test_click_feed_link_opens_feed(self, driver):
        page = MainPage(driver).open()
        page.go_to_feed()
        page.wait_for_url_contains("/feed")
        assert "/feed" in page.current_url, (
            "После клика на «Лента заказов» URL должен содержать /feed"
        )


@allure.epic("Stellar Burgers")
@allure.feature("Основная функциональность")
class TestIngredientModal:

    @allure.story("Клик по ингредиенту открывает модальное окно с деталями")
    @pytest.mark.constructor
    def test_ingredient_click_opens_modal(self, driver):
        page = MainPage(driver).open()
        page.click_ingredient(BUN_NAME)
        assert page.modal_is_open(), "После клика по ингредиенту должно открыться модальное окно"

    @allure.story("Модальное окно закрывается по клику на крестик")
    @pytest.mark.constructor
    def test_modal_closes_by_cross_click(self, driver):
        page = MainPage(driver).open()
        page.click_ingredient(BUN_NAME)
        assert page.modal_is_open(), "Предусловие: модальное окно должно быть открыто"
        page.close_modal()
        assert page.modal_is_closed(), "После клика на крестик модальное окно должно закрыться"


@allure.epic("Stellar Burgers")
@allure.feature("Основная функциональность")
class TestIngredientCounter:

    @allure.story("Счётчик ингредиента увеличивается при добавлении в заказ")
    @pytest.mark.constructor
    def test_ingredient_counter_increases(self, driver):
        page = MainPage(driver).open()
        counter_before = page.get_ingredient_counter(FILLING_NAME)

        page.add_ingredient_to_order(FILLING_NAME)

        counter_after = page.get_ingredient_counter(FILLING_NAME)
        assert counter_after == counter_before + 1, (
            f"Счётчик ингредиента должен увеличиться на 1: было {counter_before}, стало {counter_after}"
        )
