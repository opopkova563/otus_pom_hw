import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.pages.abc_base_page import AbcBasePage


class BasePage(AbcBasePage):
    def __init__(self, driver: LocalWebDriver, path: str):
        super().__init__(driver, path)
        self.logger = logging.getLogger("PrestaShop.BasePage")

    def change_currency(self) -> str:
        self.logger.info("Получение текущей валюты")
        current_currency: WebElement = self.wait_clickable(
            locator=(By.CSS_SELECTOR, 'span[class*="expand-more"]')
        )
        self.logger.info(f"Текущая валюта: {current_currency.text}")
        current_currency.click()
        self.logger.info("Изменение валюты")
        if "€" in current_currency.text:
            self.wait_clickable(
                locator=(By.CSS_SELECTOR, 'a[title*="US Dollar"]')
            ).click()
        elif "$" in current_currency.text:
            self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[title*="Euro"]')).click()
        else:
            raise Exception("Currency not found")
        self.logger.info("Считывание новой валюты")
        return self.wait_visible(
            locator=(By.CSS_SELECTOR, 'span[class*="expand-more"]')
        ).text

    def check_price_currency(self, currency: str) -> None:
        self.logger.info(f"Проверка, что цены отображаются в валюте {currency}")
        currency = currency[-1]
        all_prices: list[WebElement] = self.wait_elements_visible(
            locator=(By.CSS_SELECTOR, 'span[class*="price"]')
        )
        for price in all_prices:
            assert currency in price.text, f"Price not in correct currency {price.text}"

    def get_page_title(self, locator) -> str:
        self.logger.info("Получение заголовка страницы")
        return self.wait_visible(locator).text.lower()

    def open_cart(self) -> None:
        self.logger.info("Открытие корзины")
        self.wait_clickable(locator=(By.ID, "_desktop_cart")).click()
