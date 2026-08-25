import logging
import random

from selenium.webdriver.common.by import By

from src.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, "/")
        self.logger = logging.getLogger("PrestaShop.HomePage")

    def click_next_button(self) -> None:
        self.logger.info("Нажатие кнопки next")
        self.wait_visible(locator=(By.CSS_SELECTOR, 'a[data-slide="next"]')).click()

    def get_carousel_active_text(self) -> str:
        self.logger.info("Получение текста из активного слайда карусели")
        return self.wait_visible(
            locator=(By.CSS_SELECTOR, 'li[class*="carousel-item active"] h2')
        ).text

    def wait_for_carousel_page_change(self, old_text: str, timeout: int = 2) -> None:
        self.logger.info(f"Ожидание изменения карусели с текстом '{old_text}'")
        self._wait.until(
            lambda driver: self.get_carousel_active_text() != old_text,
            message=f"Carousel did not change from '{old_text}' within {timeout} seconds",
        )

    def check_carousel_page_is_changed(self, current_sample) -> None:
        self.logger.info("Проверка, что слайд карусели изменился")
        self.wait_for_carousel_page_change(current_sample)
        assert self.get_carousel_active_text() != current_sample, (
            "Carousel page is not changed"
        )

    def select_unique_product_card(self) -> None:
        self.logger.info("Нажатие на карточку товара")
        self.wait_clickable(
            locator=(By.CSS_SELECTOR, 'article[data-id-product="4"]')
        ).click()

    def get_unique_product_card_text(self) -> str:
        self.logger.info("Получение текста карточки товара")
        return self.wait_visible(
            locator=(By.CSS_SELECTOR, 'article[data-id-product="4"] h3 a')
        ).text.lower()

    def open_random_product_card(self) -> str:
        self.logger.info("Открытие случайной карточки товара")
        product_tiles = self.wait_elements_visible(
            locator=(By.CSS_SELECTOR, 'div[class*="js-product product"]')
        )
        self.logger.info(f"Получение текста выброанного товара: {product_tiles}")
        product_tile = random.choice(product_tiles)
        title = product_tile.text.lower().split("\n")[0]
        product_tile.click()
        return title

    def click_all_products(self) -> None:
        self.logger.info("Нажатие на ссылку 'All products'")
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[href*="2-home"]')).click()

    def click_wishlist_button(self) -> None:
        self.logger.info("Нажатие на кнопку 'Add to wishlist'")
        return self.wait_visible(
            locator=(By.CSS_SELECTOR, 'button[class*="wishlist-button-add"]')
        ).click()

    def check_wishlist_login_modal_is_displayed(self) -> None:
        self.logger.info("Проверка, что модальное окно 'Add to wishlist' появилось")
        assert self.wait_visible(
            locator=(By.CSS_SELECTOR, "div.wishlist-modal[class*=show]")
        ).is_displayed(), "Wishlist login modal did not appear"
