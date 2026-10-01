from collections.abc import Generator

import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.events import EventFiringWebDriver

import logger_config
from logger_config import setup_logger
from src.exceptions.runtime_errors import BrowserNotSupportedError
from src.pages.admin_page import AdminPage
from src.pages.cart_page import CartPage
from src.pages.catalog_page import CatalogPage
from src.pages.home_page import HomePage
from src.pages.product_card_page import ProductCardPage

load_dotenv('.env.test')

logger = setup_logger()


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    logger_config.setup_logger()
    yield


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Браузер: chrome или firefox. По умолчанию chrome"
    )

    parser.addoption(
        "--browser-version",
        action="store",
        default=None,
        help="Версия браузера для Selenoid, например: 128.0"
    )

    parser.addoption(
        "--selenoid-url",
        action="store",
        default=None,
        help="URL Selenoid/GGR, например: http://localhost/wd/hub"
    )


@pytest.fixture()
def browser(request) -> Generator[LocalWebDriver, None, None]:
    browser_name: str = request.config.getoption("--browser").strip().lower()
    browser_version: str | None = request.config.getoption("--browser-version")
    selenoid_url: str | None = request.config.getoption("--selenoid-url", default=None)

    if selenoid_url:
            driver = _create_remote_driver(
                browser_name=browser_name,
                browser_version=browser_version,
                selenoid_url=selenoid_url,
                test_name=request.node.name,
            )
    else:
        driver = _create_local_driver(browser_name)

    listener = logger_config.CustomListener()
    event_driver = EventFiringWebDriver(driver, listener)

    yield event_driver

    event_driver.quit()
    logger.info("Браузер закрыт.")


def _create_remote_driver(browser_name: str,
        browser_version: str | None,
        selenoid_url: str,
        test_name: str,
                    ) -> WebDriver:
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

    else:
        raise BrowserNotSupportedError(
            f"Browser '{browser_name}' is not supported. "
            "Supported browsers: chrome, firefox."
        )

    if browser_version:
        options.browser_version = browser_version

    options.set_capability(
        "selenoid:options",
        {
            "enableVNC": True,
            "enableVideo": False,
            "name": f"test_{test_name}",
            "sessionTimeout": "10m",
        },
    )

    logger.info(
        "Удаленный запуск: browser=%s, version=%s, url=%s",
        browser_name,
        browser_version or "default",
        selenoid_url,
    )

    return webdriver.Remote(
        command_executor=selenoid_url,
        options=options,
    )


def _create_local_driver(browser_name: str) -> WebDriver:
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")

        logger.info("Локальный запуск Chrome")

        return webdriver.Chrome(
            service=Service(),
            options=options,
        )

    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        logger.info("Локальный запуск Firefox")

        return webdriver.Firefox(options=options)

    raise BrowserNotSupportedError(
        f"Browser '{browser_name}' is not supported. "
        "Supported browsers: chrome, firefox."
    )



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
