from src.pages.cart_page import CartPage
from src.pages.catalog_page import CatalogPage
from src.pages.product_card_page import ProductCardPage


def test_check_prices_after_switching_currency_home(home_page):
    currency = home_page.change_currency()
    home_page.check_price_currency(currency)


def test_add_product_to_cart(browser, home_page):
    product_title = home_page.open_random_product_card()
    product_card_page = ProductCardPage(browser)
    product_card_page.add_product_to_cart()
    product_card_page.check_modal_added_to_cart_is_displayed()
    product_card_page.close_modal_added_to_cart()
    home_page.open_cart()
    cart_page = CartPage(browser)
    cart_page.check_the_product_is_added_to_cart(product_title)


def test_click_carousel_next_button(home_page):
    current_sample = home_page.get_carousel_active_text()
    home_page.click_next_button()
    home_page.check_carousel_page_is_changed(current_sample)


def test_tap_on_product_card(browser, home_page):
    product_title = home_page.get_unique_product_card_text()
    home_page.select_unique_product_card()
    product_card_page = ProductCardPage(browser)
    product_card_page.check_product_card_page_is_displayed(product_title)


def test_select_all_products_link(browser, home_page):
    home_page.click_all_products()
    catalog_page = CatalogPage(browser)
    catalog_page.check_catalog_page_is_opened()


def test_tap_on_wishlist_button(home_page):
    home_page.click_wishlist_button()
    home_page.check_wishlist_login_modal_is_displayed()
