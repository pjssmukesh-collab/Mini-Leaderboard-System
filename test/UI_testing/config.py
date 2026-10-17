import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    """Central configuration for Selenium UI automation test suite."""
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5173").rstrip("/")
    BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
    
    # Dedicated test credentials
    TEST_CREATOR_EMAIL = os.getenv("TEST_CREATOR_EMAIL", "anu@gmail.com")
    TEST_CREATOR_PASSWORD = os.getenv("TEST_CREATOR_PASSWORD", "111111")
    
    TEST_PLAYER_EMAIL = os.getenv("TEST_PLAYER_EMAIL", "test_player@example.com")
    TEST_PLAYER_PASSWORD = os.getenv("TEST_PLAYER_PASSWORD", "Password123!")
    
    # Browser configuration
    HEADLESS = os.getenv("HEADLESS", "true").lower() in ("true", "1", "yes")
    EXPLICIT_WAIT_TIMEOUT = int(os.getenv("EXPLICIT_WAIT_TIMEOUT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "20"))
    
    # Paths
    FIXTURES_DIR = BASE_DIR / "fixtures"

# Ensure directories exist
Config.FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
