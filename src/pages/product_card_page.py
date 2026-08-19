from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver

from src.pages.base_page import BasePage


class ProductCardPage(BasePage):

    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, '/stationery/18-37-hummingbird-notebook.html#/')

    def get_product_page_title(self) -> str:
        return self.get_page_title(locator=(By.CSS_SELECTOR, 'h1'))

    def check_product_card_page_is_displayed(self, product_title) -> None:
        assert product_title.replace('...', '').strip() in self.get_product_page_title(), "Product page title is not correct"

    def get_paper_type(self) -> str:
        return self.wait_visible(locator=(By.CSS_SELECTOR, "div[class*='product-variants'] span")).text.split(' ')[-1]

    def change_paper_type(self, initial_paper_type: str, timeout: int = 2) -> None:
        self.wait_clickable(locator=(By.ID, "group_4")).click()
        self.wait_clickable(locator=(By.CSS_SELECTOR, "option[title='Doted']")).click()
        self._wait.until(lambda driver: self.get_paper_type() != initial_paper_type,
                         message=f"Paper type is not changed from {initial_paper_type} within {timeout} seconds")

    def add_product_to_cart(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'button[class*="add-to-cart"]')).click()

    def check_modal_added_to_cart_is_displayed(self) -> None:
        assert self.wait_visible(locator=(By.ID, "myModalLabel")).is_displayed(), "Modal about success add product to cart is not displayed"

    def close_modal_added_to_cart(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, '.modal.fade.in .close')).click()

    def check_paper_type_changed(self, initial_paper_type) -> None:
        new_paper_type = self.get_paper_type()
        assert new_paper_type != initial_paper_type, f"Paper type is not changed from {initial_paper_type} to {new_paper_type}"

