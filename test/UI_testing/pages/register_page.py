from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class RegisterPage(BasePage):
    """Register Page Object."""

    # Locators
    PAGE_HEADING = (By.XPATH, "//h2[contains(., 'Create account')]")
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    ROLE_SELECT = (By.NAME, "role")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_ALERT = (By.XPATH, "//div[contains(@style, 'background: rgb(255, 245, 245)') or contains(@style, '#fff5f5')]")
    SIGN_IN_LINK = (By.XPATH, "//a[@href='/login' and contains(., 'Sign in')]")

    def open_register(self):
        return self.open("/register")

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING) and self.is_visible(self.NAME_INPUT)

    def enter_name(self, name: str):
        self.type_text(self.NAME_INPUT, name)

    def enter_email(self, email: str):
        self.type_text(self.EMAIL_INPUT, email)

    def select_role(self, role: str):
        select_elem = self.find_element(self.ROLE_SELECT)
        Select(select_elem).select_by_value(role)

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_INPUT, password)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def register(self, name: str, email: str, password: str, role: str = "player"):
        self.enter_name(name)
        self.enter_email(email)
        self.select_role(role)
        self.enter_password(password)
        self.click_submit()

    def get_error_message(self, timeout: int = 5) -> str:
        return self.get_text(self.ERROR_ALERT, timeout=timeout)

    def is_error_displayed(self, timeout: int = 3) -> bool:
        return self.is_visible(self.ERROR_ALERT, timeout=timeout)

    def click_sign_in(self):
        self.click(self.SIGN_IN_LINK)

    def get_name_validation_message(self) -> str:
        elem = self.find_element(self.NAME_INPUT)
        return self.driver.execute_script("return arguments[0].validationMessage;", elem)

    def get_email_validation_message(self) -> str:
        elem = self.find_element(self.EMAIL_INPUT)
        return self.driver.execute_script("return arguments[0].validationMessage;", elem)

    def get_password_validation_message(self) -> str:
        elem = self.find_element(self.PASSWORD_INPUT)
        return self.driver.execute_script("return arguments[0].validationMessage;", elem)
