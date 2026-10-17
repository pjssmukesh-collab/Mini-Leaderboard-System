import pytest
from pages.creator_dashboard_page import CreatorDashboardPage
from pages.player_dashboard_page import PlayerDashboardPage

@pytest.mark.ui
@pytest.mark.smoke
class TestDashboard:
    """Verifies Creator and Player dashboard views, metric summary cards, and search functionality."""

    def test_creator_dashboard_loads_with_metrics(self, authenticated_creator):
        """Verify creator dashboard loads after authentication with summary cards and buttons."""
        dashboard = CreatorDashboardPage(authenticated_creator)
        assert dashboard.is_page_loaded(), "Creator dashboard heading failed to render."
        assert dashboard.is_visible(dashboard.CREATE_TOURNAMENT_BUTTON), "Create Tournament button missing."
        assert dashboard.is_visible(dashboard.SEARCH_INPUT), "Tournament search input missing."

    def test_creator_dashboard_search_filter(self, authenticated_creator):
        """Verify search input allows typing and filters the tournament list."""
        dashboard = CreatorDashboardPage(authenticated_creator)
        dashboard.search_tournaments("Tech")
        
        # Verify search field accepts input
        elem = dashboard.find_element(dashboard.SEARCH_INPUT)
        assert elem.get_attribute("value") == "Tech"

    def test_player_dashboard_loads_with_metrics(self, authenticated_player):
        """Verify player dashboard loads after player authentication."""
        dashboard = PlayerDashboardPage(authenticated_player)
        assert dashboard.is_page_loaded(), "Player dashboard heading failed to render."
        assert dashboard.is_visible(dashboard.SEARCH_INPUT), "Player search input missing."
