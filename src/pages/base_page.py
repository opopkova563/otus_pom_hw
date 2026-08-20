from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.pages.abc_base_page import AbcBasePage


class BasePage(AbcBasePage):

    def change_currency(self) -> str:
        current_currency: WebElement = self.wait_clickable(locator=(By.CSS_SELECTOR, 'span[class*="expand-more"]'))
        current_currency.click()
        if "€" in current_currency.text:
            self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[title*="US Dollar"]')).click()
        elif "$" in current_currency.text:
            self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[title*="Euro"]')).click()
        else:
            raise Exception("Currency not found")
        return self.wait_visible(locator=(By.CSS_SELECTOR, 'span[class*="expand-more"]')).text

    def check_price_currency(self, currency: str) -> None:
        currency = currency[-1]
        all_prices: list[WebElement] = self.wait_elements_visible(locator=(By.CSS_SELECTOR, 'span[class*="price"]'))
        for price in all_prices:
            assert currency in price.text, f"Price not in correct currency {price.text}"

    def get_page_title(self, locator) -> str:
        return self.wait_visible(locator).text.lower()

    def open_cart(self) -> None:
        self.wait_clickable(locator=(By.ID, '_desktop_cart')).click()
