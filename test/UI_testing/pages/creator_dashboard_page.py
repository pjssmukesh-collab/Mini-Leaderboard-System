from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CreatorDashboardPage(BasePage):
    """Creator Dashboard Page Object."""

    PAGE_HEADING = (By.XPATH, "//h1[contains(., 'Creator Dashboard') or contains(., 'Creator Studio')]")
    CREATE_TOURNAMENT_BUTTON = (By.XPATH, "//a[@href='/creator/events/create' and contains(., 'Create Tournament')]")
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Search tournament')]")
    
    # Filter buttons
    FILTER_ALL = (By.XPATH, "//button[normalize-space()='All']")
    FILTER_GAMING = (By.XPATH, "//button[contains(., 'Gaming')]")
    FILTER_SPORTS = (By.XPATH, "//button[contains(., 'Sports')]")
    
    # Tournament cards and actions
    TOURNAMENT_CARDS = (By.CLASS_NAME, "card-modern")
    TOURNAMENT_TITLES = (By.XPATH, "//div[contains(@class, 'card-modern')]//h3")
    
    # Action alert
    ACTION_ALERT = (By.XPATH, "//div[contains(@class, 'alert-success') or contains(@class, 'alert-danger')]")
    
    # Edit Modal
    EDIT_NAME_INPUT = (By.XPATH, "//div[contains(@class, 'modal') or contains(@style, 'fixed')]//input[@type='text']")
    EDIT_SAVE_BUTTON = (By.XPATH, "//button[contains(., 'Save Changes')]")
    EDIT_CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Cancel')]")
    
    # Delete Modal
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(., 'Delete Tournament')]")
    DELETE_CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Keep Tournament') or contains(., 'Cancel')]")

    def open_dashboard(self):
        return self.open("/creator/dashboard")

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING)

    def click_create_tournament(self):
        self.click(self.CREATE_TOURNAMENT_BUTTON)

    def search_tournaments(self, query: str):
        self.type_text(self.SEARCH_INPUT, query)

    def get_tournament_titles(self) -> list:
        elements = self.find_elements(self.TOURNAMENT_TITLES)
        return [el.text.strip() for el in elements if el.text.strip()]

    def click_rules_for_event(self, event_id: int):
        locator = (By.XPATH, f"//a[@href='/creator/events/{event_id}/rules']")
        self.click(locator)

    def click_results_for_event(self, event_id: int):
        locator = (By.XPATH, f"//a[@href='/creator/events/{event_id}/results']")
        self.click(locator)

    def click_leaderboard_for_event(self, event_id: int):
        locator = (By.XPATH, f"//a[@href='/player/leaderboard/{event_id}']")
        self.click(locator)

    def get_alert_message(self, timeout: int = 5) -> str:
        return self.get_text(self.ACTION_ALERT, timeout=timeout)
