from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PlayerDashboardPage(BasePage):
    """Player Dashboard Page Object."""

    PAGE_HEADING = (By.XPATH, "//h1[contains(., 'Welcome back') or contains(., 'Tournaments')]")
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Search')]")
    SUMMARY_METRIC_CARDS = (By.CLASS_NAME, "stat-card")
    TOURNAMENT_CARDS = (By.XPATH, "//div[contains(@class, 'event-card')]")
    JOIN_BUTTONS = (By.XPATH, "//button[contains(., 'Join Event') or contains(., 'Join Tournament')]")
    LEADERBOARD_LINKS = (By.XPATH, "//a[contains(@href, '/player/leaderboard/')]")
    
    # Status popup modal
    STATUS_POPUP = (By.XPATH, "//div[contains(@class, 'modal')]")
    STATUS_POPUP_TITLE = (By.XPATH, "//div[contains(@class, 'modal')]//h4")
    STATUS_POPUP_CLOSE = (By.XPATH, "//div[contains(@class, 'modal')]//button[contains(., 'Understood') or contains(@class, 'btn-close')]")

    def open_dashboard(self):
        return self.open("/player/dashboard")

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING)

    def search_tournaments(self, query: str):
        self.type_text(self.SEARCH_INPUT, query)

    def get_first_join_button(self):
        buttons = self.find_elements(self.JOIN_BUTTONS)
        return buttons[0] if buttons else None

    def join_first_available_tournament(self):
        btn = self.get_first_join_button()
        if btn:
            self.scroll_into_view(btn)
            btn.click()

    def is_status_popup_displayed(self, timeout: int = 5) -> bool:
        return self.is_visible(self.STATUS_POPUP, timeout=timeout)

    def get_status_popup_title(self) -> str:
        return self.get_text(self.STATUS_POPUP_TITLE)

    def close_status_popup(self):
        self.click(self.STATUS_POPUP_CLOSE)
