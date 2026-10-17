from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    """Home / Landing Page Object."""

    # Locators
    HERO_HEADING = (By.XPATH, "//h1[contains(., 'Turn every result into a')]")
    HERO_GET_STARTED_BUTTON = (By.XPATH, "//section//a[contains(., 'Get Started Free')]")
    DASHBOARD_PREVIEW_CARD = (By.CLASS_NAME, "dashboard-preview-card")
    BENEFITS_SECTION = (By.CLASS_NAME, "benefits-section")
    EVENT_TYPES_SECTION = (By.CLASS_NAME, "event-types-section")
    FOOTER = (By.TAG_NAME, "footer")

    def open_home(self):
        return self.open("/")

    def get_hero_heading_text(self) -> str:
        return self.get_text(self.HERO_HEADING)

    def is_hero_heading_displayed(self) -> bool:
        return self.is_visible(self.HERO_HEADING)

    def click_get_started(self):
        self.click(self.HERO_GET_STARTED_BUTTON)

    def is_footer_displayed(self) -> bool:
        return self.is_visible(self.FOOTER)
