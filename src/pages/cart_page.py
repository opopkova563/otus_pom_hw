import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, "/cart")
        self.logger = logging.getLogger("PrestaShop.CartPage")

    def get_the_last_product_in_cart_title(self) -> str:
        self.logger.info("Получение названия последнего товара в корзине")
        self.products: list[WebElement] = self.wait_elements_visible(
            locator=(By.CLASS_NAME, "cart-item")
        )
        return self.products[-1].text.lower().split("\n")[0]

    def check_the_product_is_added_to_cart(self, product_title) -> None:
        self.logger.info("Проверка, что товар был добавлен в корзину")
        assert (
            product_title.replace("...", "").strip()
            in self.get_the_last_product_in_cart_title()
        ), "Product was not added to cart"
