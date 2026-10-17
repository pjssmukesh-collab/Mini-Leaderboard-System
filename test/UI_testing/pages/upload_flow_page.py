from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pathlib import Path

class UploadFlowPage(BasePage):
    """Results File Upload, Validation, and Processing Flow Page Object."""

    # Locators
    PAGE_HEADING = (By.XPATH, "//h1[contains(., 'Process Match Results')]")
    FILE_INPUT = (By.XPATH, "//input[@type='file']")
    UPLOAD_PARSE_BUTTON = (By.XPATH, "//button[contains(., 'Upload & Parse Results')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Cancel')]")
    FILE_NAME_BADGE = (By.XPATH, "//span[contains(@class, 'fw-semibold')]")
    
    # Step 2: Validation Report
    VALIDATION_HEADER = (By.XPATH, "//h2[contains(., 'Validation & Player Verification')]")
    VALID_RECORDS_COUNT = (By.XPATH, "//div[contains(@class, 'text-success') and contains(@class, 'h3')]")
    CALCULATE_SCORES_BUTTON = (By.XPATH, "//button[contains(., 'Calculate Scores & Publish Leaderboard') or contains(., 'Publish')]")
    
    # Error state
    EXTRACTION_ERROR_TITLE = (By.XPATH, "//h4[contains(., 'Extraction Could Not Complete')]")
    ERROR_ALERT = (By.CLASS_NAME, "alert-danger")

    def open_upload_page(self, event_id: int):
        return self.open(f"/creator/events/{event_id}/results")

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING) and self.is_visible(self.FILE_INPUT)

    def select_file(self, file_path: Path):
        """Sends the absolute file path to the hidden or styled file input element."""
        file_input = self.find_element(self.FILE_INPUT)
        file_input.send_keys(str(file_path.resolve()))

    def click_upload(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.UPLOAD_PARSE_BUTTON))
        self.scroll_into_view(btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def is_validation_report_displayed(self, timeout: int = 10) -> bool:
        return self.is_visible(self.VALIDATION_HEADER, timeout=timeout)

    def is_extraction_error_displayed(self, timeout: int = 8) -> bool:
        return self.is_visible(self.EXTRACTION_ERROR_TITLE, timeout=timeout)

    def get_valid_records_count(self) -> str:
        return self.get_text(self.VALID_RECORDS_COUNT)

    def click_calculate_scores(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CALCULATE_SCORES_BUTTON))
        self.scroll_into_view(btn)
        self.driver.execute_script("arguments[0].click();", btn)
