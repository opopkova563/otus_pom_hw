import allure

from src.pages.cart_page import CartPage
from src.pages.catalog_page import CatalogPage
from src.pages.product_card_page import ProductCardPage


@allure.epic("Главная страница")
@allure.feature("Карусель")
@allure.story("Управление каруселью")
@allure.title("Нажатие на кнопку next")
def test_click_carousel_next_button(home_page):
    with allure.step("Получить текст на текущем семпле карусели"):
        current_sample = home_page.get_carousel_active_text()
    with allure.step("Нажатие на кнопку next"):
        home_page.click_next_button()
    with allure.step("Проверка что карусель переключилась на следующий семпл"):
        home_page.check_carousel_page_is_changed(current_sample)


@allure.feature("Работа с товарами")
@allure.story("Катрочки товаров на главной странице")
@allure.title("Проверка цены товара после переключения валюты")
def test_check_prices_after_switching_currency_home(home_page):
    with allure.step("Переключение валюты"):
        currency = home_page.change_currency()
    with allure.step("Проверка цены товара после переключения валюты"):
        home_page.check_price_currency(currency)


@allure.title("Добавление товара в корзину")
def test_add_product_to_cart(browser, home_page):
    with allure.step("Открытие случайного товара"):
        product_title = home_page.open_random_product_card()
    with allure.step("Добавление товара в корзину"):
        product_card_page = ProductCardPage(browser)
        product_card_page.add_product_to_cart()
    with allure.step("Проверка модального окна добавления товара в корзину"):
        product_card_page.check_modal_added_to_cart_is_displayed()
    with allure.step("Закрытие модального окна добавления товара в корзину"):
        product_card_page.close_modal_added_to_cart()
    with allure.step("Открытие корзины"):
        home_page.open_cart()
        cart_page = CartPage(browser)
    with allure.step("Проверка того, что товар добавлен в корзину"):
        cart_page.check_the_product_is_added_to_cart(product_title)


@allure.title("Открытие карточки товара")
def test_tap_on_product_card(browser, home_page):
    with allure.step("Получить текст карточки товара"):
        product_title = home_page.get_unique_product_card_text()
    with allure.step("Нажать на карточку товара"):
        home_page.select_unique_product_card()
    with allure.step("Проверка, что открылась страница карточки товара"):
        product_card_page = ProductCardPage(browser)
        product_card_page.check_product_card_page_is_displayed(product_title)


@allure.title("Нажать на кнопку wishlist")
def test_tap_on_wishlist_button(home_page):
    with allure.step("Нажать на кнопку wishlist"):
        home_page.click_wishlist_button()
    with allure.step("Проверка, что открылось модальное окно логина"):
        home_page.check_wishlist_login_modal_is_displayed()


@allure.feature("Элементы главной страницы")
@allure.story("Ссылки")
@allure.title("Открыть все товары")
def test_select_all_products_link(browser, home_page):
    with allure.step("Нажать на ссылку 'All products'"):
        home_page.click_all_products()
    with allure.step("Проверка, что открылась страница каталога"):
        catalog_page = CatalogPage(browser)
        catalog_page.check_catalog_page_is_opened()
