import sys
from pathlib import Path

# Add test/ui_testing to sys.path to allow clean relative imports
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import pytest
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import Config
from pages.login_page import LoginPage
from pages.navbar_component import NavbarComponent

@pytest.fixture(scope="session", autouse=True)
def verify_services_running():
    """Verifies that frontend and backend services are reachable before starting UI tests."""
    # Check Backend
    try:
        with urllib.request.urlopen(f"{Config.BACKEND_BASE_URL}/health", timeout=3) as resp:
            if resp.status != 200:
                pytest.fail(f"Backend at {Config.BACKEND_BASE_URL} returned status {resp.status}, expected 200.")
    except Exception as e:
        pytest.fail(
            f"Backend service is unavailable at {Config.BACKEND_BASE_URL}. "
            f"Please start FastAPI backend before running UI tests. Error: {e}"
        )

    # Check Frontend
    try:
        with urllib.request.urlopen(f"{Config.APP_BASE_URL}/", timeout=3) as resp:
            if resp.status != 200:
                pytest.fail(f"Frontend at {Config.APP_BASE_URL} returned status {resp.status}, expected 200.")
    except Exception as e:
        pytest.fail(
            f"Frontend service is unavailable at {Config.APP_BASE_URL}. "
            f"Please start React/Vite frontend before running UI tests. Error: {e}"
        )

@pytest.fixture
def chrome_options():
    """Configures Chrome options for test execution."""
    options = Options()
    if Config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--disable-extensions")
    return options

@pytest.fixture
def driver(chrome_options):
    """Initializes a clean Chrome WebDriver instance for each test."""
    driver_instance = webdriver.Chrome(options=chrome_options)
    driver_instance.implicitly_wait(0)  # Use explicit waits throughout
    driver_instance.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    
    yield driver_instance
    driver_instance.quit()

@pytest.fixture
def mobile_driver(chrome_options):
    """Provides a mobile-viewport (375x812, iPhone size) browser instance."""
    driver_instance = webdriver.Chrome(options=chrome_options)
    driver_instance.set_window_size(375, 812)
    yield driver_instance
    driver_instance.quit()

@pytest.fixture
def authenticated_creator(driver):
    """Logs in as a tournament creator and returns the authenticated driver."""
    login_page = LoginPage(driver)
    login_page.open_login()
    login_page.login(Config.TEST_CREATOR_EMAIL, Config.TEST_CREATOR_PASSWORD)
    login_page.wait_for_url_contains("/creator/dashboard")
    return driver

@pytest.fixture
def authenticated_player(driver):
    """Logs in as a player and returns the authenticated driver."""
    login_page = LoginPage(driver)
    login_page.open_login()
    login_page.login(Config.TEST_PLAYER_EMAIL, Config.TEST_PLAYER_PASSWORD)
    login_page.wait_for_url_contains("/player/dashboard")
    return driver
