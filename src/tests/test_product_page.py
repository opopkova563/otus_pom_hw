import allure


@allure.epic("Страница товара")
@allure.feature("Работа с карточкой товара")
@allure.story("Атрибуты товара")
@allure.title("Изменение типа бумаги")
def test_change_paper_type(browser, product_card_page):
    with allure.step("Получить текущий тип бумаги"):
        initial_paper_type = product_card_page.get_paper_type()
    with allure.step("Изменить тип бумаги"):
        product_card_page.change_paper_type(initial_paper_type)
    with allure.step("Проверить, что тип бумаги изменился"):
        product_card_page.check_paper_type_changed(initial_paper_type)
