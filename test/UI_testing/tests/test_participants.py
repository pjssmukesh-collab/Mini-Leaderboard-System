import pytest
from pages.player_dashboard_page import PlayerDashboardPage
from pages.leaderboard_page import LeaderboardPage

@pytest.mark.ui
@pytest.mark.events
class TestParticipants:
    """Test suite for player tournament enrollment and participation flows."""

    def test_player_dashboard_lists_tournaments(self, authenticated_player):
        """Verify tournaments are listed on the player dashboard with join or leaderboard links."""
        dashboard = PlayerDashboardPage(authenticated_player)
        assert dashboard.is_page_loaded(), "Player dashboard not loaded."
        
        # Check that tournament cards or search are visible
        cards = dashboard.find_elements(dashboard.TOURNAMENT_CARDS)
        assert len(cards) > 0, "No tournament cards rendered on player dashboard."

    def test_player_join_tournament_action_and_modal(self, authenticated_player):
        """Verify clicking Join Tournament triggers the registration action and displays status modal."""
        dashboard = PlayerDashboardPage(authenticated_player)
        join_btn = dashboard.get_first_join_button()
        
        if join_btn:
            dashboard.join_first_available_tournament()
            # Verify status popup modal appears
            assert dashboard.is_status_popup_displayed(timeout=6), "Status modal did not appear after joining."
            popup_title = dashboard.get_status_popup_title()
            assert any(term in popup_title.lower() for term in ["registered", "joined", "full", "tournament"]), (
                f"Unexpected popup title: {popup_title}"
            )
            dashboard.close_status_popup()
        else:
            pytest.skip("All available tournaments are already joined by this test account.")

    def test_navigate_to_leaderboard_from_player_dashboard(self, authenticated_player):
        """Verify player can navigate to tournament leaderboard from dashboard."""
        dashboard = PlayerDashboardPage(authenticated_player)
        lb_links = dashboard.find_elements(dashboard.LEADERBOARD_LINKS)
        assert len(lb_links) > 0, "No leaderboard links found on player dashboard."
        
        dashboard.scroll_into_view(lb_links[0])
        lb_links[0].click()
        
        leaderboard_page = LeaderboardPage(authenticated_player)
        assert leaderboard_page.wait_for_url_contains("/player/leaderboard/", timeout=5), (
            "Clicking Leaderboard did not navigate to leaderboard URL."
        )
