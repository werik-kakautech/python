from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, username, password):
        self.wait_for_element_visible(self.USERNAME_INPUT).send_keys(username)
        self.wait_for_element_visible(self.PASSWORD_INPUT).send_keys(password)
        self.wait_for_element_clickable(self.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.wait_for_element_visible(self.ERROR_MESSAGE).text

    def is_login_successful(self):
        return "inventory.html" in self.driver.current_url