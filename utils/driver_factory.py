from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class to manage WebDriver instances"""

    @staticmethod
    def get_driver(headless=False):
        """
        Create and return a Chrome WebDriver instance

        Args:
            headless (bool): Run browser in headless mode

        Returns:
            WebDriver: Configured Chrome WebDriver
        """
        try:
            chrome_options = Options()

            # Basic options
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-gpu")

            # Headless mode
            if headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")

            # Experimental options to avoid detection
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)

            # Initialize driver - Selenium 4.6+ auto-manages driver
            driver = webdriver.Chrome(options=chrome_options)

            # Set page load timeout
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)

            logger.info("Chrome WebDriver initialized successfully")
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
