from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LeaderboardPage(BasePage):
    """Leaderboard Page Object."""

    # Locators
    PAGE_HEADING = (By.XPATH, "//h1")
    EVENT_CATEGORY_BADGE = (By.XPATH, "//span[contains(@class, 'badge-soft-primary')]")
    SEARCH_INPUT = (By.XPATH, "//input[contains(@placeholder, 'Search')]")
    EXPORT_CSV_BUTTON = (By.XPATH, "//button[contains(., 'CSV')]")
    EXPORT_JSON_BUTTON = (By.XPATH, "//button[contains(., 'JSON')]")
    RANKINGS_TABLE = (By.TAG_NAME, "table")
    RANKINGS_ROWS = (By.XPATH, "//table//tbody//tr")
    PODIUM_TOP_PLAYERS = (By.XPATH, "//div[contains(@class, 'card-modern')]//h4")

    def open_leaderboard(self, event_id: int):
        return self.open(f"/player/leaderboard/{event_id}")

    def is_page_loaded(self) -> bool:
        return self.is_visible(self.PAGE_HEADING) and self.is_visible(self.RANKINGS_TABLE)

    def search_player(self, player_name: str):
        self.type_text(self.SEARCH_INPUT, player_name)

    def get_rankings_count(self) -> int:
        return len(self.find_elements(self.RANKINGS_ROWS, timeout=5))

    def is_export_csv_available(self) -> bool:
        return self.is_visible(self.EXPORT_CSV_BUTTON)

    def is_export_json_available(self) -> bool:
        return self.is_visible(self.EXPORT_JSON_BUTTON)
