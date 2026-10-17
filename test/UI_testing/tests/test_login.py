import pytest
from pages.login_page import LoginPage
from pages.navbar_component import NavbarComponent
from config import Config

@pytest.mark.ui
@pytest.mark.auth
class TestLogin:
    """Comprehensive test suite for the Login UI and authentication workflows."""

    def test_login_page_loads_correctly(self, driver):
        """Verify that the login page elements render correctly."""
        login_page = LoginPage(driver)
        login_page.open_login()
        
        assert login_page.is_page_loaded(), "Login page heading or email input is not visible."
        assert login_page.is_visible(login_page.PASSWORD_INPUT), "Password input is missing."
        assert login_page.is_visible(login_page.SUBMIT_BUTTON), "Submit button is missing."

    def test_empty_email_and_password_validation(self, driver):
        """Verify client-side validation prevents submission when fields are empty."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.click_submit()
        
        # HTML5 required validation should be triggered on email
        validation_msg = login_page.get_email_validation_message()
        assert len(validation_msg) > 0, "Expected HTML5 validation message on empty email input."
        assert not login_page.is_error_displayed(timeout=1), "Server error should not appear on empty form."

    def test_empty_password_validation(self, driver):
        """Verify validation prevents submission when password is empty."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.enter_email("valid.user@example.com")
        login_page.click_submit()
        
        validation_msg = login_page.get_password_validation_message()
        assert len(validation_msg) > 0, "Expected HTML5 validation message on empty password input."

    def test_invalid_email_format_validation(self, driver):
        """Verify validation when an invalid email format is entered."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.enter_email("invalid-email-no-at-sign")
        login_page.enter_password("Secret123!")
        login_page.click_submit()
        
        validation_msg = login_page.get_email_validation_message()
        assert len(validation_msg) > 0, "Expected HTML5 validation message for malformed email."

    def test_incorrect_password_shows_error(self, driver):
        """Verify error message appears when entering wrong password for registered account."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.login(Config.TEST_CREATOR_EMAIL, "WrongPassword999!")
        
        assert login_page.is_error_displayed(timeout=5), "Error alert did not appear on incorrect password."
        error_msg = login_page.get_error_message()
        assert "invalid" in error_msg.lower() or "failed" in error_msg.lower() or "unauthorized" in error_msg.lower()

    def test_unregistered_user_shows_error(self, driver):
        """Verify error message appears when logging in with an unregistered email."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.login("nonexistent_user_9999@example.com", "Password123!")
        
        assert login_page.is_error_displayed(timeout=5), "Error alert did not appear for unregistered user."

    def test_valid_creator_login_navigates_to_dashboard(self, driver):
        """Verify valid creator login successfully redirects to creator dashboard."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.login(Config.TEST_CREATOR_EMAIL, Config.TEST_CREATOR_PASSWORD)
        
        assert login_page.wait_for_url_contains("/creator/dashboard", timeout=8), (
            f"Expected redirection to /creator/dashboard, but current URL is {login_page.get_current_url()}"
        )
        
        navbar = NavbarComponent(driver)
        assert navbar.is_profile_dropdown_visible(), "Profile dropdown should be visible after login."

    def test_valid_player_login_navigates_to_dashboard(self, driver):
        """Verify valid player login successfully redirects to player dashboard."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.login(Config.TEST_PLAYER_EMAIL, Config.TEST_PLAYER_PASSWORD)
        
        assert login_page.wait_for_url_contains("/player/dashboard", timeout=8), (
            f"Expected redirection to /player/dashboard, but current URL is {login_page.get_current_url()}"
        )

    def test_auth_state_maintained_and_logout_works(self, driver):
        """Verify authentication persists across navigation and logout clears the session."""
        login_page = LoginPage(driver)
        login_page.open_login()
        login_page.login(Config.TEST_CREATOR_EMAIL, Config.TEST_CREATOR_PASSWORD)
        login_page.wait_for_url_contains("/creator/dashboard")
        
        navbar = NavbarComponent(driver)
        # Navigate to another page (Home)
        navbar.click_brand_logo()
        assert navbar.is_profile_dropdown_visible(), "Auth session lost after navigating to home."
        
        # Perform Logout
        navbar.logout()
        assert login_page.wait_for_url_contains("/login", timeout=5), "Logout did not redirect to /login."
        assert navbar.is_login_link_visible(), "Login link should appear in navbar after logout."

    def test_unauthenticated_protected_route_redirects_to_login(self, driver):
        """Verify unauthenticated access to protected creator dashboard redirects to /login."""
        login_page = LoginPage(driver)
        # Attempt to access protected dashboard directly
        login_page.open("/creator/dashboard")
        
        assert login_page.wait_for_url_contains("/login", timeout=5), (
            f"Protected route allowed access without auth! Current URL: {login_page.get_current_url()}"
        )
