from selenium.webdriver.common.webdriver import LocalWebDriver
from src.pages.base_page import BasePage


class BrandGCPage(BasePage):

    def __init__(self, driver: LocalWebDriver):
        super().__init__(driver, '/2-graphic-corner')
