import pytest
from pages.leaderboard_page import LeaderboardPage

@pytest.mark.ui
@pytest.mark.leaderboard
class TestLeaderboard:
    """Test suite for the tournament leaderboard, rankings table, search, and export features."""

    def test_leaderboard_page_loads(self, driver):
        """Verify leaderboard page loads with rankings table and tournament info."""
        leaderboard_page = LeaderboardPage(driver)
        leaderboard_page.open_leaderboard(event_id=1)
        
        assert leaderboard_page.is_page_loaded(), "Leaderboard page or rankings table failed to load."
        assert leaderboard_page.is_visible(leaderboard_page.SEARCH_INPUT), "Search player input missing."

    def test_leaderboard_export_buttons_present(self, driver):
        """Verify export buttons (CSV and JSON) are rendered on the leaderboard."""
        leaderboard_page = LeaderboardPage(driver)
        leaderboard_page.open_leaderboard(event_id=1)
        
        assert leaderboard_page.is_export_csv_available(), "Export CSV button is not available."
        assert leaderboard_page.is_export_json_available(), "Export JSON button is not available."

    def test_leaderboard_player_search_filter(self, driver):
        """Verify player search input accepts text without throwing errors."""
        leaderboard_page = LeaderboardPage(driver)
        leaderboard_page.open_leaderboard(event_id=1)
        
        leaderboard_page.search_player("mukesh")
        input_elem = leaderboard_page.find_element(leaderboard_page.SEARCH_INPUT)
        assert input_elem.get_attribute("value") == "mukesh"
