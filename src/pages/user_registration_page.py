from selenium.webdriver.common.by import By
from selenium.webdriver.common.webdriver import LocalWebDriver
from src.data.data import generate_user

from src.pages.base_page import BasePage


class UserRegistrationPage(BasePage):

    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, '/registration')

    def fill_create_an_account_form(self) -> str:
        user = generate_user()
        locator_gender = (
            (By.CSS_SELECTOR, 'input#field-id_gender-1')
            if user["gender"] == "male"
            else (By.CSS_SELECTOR, 'input#field-id_gender-2')
        )

        self.wait_located(locator_gender).click()
        self.wait_visible(locator=(By.CSS_SELECTOR, 'input#field-firstname')).send_keys(user["first_name"])
        self.wait_visible(locator=(By.CSS_SELECTOR, 'input#field-lastname')).send_keys(user["last_name"])
        email = self.wait_visible(locator=(By.CSS_SELECTOR, 'input#field-email'))
        email.clear()
        email.send_keys(user["email"])

        password = self.wait_visible(locator=(By.CSS_SELECTOR, 'input#field-password'))
        password.clear()
        password.send_keys(user["password"])

        self.wait_visible(locator=(By.CSS_SELECTOR, 'input#field-birthday')).send_keys(user["birthdate"])

        self.wait_located(locator=(By.CSS_SELECTOR, 'input[name="optin"]')).click()
        self.wait_located(locator=(By.CSS_SELECTOR, 'input[name="psgdpr"]')).click()
        self.wait_located(locator=(By.CSS_SELECTOR, 'input[name="newsletter"]')).click()
        self.wait_located(locator=(By.CSS_SELECTOR, 'input[name="customer_privacy"]')).click()

        return user["first_name"] + ' ' + user["last_name"]

    def save_user(self) -> None:
        self.wait_clickable(locator=(By.CSS_SELECTOR, 'button[data-link-action="save-customer"]')).click()

    def get_logged_user(self) -> str:
        return self.wait_visible(locator=(By.CSS_SELECTOR, '[class*="user-info"] span')).text

    def check_registered_user_is_logged(self, registered_user_first_last_name) -> None:
        assert self.get_logged_user() == registered_user_first_last_name, f"New user {registered_user_first_last_name} is not created"

