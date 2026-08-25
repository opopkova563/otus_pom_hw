import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.pages.base_page import BasePage


class CatalogPage(BasePage):
    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, "/2-home")
        self.logger = logging.getLogger("PrestaShop.CatalogPage")

    def sort_by_price_low_to_high(self) -> list[float]:
        self.logger.info("Сортировка товаров по цене от низкой к высокой")
        self.wait_clickable(
            locator=(By.CSS_SELECTOR, "button[class*=select-title]")
        ).click()
        self.logger.info("Выбор сортировки по цене от низкой к высокой")
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[href*="price.asc"]')).click()
        self.wait_text_on_element(
            locator=(By.CSS_SELECTOR, "button[class*=select-title]"),
            text_="Price, low to high",
        )
        self.logger.info("Считывание цены товаров")
        list_of_sorted_prices: list[WebElement] = self.wait_elements_visible(
            locator=(By.CSS_SELECTOR, 'span[class*="price"]')
        )

        return [float(price.text[1:]) for price in list_of_sorted_prices]

    def check_list_sorted_by_price(self, actual_list_of_price) -> None:
        self.logger.info("Проверка, что товары отсортированы по цене")
        price_sorted = sorted(actual_list_of_price)
        assert actual_list_of_price == price_sorted, (
            f"Prices are not sorted {actual_list_of_price}, expected {price_sorted}"
        )

    def open_graphic_corner_filter(self) -> None:
        self.logger.info("Открытие фильтра по бренду Graphic Corner")
        self.wait_clickable(
            locator=(By.CSS_SELECTOR, 'a[href*="graphic-corner"]')
        ).click()

    def get_brand_page_title(self) -> str:
        self.logger.info("Получение заголовка страницы брена")
        return self.get_page_title(locator=(By.CSS_SELECTOR, "h1"))

    def get_catalog_page_title(self) -> str:
        self.logger.info("Получение заголовка страницы каталога")
        return self.get_page_title(locator=(By.CSS_SELECTOR, "h1"))

    def check_catalog_page_is_opened(self) -> None:
        self.logger.info("Проверка, что открыта страница каталога")
        assert self.get_catalog_page_title() == "home", "Incorrect catalog title"

    def check_graphic_corner_filter_is_opened(self) -> None:
        self.logger.info("Проверка, что открыт фильтр по бренду Graphic Corner")
        assert (
            "List of products by brand Graphic Corner".lower()
            == self.get_brand_page_title()
        ), "Graphic corner filter is not opened"
