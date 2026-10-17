from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Login Page Object."""

    # Locators
    PAGE_HEADING = (By.XPATH, "//h2[contains(., 'Welcome back')]")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_ALERT = (By.XPATH, "//div[contains(@style, 'background: rgb(255, 245, 245)') or contains(@style, '#fff5f5')]")
    CREATE_ACCOUNT_LINK = (By.XPATH, "//a[@href='/register' and contains(., 'Create one')]")

    def open_login(self):
        return self.open("/login")

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING) and self.is_visible(self.EMAIL_INPUT)

    def enter_email(self, email: str):
        self.type_text(self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_INPUT, password)

    def click_submit(self):
        self.click(self.SUBMIT_BUTTON)

    def login(self, email: str, password: str):
        """Fills credentials and submits the login form."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()

    def get_error_message(self, timeout: int = 5) -> str:
        """Retrieves text from the error alert."""
        return self.get_text(self.ERROR_ALERT, timeout=timeout)

    def is_error_displayed(self, timeout: int = 3) -> bool:
        return self.is_visible(self.ERROR_ALERT, timeout=timeout)

    def click_create_account(self):
        self.click(self.CREATE_ACCOUNT_LINK)

    def get_email_validation_message(self) -> str:
        """Retrieves HTML5 validation message for email input."""
        elem = self.find_element(self.EMAIL_INPUT)
        return self.driver.execute_script("return arguments[0].validationMessage;", elem)

    def get_password_validation_message(self) -> str:
        """Retrieves HTML5 validation message for password input."""
        elem = self.find_element(self.PASSWORD_INPUT)
        return self.driver.execute_script("return arguments[0].validationMessage;", elem)
