import logging
from pathlib import Path

from selenium.webdriver.support.abstract_event_listener import AbstractEventListener


def setup_logger(name="PrestaShop"):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] (%(name)s) %(message)s"
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(logs_dir / f"{name}.log", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


class CustomListener(AbstractEventListener):
    def __init__(self):
        self.log = logging.getLogger("PrestaShop")

    def before_click(self, element, driver):
        self.log.info(
            f"-> [Listener] Готовимся кликнуть по <{element.tag_name}> (текст: '{element.text.strip()}')"
        )

    def after_click(self, element, driver):
        self.log.info("<- [Listener] Клик успешно завершен")

    def on_exception(self, exception, driver):
        self.log.error(f"[Listener] Исключение: {type(exception).__name__}")

    def before_navigate_to(self, url, driver):
        self.log.info(f"-> Открытие URL: {url}")

    def after_navigate_to(self, url, driver):
        self.log.info(f"<- Страница загружена: {url}")

    def get_element_info(self, element) -> str:
        value = element.get_attribute("value") or ""
        name = element.get_attribute("name") or ""
        element_id = element.get_attribute("id") or ""
        return (
            f"<{element.tag_name}> [id='{element_id}', name='{name}', value='{value}']"
        )

    def before_change_value_of(self, element, driver):
        self.log.info(f"-> Изменение значения {self.get_element_info(element)}")

    def after_change_value_of(self, element, driver):
        self.log.info(f"<- Значение изменено {self.get_element_info(element)}")

    def before_execute_script(self, script, driver):
        self.log.debug(f"Выполнение скрипта: {script[:80]}...")

    def after_execute_script(self, script, driver):
        self.log.debug(f"Скрипт выполнен: {script[:80]}...")
