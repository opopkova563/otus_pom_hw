import allure

from src.pages.user_registration_page import UserRegistrationPage


@allure.epic("Страница регистрации нового пользователя")
@allure.feature("Регистрации пользователя")
@allure.story("Форма регистрации нового пользователя")
@allure.title("Успешная регистрация нового пользователя")
def test_register_new_user(browser):
    with allure.step("Открыть страницу регистрации нового пользователя"):
        user_registration_page = UserRegistrationPage(browser)
        user_registration_page.open()
    with allure.step("Заполнить форму регистрации нового пользователя"):
        registered_user_first_last_name = (
            user_registration_page.fill_create_an_account_form()
        )
    with allure.step("Сохранить нового пользователя"):
        user_registration_page.save_user()
    with allure.step("Проверить, что новый пользователь зарегистрировался"):
        user_registration_page.check_registered_user_is_logged(
            registered_user_first_last_name
        )
