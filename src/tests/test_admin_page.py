def test_log_in_to_admin_page(admin_page):
    admin_page.input_admin_email()
    admin_page.input_admin_password()
    admin_page.click_login_button()
    admin_page.check_admin_page_displayed()


def test_log_out_from_admin_page(admin_page):
    admin_page.admin_page_log_in()
    admin_page.select_log_out()
    admin_page.check_admin_log_in_page_is_displayed()


def test_add_new_product(admin_page):
    admin_page.admin_page_log_in()
    admin_page.select_add_new_product()
    product_name = admin_page.fill_new_product_form()
    admin_page.save_new_product()
    admin_page.check_delete_confirmation_displayed_text()
    admin_page.check_new_product_was_added(product_name)


def test_delete_product(admin_page):
    admin_page.admin_page_log_in()
    admin_page.open_catalog_products()
    deleted_product = admin_page.delete_the_last_added_product()
    admin_page.check_product_deleted(deleted_product)
