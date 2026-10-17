import pytest
import time
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from config import Config

@pytest.mark.ui
@pytest.mark.auth
class TestRegistration:
    """Test suite for registration UI, form validation, and unique user creation."""

    def test_registration_page_loads_correctly(self, driver):
        """Verify that the register page renders all necessary input fields."""
        register_page = RegisterPage(driver)
        register_page.open_register()
        
        assert register_page.is_page_loaded(), "Registration page failed to load."
        assert register_page.is_visible(register_page.NAME_INPUT), "Name input missing."
        assert register_page.is_visible(register_page.EMAIL_INPUT), "Email input missing."
        assert register_page.is_visible(register_page.ROLE_SELECT), "Role select missing."
        assert register_page.is_visible(register_page.PASSWORD_INPUT), "Password input missing."
        assert register_page.is_visible(register_page.SUBMIT_BUTTON), "Submit button missing."

    def test_required_fields_validation(self, driver):
        """Verify HTML5 validation triggers when submitting empty registration form."""
        register_page = RegisterPage(driver)
        register_page.open_register()
        register_page.click_submit()
        
        name_val = register_page.get_name_validation_message()
        assert len(name_val) > 0, "Expected required validation on Full Name input."

    def test_password_min_length_validation(self, driver):
        """Verify password input requires minimum 6 characters."""
        register_page = RegisterPage(driver)
        register_page.open_register()
        register_page.enter_name("Short Pass")
        register_page.enter_email(f"test_{int(time.time())}@example.com")
        register_page.enter_password("123")  # Less than minLength 6
        register_page.click_submit()
        
        pwd_val = register_page.get_password_validation_message()
        assert len(pwd_val) > 0, "Expected minLength validation on password input."

    def test_invalid_email_format_validation(self, driver):
        """Verify invalid email format is rejected by client validation."""
        register_page = RegisterPage(driver)
        register_page.open_register()
        register_page.enter_name("Jane Doe")
        register_page.enter_email("jane.doe.without.at.domain")
        register_page.enter_password("Password123!")
        register_page.click_submit()
        
        email_val = register_page.get_email_validation_message()
        assert len(email_val) > 0, "Expected email format validation message."

    def test_duplicate_email_registration_shows_error(self, driver):
        """Verify attempting to register an already existing email shows a server error alert."""
        register_page = RegisterPage(driver)
        register_page.open_register()
        # Use existing creator account
        register_page.register(
            name="Duplicate Test",
            email=Config.TEST_CREATOR_EMAIL,
            password="Password123!",
            role="player"
        )
        
        assert register_page.is_error_displayed(timeout=5), "Error alert did not appear for duplicate email."
        error_msg = register_page.get_error_message().lower()
        assert "already" in error_msg or "exists" in error_msg or "registered" in error_msg

    def test_successful_registration_with_unique_data(self, driver):
        """Verify registering with fresh unique data succeeds and redirects to /login."""
        register_page = RegisterPage(driver)
        register_page.open_register()
        
        unique_email = f"auto_user_{int(time.time())}@example.com"
        register_page.register(
            name="Automated User",
            email=unique_email,
            password="StrongPassword123!",
            role="player"
        )
        
        # Upon success, Register.jsx navigates to /login
        login_page = LoginPage(driver)
        assert login_page.wait_for_url_contains("/login", timeout=8), (
            f"Registration did not redirect to /login. Current URL: {login_page.get_current_url()}"
        )
