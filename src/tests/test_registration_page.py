from src.pages.user_registration_page import UserRegistrationPage


def test_register_new_user(browser):
    user_registration_page = UserRegistrationPage(browser)
    user_registration_page.open()
    registered_user_first_last_name = user_registration_page.fill_create_an_account_form()
    user_registration_page.save_user()
    user_registration_page.check_registered_user_is_logged(registered_user_first_last_name)
