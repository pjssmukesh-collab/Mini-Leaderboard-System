from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class RuleBuilderPage(BasePage):
    """Rule Builder and Scoring Configuration Page Object."""

    # Locators
    PAGE_HEADING = (By.XPATH, "//h1[contains(., 'Rule Builder')]")
    METRIC_INPUT = (By.XPATH, "//input[contains(@placeholder, 'kills')]")
    OPERATOR_SELECT = (By.XPATH, "//select[contains(@class, 'form-select')]")
    TARGET_VALUE_INPUT = (By.XPATH, "//input[contains(@placeholder, 'for rank 1')]")
    POINTS_INPUT = (By.XPATH, "//input[contains(@placeholder, '10, 5, or -2')]")
    PRIORITY_INPUT = (By.XPATH, "//label[contains(., 'Priority')]/following-sibling::input")
    ADD_RULE_BUTTON = (By.XPATH, "//button[@type='submit' and contains(., 'Add Scoring Rule')]")
    FINISH_BUTTON = (By.XPATH, "//button[contains(., 'Finish Setup')]")
    PROCEED_RESULTS_BUTTON = (By.XPATH, "//button[contains(., 'Proceed to Results')]")
    RULES_TABLE_ROWS = (By.XPATH, "//table//tbody//tr")
    ERROR_ALERT = (By.CLASS_NAME, "alert-danger")

    def open_rules_page(self, event_id: int):
        self.open(f"/creator/events/{event_id}/rules")
        self.find_element(self.PAGE_HEADING, timeout=10)
        return self

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING) and self.is_visible(self.METRIC_INPUT)

    def add_rule(self, metric: str, points: str, operator: str = "each", target_value: str = "", priority: str = "1"):
        self.type_text(self.METRIC_INPUT, metric)
        if operator != "each":
            select_elem = self.find_element(self.OPERATOR_SELECT)
            Select(select_elem).select_by_value(operator)
            if target_value:
                self.type_text(self.TARGET_VALUE_INPUT, target_value)
        self.type_text(self.POINTS_INPUT, str(points))
        if priority:
            self.type_text(self.PRIORITY_INPUT, str(priority))
        self.click(self.ADD_RULE_BUTTON)

    def get_rules_count(self) -> int:
        return len(self.find_elements(self.RULES_TABLE_ROWS, timeout=3))

    def click_finish(self):
        btn = self.find_element(self.FINISH_BUTTON)
        self.scroll_into_view(btn)
        self.driver.execute_script("arguments[0].click();", btn)

    def click_proceed_to_results(self):
        btn = self.find_element(self.PROCEED_RESULTS_BUTTON)
        self.scroll_into_view(btn)
        self.driver.execute_script("arguments[0].click();", btn)
