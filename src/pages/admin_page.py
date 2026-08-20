import os
from dotenv import load_dotenv, find_dotenv
from selenium.webdriver import Keys
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.remote.webelement import WebElement
from src.data.data import generate_product
from selenium.webdriver.common.by import By
from src.pages.abc_base_page import AbcBasePage


class AdminPage(AbcBasePage):

    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, '/administration')

        load_dotenv(find_dotenv(".env.test"))
        self.admin_email: str = os.getenv("ADMIN_EMAIL")
        if self.admin_email is None:
            raise ValueError("ADMIN_EMAIL is not set")
        self.admin_password: str = os.getenv("ADMIN_PASSWORD")
        if self.admin_password is None:
            raise ValueError("ADMIN_PASSWORD is not set")

    def input_admin_email(self) -> None:
        admin_email: WebElement = self.wait_visible(locator=(By.ID, 'email'))
        admin_email.clear()
        admin_email.send_keys(self.admin_email)

    def input_admin_password(self) -> None:
        admin_password: WebElement = self.wait_visible(locator=(By.ID, 'passwd'))
        admin_password.clear()
        admin_password.send_keys(self.admin_password)

    def click_login_button(self) -> None:
        self.wait_clickable(locator=(By.ID, 'submit_login')).click()

    def check_admin_page_displayed(self) -> None:
        assert self.wait_visible(
            locator=(By.ID, 'calendar_form')).is_displayed(), "Admin dashboard is not displayed after login"

    def get_employee_infos_menu(self) -> WebElement:
        return self.wait_visible(locator=(By.ID, 'employee_infos'))

    def admin_page_log_in(self) -> None:
        self.input_admin_email()
        self.input_admin_password()
        self.click_login_button()

    def select_log_out(self) -> None:
        self.get_employee_infos_menu().click()
        self.wait_clickable(locator=(By.ID, 'header_logout')).click()

    def check_admin_log_in_page_is_displayed(self) -> None:
        assert self.wait_visible(
            locator=(By.ID, 'login_form')).is_displayed(), "Login to admin page is not displayed after log out"

    def open_catalog_products(self) -> None:
        self.wait_clickable(locator=(By.ID, 'subtab-AdminCatalog')).click()
        self.wait_clickable(locator=(By.ID, 'subtab-AdminProducts')).click()

    def click_new_product(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[data-modal-title*="Add new product"]')).click()

    def switch_to_create_product_frame(self) -> None:
        self.switch_to_frame(locator="modal-create-product-iframe")

    def select_virtual_product(self) -> None:
        self.wait_visible(locator=(By.CSS_SELECTOR, 'button[data-value="virtual"]')).click()

    def close_toolbar(self) -> None:
        self.wait_visible(locator=(By.CSS_SELECTOR, 'a[title="Close Toolbar"]')).click()

    def add_new_product(self) -> None:
        self.wait_clickable(locator=(By.NAME, 'create_product[create]')).click()

    def switch_back(self) -> None:
        self.switch_to_default_content()

    def select_add_new_product(self) -> None:
        self.open_catalog_products()
        self.click_new_product()
        self.switch_to_create_product_frame()
        self.select_virtual_product()
        self.close_toolbar()
        self.add_new_product()
        self.switch_back()

    def fill_header(self, product_name: str):
        self.wait_visible(locator=(By.ID, 'product_header_name_1')).send_keys(product_name)

    def fill_summary(self, summary: str) -> None:
        self.switch_to_frame('product_description_description_short_1_ifr')
        body = self.wait_visible(locator=(By.CSS_SELECTOR, 'body[data-id="product_description_description_short_1"]'))
        self._driver.execute_script("arguments[0].innerHTML = arguments[1];", body, summary)
        self.switch_to_default_content()

    def fill_description(self, description: str) -> None:
        self.switch_to_frame('product_description_description_1_ifr')
        body: WebElement = self.wait_visible(
            locator=(By.CSS_SELECTOR, 'body[data-id="product_description_description_1"]'))
        self._driver.execute_script("arguments[0].innerHTML = arguments[1];", body, description)
        self.switch_to_default_content()

    def fill_description_tab(self, summary: str, description: str) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, "a[href='#product_description-tab']")).click()
        self.fill_summary(summary)
        self.fill_description(description)

    def fill_isbn(self, isbn: str) -> None:
        self.wait_visible(locator=(By.ID, 'product_details_references_isbn')).send_keys(isbn)

    def fill_details_tab(self, isbn: str) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, "a[href='#product_details-tab']")).click()
        self.fill_isbn(isbn)

    def fill_virtual_product_tab(self, min_value: int) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, "a[href='#product_stock-tab']")).click()
        enter_min: WebElement = self.wait_visible(locator=(By.ID, 'product_stock_quantities_minimal_quantity'))
        enter_min.clear()
        enter_min.send_keys(str(min_value))

    def fill_pricing_tab(self, retail_price: int, cost_price: int) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, "a[href='#product_pricing-tab']")).click()
        retail_price_input: WebElement = self.wait_visible(
            locator=(By.ID, 'product_pricing_retail_price_price_tax_excluded'))
        retail_price_input.click()
        retail_price_input.send_keys(Keys.CONTROL, "a")
        retail_price_input.send_keys(Keys.BACKSPACE)
        retail_price_input.send_keys(str(retail_price))
        cost_price_input: WebElement = self.wait_visible(locator=(By.ID, 'product_pricing_wholesale_price'))
        cost_price_input.click()
        cost_price_input.send_keys(Keys.CONTROL, "a")
        cost_price_input.send_keys(Keys.BACKSPACE)
        cost_price_input.send_keys(str(cost_price))

    def fill_seo_tab(self, meta_title: str) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[href="#product_seo-tab"]')).click()
        self.wait_visible(locator=(By.ID, 'product_seo_meta_title_1')).send_keys(meta_title)

    def fill_options_tab(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[href="#product_options-tab"]')).click()

    def fill_new_product_form(self) -> str:
        product = generate_product()
        self.fill_header(product["product_name"])
        self.fill_description_tab(summary=product['summary'], description=product['description'])
        self.fill_details_tab(isbn=product['ISBN'])
        self.fill_virtual_product_tab(min_value=product['min_value'])
        self.fill_pricing_tab(retail_price=product['retail_price'], cost_price=product['cost_price'])
        self.fill_seo_tab(meta_title=product["product_name"])
        self.fill_options_tab()
        return product["product_name"]

    def save_new_product(self) -> None:
        self.wait_clickable(locator=(By.ID, 'product_footer_save')).click()

    def get_the_last_product_name(self) -> str:
        all_products: list[WebElement] = self.wait_elements_visible(locator=(By.CSS_SELECTOR,
                                                                             'td[class*="link-type column-name text-left"] a'))
        added_product_name = all_products[0].text
        return added_product_name

    def check_new_product_was_added(self, product_name) -> None:
        self.open_catalog_products()
        assert self.get_the_last_product_name() == product_name, "New product is not added to catalog"

    def delete_the_last_added_product(self) -> str:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'span[class="menu-collapse"]')).click()
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'a[class="hide-button"]')).click()
        deleted_product: str = self.get_the_last_product_name()
        all_menus: list[WebElement] = self.wait_elements_visible(
            locator=(By.CSS_SELECTOR, 'a[class*="dropdown-toggle-dots"]'))
        all_menus[0].click()
        self.wait_clickable(
            locator=(By.CSS_SELECTOR, 'div[class*="dropdown-menu-right show"] a[class*=''"delete"]')).click()
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'button[class*="btn-confirm-submit"]')).click()
        return deleted_product

    def check_delete_confirmation_displayed_text(self) -> None:
        assert self.wait_visible(
            locator=(By.CSS_SELECTOR, 'div[class="alert-text"]')).text, "Delete confirmation is not displayed"

    def check_product_deleted(self, deleted_product: str) -> None:
        all_products: list[WebElement] = self.wait_elements_visible(locator=(By.CSS_SELECTOR,
                                                                             'td[class*="link-type column-name text-left"] a'))
        for product in all_products:
            assert deleted_product not in product.text, f"Product {deleted_product} is not  deleted"
