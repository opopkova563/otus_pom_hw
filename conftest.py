import os
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.webdriver import LocalWebDriver

from src.exceptions.runtime_errors import BrowserNotSupportedError
from src.pages.admin_page import AdminPage
from src.pages.cart_page import CartPage
from src.pages.catalog_page import CatalogPage
from src.pages.home_page import HomePage
from src.pages.product_card_page import ProductCardPage


@pytest.fixture
def browser() -> Generator[LocalWebDriver, None, None]:
    browser_name: str = (os.getenv("BROWSER")).strip().lower()

    if browser_name == "chrome":
        chrome_options: ChromeOptions = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver: LocalWebDriver = webdriver.Chrome(service=Service(), options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--start-maximized")
        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise BrowserNotSupportedError(f"Browser {browser_name} is not supported")

    yield driver

    driver.quit()

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