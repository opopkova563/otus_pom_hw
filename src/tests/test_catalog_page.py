import allure


@allure.epic("Каталог")
@allure.feature("Работа с каталогом")
@allure.story("Сортировка")
@allure.title("Сортировка по цене от меньшего к большему")
def test_sort_by_price_low_to_high(catalog_page):
    with allure.step("Сортировка по цене от меньшего к большему"):
        actual_list_of_price = catalog_page.sort_by_price_low_to_high()
    with allure.step("Проверка что каталог отсортировался от меньшего к большему"):
        catalog_page.check_list_sorted_by_price(actual_list_of_price)


@allure.story("Карточки тавара в каталоге")
@allure.title("Проверка цены  на карточке товра после смены валюты")
def test_check_prices_after_switching_currency_catalog(catalog_page):
    with allure.step("Смена валюты"):
        currency = catalog_page.change_currency()
    with allure.step("Проверка что цена на карточке товара соответствует валюте"):
        catalog_page.check_price_currency(currency)


@allure.story("Фильтры")
@allure.title("Открытие фильтра по бренду Graphic Corner")
def test_open_graphic_corner_filter(catalog_page):
    with allure.step("Открытие фильтра по бренду Graphic Corner"):
        catalog_page.open_graphic_corner_filter()
    with allure.step("Проверка что фильтр по бренду Graphic Corner открылся"):
        catalog_page.check_graphic_corner_filter_is_opened()
