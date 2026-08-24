import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver

from src.pages.base_page import BasePage


class ProductCardPage(BasePage):
    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, "/stationery/18-37-hummingbird-notebook.html#/")
        self.logger = logging.getLogger("PrestaShop.HomePage")

    def get_product_page_title(self) -> str:
        self.logger.info("Получение заголовка страницы товара")
        return self.get_page_title(locator=(By.CSS_SELECTOR, "h1"))

    def check_product_card_page_is_displayed(self, product_title) -> None:
        self.logger.info("Проверка, что страница товара отображается")
        assert (
            product_title.replace("...", "").strip() in self.get_product_page_title()
        ), "Product page title is not correct"

    def get_paper_type(self) -> str:
        self.logger.info("Получение типа бумаги")
        return self.wait_visible(
            locator=(By.CSS_SELECTOR, "div[class*='product-variants'] span")
        ).text.split(" ")[-1]

    def change_paper_type(self, initial_paper_type: str, timeout: int = 2) -> None:
        self.logger.info("Смена типа бумаги")
        self.wait_clickable(locator=(By.ID, "group_4")).click()
        self.logger.info("Выбор типа бумаги Doted")
        self.wait_clickable(locator=(By.CSS_SELECTOR, "option[title='Doted']")).click()
        self.logger.info("Ждем, пока тип бумаги изменится")
        self._wait.until(
            lambda driver: self.get_paper_type() != initial_paper_type,
            message=f"Paper type is not changed from {initial_paper_type} within {timeout} seconds",
        )

    def add_product_to_cart(self) -> None:
        self.logger.info("Добавление товара в корзину")
        self.wait_clickable(
            locator=(By.CSS_SELECTOR, 'button[class*="add-to-cart"]')
        ).click()

    def check_modal_added_to_cart_is_displayed(self) -> None:
        self.logger.info(
            "Проверка, что модальное окно о добавлении товара в корзину отображается"
        )
        assert self.wait_visible(locator=(By.ID, "myModalLabel")).is_displayed(), (
            "Modal about success add product to cart is not displayed"
        )

    def close_modal_added_to_cart(self) -> None:
        self.logger.info("Закрытие модального окна о добавлении товара в корзину")
        self.wait_clickable(locator=(By.CSS_SELECTOR, ".modal.fade.in .close")).click()

    def check_paper_type_changed(self, initial_paper_type) -> None:
        self.logger.info("Проверка, что тип бумаги изменился")
        new_paper_type = self.get_paper_type()
        assert new_paper_type != initial_paper_type, (
            f"Paper type is not changed from {initial_paper_type} to {new_paper_type}"
        )
