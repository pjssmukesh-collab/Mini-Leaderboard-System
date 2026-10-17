import pytest
from pages.navbar_component import NavbarComponent
from pages.login_page import LoginPage
from config import Config

@pytest.mark.ui
@pytest.mark.auth
class TestProfile:
    """Test suite for the user profile dropdown, user info display, and session management."""

    def test_profile_dropdown_displays_creator_details(self, authenticated_creator):
        """Verify profile dropdown correctly displays creator's name, email, and role."""
        navbar = NavbarComponent(authenticated_creator)
        assert navbar.is_profile_dropdown_visible(), "Profile avatar button not visible in navbar."
        
        info = navbar.get_profile_info()
        assert len(info["name"]) > 0, "User name is empty in profile dropdown."
        assert Config.TEST_CREATOR_EMAIL.lower() in info["email"].lower(), f"Unexpected email in profile: {info['email']}"
        assert "creator" in info["role"].lower(), f"Expected role 'creator', got: {info['role']}"

    def test_profile_dropdown_displays_player_details(self, authenticated_player):
        """Verify profile dropdown correctly displays player's role and details."""
        navbar = NavbarComponent(authenticated_player)
        assert navbar.is_profile_dropdown_visible(), "Profile avatar button not visible."
        
        info = navbar.get_profile_info()
        assert "player" in info["role"].lower(), f"Expected role 'player', got: {info['role']}"

    def test_profile_logout_action(self, authenticated_creator):
        """Verify clicking Logout in profile dropdown destroys session and redirects to /login."""
        navbar = NavbarComponent(authenticated_creator)
        navbar.logout()
        
        login_page = LoginPage(authenticated_creator)
        assert login_page.wait_for_url_contains("/login", timeout=5), "Logout did not redirect to /login."
