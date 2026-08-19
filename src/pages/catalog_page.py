from selenium.webdriver.common.bidi.input import NoneSourceActions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.webdriver import LocalWebDriver

from src.pages.base_page import BasePage


class CatalogPage(BasePage):

    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, '/2-home')

    def sort_by_price_low_to_high(self)  -> list[float]:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'button[class*=select-title]')).click()
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[href*="price.asc"]')).click()
        self.wait_text_on_element(locator=(By.CSS_SELECTOR, 'button[class*=select-title]'), text_='Price, low to high')
        list_of_sorted_prices: list[WebElement] = self.wait_elements_visible(locator=(By.CSS_SELECTOR, 'span[class*="price"]'))

        return [float(price.text[1:]) for price in list_of_sorted_prices]

    def check_list_sorted_by_price(self, actual_list_of_price) -> None:
        price_sorted = sorted(actual_list_of_price)
        assert actual_list_of_price == price_sorted, f"Prices are not sorted {actual_list_of_price}, expected {price_sorted}"

    def open_graphic_corner_filter(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[href*="graphic-corner"]')).click()

    def get_brand_page_title(self) -> str:
        return self.get_page_title(locator=(By.CSS_SELECTOR, 'h1'))

    def get_catalog_page_title(self) -> str:
        return self.get_page_title(locator=(By.CSS_SELECTOR, 'h1'))

    def check_catalog_page_is_opened(self) -> None:
        assert self.get_catalog_page_title() == "home", "Incorrect catalog title"

    def check_graphic_corner_filter_is_opened(self) -> None:
        assert "List of products by brand Graphic Corner".lower() == self.get_brand_page_title(), "Graphic corner filter is not opened"
