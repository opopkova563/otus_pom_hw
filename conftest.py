import os
from collections.abc import Generator

import allure
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.support.events import EventFiringWebDriver

import logger_config
from logger_config import setup_logger
from src.exceptions.runtime_errors import BrowserNotSupportedError
from src.pages.admin_page import AdminPage
from src.pages.cart_page import CartPage
from src.pages.catalog_page import CatalogPage
from src.pages.home_page import HomePage
from src.pages.product_card_page import ProductCardPage

logger = setup_logger()


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    logger_config.setup_logger()
    yield


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture()
def browser(request) -> Generator[LocalWebDriver, None, None]:
    browser_name: str = request.config.getoption("--browser").strip().lower()

    if browser_name == "chrome":
        chrome_options: ChromeOptions = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        driver: LocalWebDriver = webdriver.Chrome(
            service=Service(), options=chrome_options
        )
    elif browser_name == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--start-maximized")
        firefox_options.add_argument("--headless")

        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise BrowserNotSupportedError(f"Browser {browser_name} is not supported")
    listener = logger_config.CustomListener()
    driver = EventFiringWebDriver(driver, listener)

    yield driver

    driver.quit()
    logger.info("Браузер закрыт.\n")


@pytest.fixture
def home_page(browser):
    return HomePage(browser).open()


@pytest.fixture
def catalog_page(browser):
    return CatalogPage(browser).open()


@pytest.fixture
def admin_page(browser):
    return AdminPage(browser).open()


@pytest.fixture
def product_card_page(browser):
    return ProductCardPage(browser).open()


@pytest.fixture
def cart_page(browser):
    return CartPage(browser).open()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Ищем фикстуру с драйвером (например, 'driver' или 'browser')
        driver = item.funcargs.get("browser")
        if driver is not None:
            try:
                screenshot_name = f"failure_{item.name}"

                if hasattr(driver, "name"):
                    screenshot_name = f"{screenshot_name}_{driver.name}"

                # Прикрепляем скриншот в Allure
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"failure_{item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот для теста '{item.name}': {e}")
