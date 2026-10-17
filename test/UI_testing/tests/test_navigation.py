import pytest
from pages.home_page import HomePage
from pages.navbar_component import NavbarComponent
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

@pytest.mark.ui
@pytest.mark.navigation
class TestNavigation:
    """Verifies that navigation links and buttons lead to expected destinations."""

    def test_navigate_to_login_via_navbar(self, driver):
        """Verify clicking 'Login' in the navbar opens the login page."""
        home_page = HomePage(driver)
        home_page.open_home()
        
        navbar = NavbarComponent(driver)
        navbar.click_login()
        
        login_page = LoginPage(driver)
        assert login_page.wait_for_url_contains("/login"), "Did not navigate to /login."
        assert login_page.is_page_loaded(), "Login page failed to render properly."

    def test_navigate_to_register_via_navbar(self, driver):
        """Verify clicking 'Get Started' in the navbar opens the register page."""
        home_page = HomePage(driver)
        home_page.open_home()
        
        navbar = NavbarComponent(driver)
        navbar.click_get_started()
        
        register_page = RegisterPage(driver)
        assert register_page.wait_for_url_contains("/register"), "Did not navigate to /register."
        assert register_page.is_page_loaded(), "Register page failed to render properly."

    def test_navigate_to_register_via_hero_cta(self, driver):
        """Verify clicking 'Get Started Free' hero button navigates to register."""
        home_page = HomePage(driver)
        home_page.open_home()
        home_page.click_get_started()
        
        register_page = RegisterPage(driver)
        assert register_page.wait_for_url_contains("/register"), "Hero CTA did not navigate to /register."

    def test_brand_logo_navigates_to_home(self, driver):
        """Verify clicking brand logo in navbar from any page returns to home."""
        login_page = LoginPage(driver)
        login_page.open_login()
        
        navbar = NavbarComponent(driver)
        navbar.click_brand_logo()
        
        home_page = HomePage(driver)
        assert home_page.is_hero_heading_displayed(), "Clicking logo did not return to home page."
