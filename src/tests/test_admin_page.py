import allure


@allure.epic("Панель администратора")
@allure.feature("Авторизация")
@allure.story("Вход в панель администратора")
@allure.title("Успешный вход в админ-панель")
def test_log_in_to_admin_page(admin_page):
    with allure.step("Ввести email администратора"):
        admin_page.input_admin_email()
    with allure.step("Ввести пароль администратора"):
        admin_page.input_admin_password()
    with allure.step("Нажать кнопку логина"):
        admin_page.click_login_button()
    with allure.step("Проверить, что панель администратора открылась"):
        admin_page.check_admin_page_displayed()


@allure.title("Успешный выход из админ-панель")
def test_log_out_from_admin_page(admin_page):
    with allure.step("Войтив панель администратора"):
        admin_page.admin_page_log_in()
    with allure.step("Выйти из панели администратора"):
        admin_page.select_log_out()
    with allure.step("Проверить, что панель администратора закрылась"):
        admin_page.check_admin_log_in_page_is_displayed()


@allure.feature("Работа с каталогом")
@allure.story("Продукты")
@allure.title("Добавление нового продукта")
def test_add_new_product(admin_page):
    with allure.step("Войти в панель администратора"):
        admin_page.admin_page_log_in()
    with allure.step("Нажать на кнопку 'New product'"):
        admin_page.select_add_new_product()
    with allure.step("Заполнить форму нового продукта"):
        product_name = admin_page.fill_new_product_form()
    with allure.step("Нажать на кнопку 'Save'"):
        admin_page.save_new_product()
    with allure.step("Проверить, что продукт добавлен"):
        admin_page.check_delete_confirmation_displayed_text()
        admin_page.check_new_product_was_added(product_name)


@allure.title("Удаление последнего добавленного продукта")
def test_delete_product(admin_page):
    with allure.step("Войти в панель администратора"):
        admin_page.admin_page_log_in()
    with allure.step("Открыть каталог продуктов"):
        admin_page.open_catalog_products()
    with allure.step("Удалить последний добавленный продукт"):
        deleted_product = admin_page.delete_the_last_added_product()
    with allure.step("Проверить, что продукт удален"):
        admin_page.check_product_deleted(deleted_product)
