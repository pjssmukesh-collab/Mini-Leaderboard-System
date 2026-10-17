from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CreateEventPage(BasePage):
    """Create Tournament Event Page Object."""

    # Locators
    PAGE_HEADING = (By.XPATH, "//h1[contains(., 'Create New Tournament')]")
    BACK_LINK = (By.XPATH, "//a[contains(., 'Back to Dashboard')]")
    NAME_INPUT = (By.NAME, "name")
    EVENT_TYPE_INPUT = (By.NAME, "event_type")
    DESCRIPTION_TEXTAREA = (By.NAME, "description")
    PARTICIPANT_LIMIT_INPUT = (By.NAME, "participant_limit")
    START_DATE_INPUT = (By.NAME, "start_date")
    END_DATE_INPUT = (By.NAME, "end_date")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Cancel')]")
    ERROR_ALERT = (By.CLASS_NAME, "alert-danger")

    def open_create_event(self):
        self.open("/creator/events/create")
        self.wait_for_url_contains("/creator/events/create")
        self.find_element(self.NAME_INPUT)
        return self

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING) and self.is_visible(self.NAME_INPUT)

    def select_preset_category(self, category_label: str):
        locator = (By.XPATH, f"//button[contains(., '{category_label}')]")
        self.click(locator)

    def fill_form(self, name: str, event_type: str, description: str = "", participant_limit: str = "50"):
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EVENT_TYPE_INPUT, event_type)
        if description:
            self.type_text(self.DESCRIPTION_TEXTAREA, description)
        if participant_limit:
            self.type_text(self.PARTICIPANT_LIMIT_INPUT, str(participant_limit))

    def submit_form(self):
        btn = self.find_element(self.SUBMIT_BUTTON)
        self.scroll_into_view(btn)
        self.driver.execute_script("arguments[0].closest('form').requestSubmit();", btn)

    def click_cancel(self):
        btn = self.find_element(self.CANCEL_BUTTON)
        self.scroll_into_view(btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def get_error_message(self, timeout: int = 5) -> str:
        return self.get_text(self.ERROR_ALERT, timeout=timeout)

    def get_name_validation_message(self) -> str:
        elem = self.find_element(self.NAME_INPUT)
        return self.driver.execute_script("return arguments[0].validationMessage;", elem)
