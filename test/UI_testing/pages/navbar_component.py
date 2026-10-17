from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class NavbarComponent(BasePage):
    """Navbar component present on all application pages."""

    # Locators
    BRAND_LOGO = (By.XPATH, "//nav//a[contains(., 'Mini Leaderboard')]")
    LOGIN_LINK = (By.XPATH, "//nav//a[@href='/login' and contains(., 'Login')]")
    GET_STARTED_LINK = (By.XPATH, "//nav//a[@href='/register' and contains(., 'Get Started')]")
    
    # Authenticated links
    CREATOR_DASHBOARD_LINK = (By.XPATH, "//nav//a[@href='/creator/dashboard']")
    CREATOR_MY_EVENTS_LINK = (By.XPATH, "//nav//a[@href='/creator/events/create']")
    PLAYER_EVENTS_LINK = (By.XPATH, "//nav//a[@href='/player/dashboard']")
    ADMIN_DASHBOARD_LINK = (By.XPATH, "//nav//a[@href='/admin/dashboard']")
    
    # Profile dropdown
    PROFILE_DROPDOWN_BUTTON = (By.XPATH, "//nav//button[contains(@style, 'border-radius') and contains(@style, '50px')]")
    PROFILE_DROPDOWN_NAME = (By.XPATH, "//nav//div[contains(@style, 'min-width: 200px')]//div[contains(@style, 'font-weight: 600')]")
    PROFILE_DROPDOWN_EMAIL = (By.XPATH, "//nav//div[contains(@style, 'min-width: 200px')]//div[contains(@style, 'color: rgb(136, 136, 136)') or contains(@style, '#888')]")
    PROFILE_DROPDOWN_ROLE = (By.XPATH, "//nav//div[contains(@style, 'min-width: 200px')]//div[contains(@style, 'text-transform: uppercase')]")
    LOGOUT_BUTTON = (By.XPATH, "//nav//button[contains(., 'Logout')]")

    def click_brand_logo(self):
        self.click(self.BRAND_LOGO)

    def click_login(self):
        self.click(self.LOGIN_LINK)

    def click_get_started(self):
        self.click(self.GET_STARTED_LINK)

    def is_login_link_visible(self) -> bool:
        return self.is_visible(self.LOGIN_LINK)

    def is_profile_dropdown_visible(self) -> bool:
        return self.is_visible(self.PROFILE_DROPDOWN_BUTTON)

    def open_profile_dropdown(self):
        self.click(self.PROFILE_DROPDOWN_BUTTON)

    def get_profile_info(self) -> dict:
        self.open_profile_dropdown()
        name = self.get_text(self.PROFILE_DROPDOWN_NAME)
        email = self.get_text(self.PROFILE_DROPDOWN_EMAIL)
        role = self.get_text(self.PROFILE_DROPDOWN_ROLE)
        return {"name": name, "email": email, "role": role}

    def logout(self):
        self.open_profile_dropdown()
        logout_btn = self.find_element(self.LOGOUT_BUTTON)
        try:
            self.driver.execute_script("arguments[0].click();", logout_btn)
        except Exception:
            pass
