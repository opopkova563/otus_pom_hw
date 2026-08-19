import random

from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver, '/')

    def click_next_button(self) -> None:
        self.wait_visible(locator=(By.CSS_SELECTOR, 'a[data-slide="next"]')).click()

    def get_carousel_active_text(self) -> str:
        return self.wait_visible(locator=(By.CSS_SELECTOR, 'li[class*="carousel-item active"] h2')).text

    def wait_for_carousel_page_change(self, old_text: str, timeout: int = 2) -> None:
        self._wait.until(
            lambda driver: self.get_carousel_active_text() != old_text,
            message=f"Carousel did not change from '{old_text}' within {timeout} seconds"
        )

    def check_carousel_page_is_changed(self, current_sample) -> None:
        self.wait_for_carousel_page_change(current_sample)
        assert self.get_carousel_active_text() != current_sample, "Carousel page is not changed"

    def select_unique_product_card(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'article[data-id-product="4"]')).click()

    def get_unique_product_card_text(self) -> str:
        return self.wait_visible(locator=(By.CSS_SELECTOR, 'article[data-id-product="4"] h3 a')).text.lower()

    def open_random_product_card(self) -> str:
        product_tiles = self.wait_elements_visible(locator=(By.CSS_SELECTOR, 'div[class*="js-product product"]'))
        product_tile = random.choice(product_tiles)
        title = product_tile.text.lower().split('\n')[0]
        product_tile.click()
        return title

    def click_all_products(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[href*="2-home"]')).click()

    def click_wishlist_button(self) -> None:
        return self.wait_visible(locator=(By.CSS_SELECTOR, 'button[class*="wishlist-button-add"]')).click()

    def check_wishlist_login_modal_is_displayed(self) -> None:
        assert self.wait_visible(locator=(By.CSS_SELECTOR, 'div.wishlist-modal[class*=show]')).is_displayed(),"Wishlist login modal did not appear"
