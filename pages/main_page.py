import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.js_dnd import drag_and_drop


class MainPage(BasePage):
    """Главная страница / раздел «Конструктор»."""

    url = BasePage.url + "/"

    # ------------------------------------------------------------------
    # Локаторы построены по реальному DOM сайта (снят через DevTools).
    # CSS-классы этого проекта хэшируются сборщиком (например,
    # "BurgerIngredient_ingredient__1TVf6" — суффикс "1TVf6" может
    # смениться при пересборке), поэтому там, где это возможно, матчим
    # по стабильной части имени класса через contains(), а не по
    # хэш-суффиксу целиком.
    # ------------------------------------------------------------------

    # Вкладки категорий ингредиентов ("Булки" / "Соусы" / "Начинки")
    TAB_BUNS = (By.XPATH, "//span[text()='Булки']")
    TAB_SAUCES = (By.XPATH, "//span[text()='Соусы']")
    TAB_FILLINGS = (By.XPATH, "//span[text()='Начинки']")

    # Зона конструктора, куда перетаскиваются ингредиенты:
    # <section class="BurgerConstructor_basket__29Cd7 ...">
    CONSTRUCTOR_DROP_ZONE = (By.XPATH, "//section[contains(@class,'BurgerConstructor_basket__')]")

    # Кнопка "Оформить заказ" — единственная primary-кнопка в футере
    # конструктора: <div class="BurgerConstructor_basket__container...">
    # <button class="button_button_type_primary...">
    ORDER_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'BurgerConstructor_basket__container')]"
        "//button[contains(@class,'button_button_type_primary')]",
    )

    # Модальное окно рендерится в DOM всегда (их несколько: детали
    # ингредиента / номер заказа / лоадер), но активное — то, у которого
    # к базовому классу "Modal_modal__..." добавлен модификатор
    # "Modal_modal_opened__...".
    MODAL_OPENED = (By.XPATH, "//section[contains(@class,'Modal_modal_opened')]")
    MODAL_CLOSE_BUTTON = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]//button[contains(@class,'Modal_modal__close')]",
    )
    # Название ингредиента внутри модалки деталей:
    # <p class="text text_type_main-medium mb-8">Краторная булка N-200i</p>
    MODAL_INGREDIENT_NAME = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]"
        "//div[contains(@class,'Modal_modal__contentBox')]/p[contains(@class,'text_type_main-medium')]",
    )
    # Номер заказа в модалке подтверждения:
    # <h2 class="... text_type_digits-large mb-8">9999</h2>
    ORDER_NUMBER_IN_MODAL = (
        By.XPATH,
        "//section[contains(@class,'Modal_modal_opened')]//h2[contains(@class,'text_type_digits-large')]",
    )

    # ------------------------------------------------------------------
    # Ингредиенты
    # ------------------------------------------------------------------

    def ingredient_card(self, name: str):
        """Карточка ингредиента в общем списке (не модалка):
        <a class="BurgerIngredient_ingredient__..." href="/ingredient/{id}">
            <div class="counter_counter__..."><p class="counter_counter__num__...">0</p></div>
            <img alt="{name}" .../>
            <p class="BurgerIngredient_ingredient__text__...">{name}</p>
        </a>
        В списке (в отличие от модалки!) alt картинки совпадает с названием
        ингредиента — это подтверждено реальным DOM."""
        return (
            By.XPATH,
            f"//a[contains(@class,'BurgerIngredient_ingredient__')][.//img[@alt='{name}']]",
        )

    def ingredient_counter(self, name: str):
        """Числовой бейдж-счётчик — он есть в DOM всегда (даже "0"),
        просто может быть визуально скрыт при нулевом значении."""
        return (
            By.XPATH,
            f"//a[contains(@class,'BurgerIngredient_ingredient__')][.//img[@alt='{name}']]"
            f"//p[contains(@class,'counter_counter__num')]",
        )

    @allure.step("Получить значение счётчика ингредиента «{name}»")
    def get_ingredient_counter(self, name: str) -> int:
        text = self.find(self.ingredient_counter(name)).text.strip()
        return int(text) if text.isdigit() else 0

    @allure.step("Кликнуть по ингредиенту «{name}»")
    def click_ingredient(self, name: str):
        self.find_clickable(self.ingredient_card(name)).click()
        return self

    @allure.step("Добавить ингредиент «{name}» в конструктор (drag&drop)")
    def add_ingredient_to_order(self, name: str):
        source = self.find(self.ingredient_card(name))
        target = self.find(self.CONSTRUCTOR_DROP_ZONE)
        drag_and_drop(self.driver, source, target)
        return self

    # ------------------------------------------------------------------
    # Модальное окно
    # ------------------------------------------------------------------

    @allure.step("Проверить, что модальное окно открыто")
    def modal_is_open(self) -> bool:
        return self.is_visible(self.MODAL_OPENED, timeout=5)

    @allure.step("Закрыть модальное окно крестиком")
    def close_modal(self):
        self.find_clickable(self.MODAL_CLOSE_BUTTON).click()
        return self

    @allure.step("Проверить, что модальное окно закрыто")
    def modal_is_closed(self) -> bool:
        try:
            self.is_invisible(self.MODAL_OPENED, timeout=5)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Оформление заказа
    # ------------------------------------------------------------------

    @allure.step("Нажать «Оформить заказ»")
    def submit_order(self):
        self.find_clickable(self.ORDER_BUTTON).click()
        return self

    @allure.step("Получить номер оформленного заказа из модального окна")
    def get_order_number_from_modal(self) -> str:
        return self.wait_text_not_empty(self.ORDER_NUMBER_IN_MODAL)
