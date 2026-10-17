import pytest
from pages.home_page import HomePage
from config import Config

@pytest.mark.ui
@pytest.mark.smoke
class TestApplication:
    """Verifies basic application launch, title, brand elements, and responsive layout."""

    def test_application_launches_successfully(self, driver):
        """Verify that the application opens successfully and title matches."""
        home_page = HomePage(driver)
        home_page.open_home()
        
        # Verify page title
        assert "Mini Leaderboard" in home_page.get_title(), f"Unexpected title: {home_page.get_title()}"
        
        # Verify hero heading
        assert home_page.is_hero_heading_displayed(), "Hero heading is not visible on landing page."
        assert "leaderboard" in home_page.get_hero_heading_text().lower()

    def test_application_footer_displayed(self, driver):
        """Verify that the footer renders properly on the home page."""
        home_page = HomePage(driver)
        home_page.open_home()
        assert home_page.is_footer_displayed(), "Footer is not displayed."

    def test_application_responsive_mobile_viewport(self, mobile_driver):
        """Verify that application layout remains usable and does not break at mobile viewport (375x812)."""
        home_page = HomePage(mobile_driver)
        home_page.open_home()
        
        # Heading should still be visible and page should be accessible
        assert home_page.is_hero_heading_displayed(), "Hero heading not visible on mobile viewport."
        assert "Mini Leaderboard" in home_page.get_title()
