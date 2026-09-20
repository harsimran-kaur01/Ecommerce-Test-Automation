import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class to manage WebDriver instances"""

    @staticmethod
    def get_driver(headless=None):
        """
        Create and return a Chrome WebDriver instance

        Args:
            headless (bool | None): Run browser in headless mode.
                If None (default), the HEADLESS environment variable decides
                (HEADLESS=1 / true / yes). This lets CI run headless without
                changing any test code.

        Returns:
            WebDriver: Configured Chrome WebDriver
        """
        if headless is None:
            headless = os.getenv("HEADLESS", "0").strip().lower() in (
                "1",
                "true",
                "yes",
            )

        try:
            chrome_options = Options()

            # Basic options
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--log-level=3")  # quieter Chrome console

            # Headless mode
            if headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

            # Experimental options to avoid detection / reduce console noise
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation", "enable-logging"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option(
                "prefs",
                {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "profile.password_manager_leak_detection": False,
                },
            )

            # Initialize driver - Selenium 4.6+ auto-manages driver
            driver = webdriver.Chrome(options=chrome_options)

            # Set page load timeout
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)

            logger.info(
                f"Chrome WebDriver initialized successfully (headless={headless})"
            )
            return driver

        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    @staticmethod
    def quit_driver(driver):
        """Safely quit WebDriver"""
        if driver:
            try:
                driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {e}")
