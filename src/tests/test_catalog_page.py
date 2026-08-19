def test_sort_by_price_low_to_high(catalog_page):
    actual_list_of_price = catalog_page.sort_by_price_low_to_high()
    catalog_page.check_list_sorted_by_price(actual_list_of_price)


def test_check_prices_after_switching_currency_catalog(catalog_page):
    currency = catalog_page.change_currency()
    catalog_page.check_price_currency(currency)


def test_open_graphic_corner_filter(catalog_page):
    catalog_page.open_graphic_corner_filter()
    catalog_page.check_graphic_corner_filter_is_opened()
