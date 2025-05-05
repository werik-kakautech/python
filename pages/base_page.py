from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from typing import Tuple, Any, List
from logger import Logger

class BasePage:
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = Logger.get_logger(self.__class__.__name__)

    def navigate_to(self, url: str) -> None:
        self.logger.info(f"Navegando para: {url}")
        self.driver.get(url)
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> Any:
        timeout = timeout or self.timeout
        self.logger.debug(f"Aguardando elemento visível: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = None) -> Any:
        timeout = timeout or self.timeout
        self.logger.debug(f"Aguardando elemento clicável: {locator}")
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        element = self.wait_for_element_visible(locator)
        return element.text
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        element = self.wait_for_element_visible(locator)
        return element.get_attribute(attribute)
    
    def find_elements(self, locator: Tuple[str, str]) -> List[Any]:
        by, value = locator
        return self.driver.find_elements(by, value)
    
    def execute_javascript(self, script: str, *args) -> Any:
        return self.driver.execute_script(script, *args)