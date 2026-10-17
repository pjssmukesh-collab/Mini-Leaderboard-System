from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import time
from config import Config

class BasePage:
    """Base Page Object containing reusable methods for all page interactions."""

    def __init__(self, driver: WebDriver, timeout: int = None):
        self.driver = driver
        self.timeout = timeout or Config.EXPLICIT_WAIT_TIMEOUT
        self.wait = WebDriverWait(self.driver, self.timeout, ignored_exceptions=[StaleElementReferenceException])

    def open(self, path: str = "/"):
        """Navigates to a specific path relative to APP_BASE_URL."""
        url = f"{Config.APP_BASE_URL}{path}"
        self.driver.get(url)
        return self

    def get_title(self) -> str:
        """Returns the page title."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Returns the current URL."""
        return self.driver.current_url

    def wait_for_url_contains(self, partial_url: str, timeout: int = None) -> bool:
        """Waits until the current URL contains the given substring."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.url_contains(partial_url))
        except TimeoutException:
            return False

    def find_element(self, locator: tuple, timeout: int = None):
        """Finds a single element with explicit wait for visibility."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator: tuple, timeout: int = None):
        """Finds all visible elements matching the locator."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []

    def click(self, locator: tuple, timeout: int = None):
        """Waits for element to be clickable and clicks it with JS fallback if intercepted."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        self.scroll_into_view(element)
        try:
            wait.until(EC.element_to_be_clickable(locator)).click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
            if element.get_attribute("type") == "submit":
                try:
                    self.driver.execute_script(
                        "var f = arguments[0].closest('form'); if (f) f.requestSubmit(arguments[0]);",
                        element
                    )
                except Exception:
                    pass

    def type_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = None):
        """Types text into an input element after ensuring visibility with React fallback."""
        element = self.find_element(locator, timeout)
        self.scroll_into_view(element)
        if clear_first:
            element.clear()
        element.send_keys(text)
        if element.get_attribute("value") != text:
            self.driver.execute_script("""
                let el = arguments[0];
                let val = arguments[1];
                let lastVal = el.value;
                el.value = val;
                let tracker = el._valueTracker;
                if (tracker) {
                    tracker.setValue(lastVal);
                }
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            """, element, text)

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """Retrieves visible text from an element."""
        element = self.find_element(locator, timeout)
        return element.text.strip()

    def is_visible(self, locator: tuple, timeout: int = None) -> bool:
        """Checks if an element is visible on the page within the given timeout."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_invisibility(self, locator: tuple, timeout: int = None) -> bool:
        """Waits for an element to disappear."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        try:
            return wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False

    def scroll_into_view(self, element):
        """Scrolls element into center of viewport."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)

    def set_viewport_size(self, width: int, height: int):
        """Resizes the browser window for responsive layout testing."""
        self.driver.set_window_size(width, height)
