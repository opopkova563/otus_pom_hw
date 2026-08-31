import logging
import os
from abc import ABC
from typing import Self

from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class AbcBasePage(ABC):
    _driver: LocalWebDriver
    _wait: WebDriverWait
    _base_url: str
    _path: str


    def __init__(self, driver: LocalWebDriver, path: str):
        self._driver = driver
        self._wait = WebDriverWait(driver=self._driver, timeout=10)
        self._base_url = os.getenv("BASE_URL")
        self._path = path
        self.logger = logging.getLogger("PrestaShop.AbcBasePage")

    def open(self) -> Self:
        self._driver.get((self._base_url + self._path).strip())
        print(f"Open page {self._base_url + self._path}")
        return self

    def wait_visible(self, locator, timeout=10) -> WebElement:
        return WebDriverWait(self._driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_elements_visible(self, locator, timeout=10) -> list[WebElement]:
        return WebDriverWait(self._driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def wait_located(self, locator, timeout=10) -> WebElement:
        return WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_clickable(self, locator, timeout=10) -> WebElement:
        return WebDriverWait(self._driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_text_on_element(self, locator, text_, timeout=10) -> bool:
        return WebDriverWait(self._driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text_)
        )

    def switch_to_frame(self, locator) -> Self:
        self._wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
        return self

    def switch_to_default_content(self) -> Self:
        self._driver.switch_to.default_content()
        return self
