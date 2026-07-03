from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import logger
from utils.screenshot import ScreenshotUtil


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self, url):
        """Navigate to a URL"""
        try:
            self.driver.get(url)
            logger.info(f"Navigated to: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            raise

    def find_element(self, by, value, timeout=10):
        """Find a single element with wait"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {by}={value}")
            return None

    def find_elements(self, by, value, timeout=10):
        """Find multiple elements with wait"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {by}={value}")
            return []

    def click(self, by, value, timeout=10):
        """Click an element"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            logger.info(f"Clicked on: {by}={value}")
            return True
        except Exception as e:
            logger.error(f"Failed to click {by}={value}: {e}")
            self.take_screenshot("click_failed")
            return False

    def type_text(self, by, value, text, timeout=10):
        """Type text into an element"""
        try:
            element = self.find_element(by, value, timeout)
            if element:
                element.clear()
                element.send_keys(text)
                logger.info(f"Typed text into: {by}={value}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            self.take_screenshot("type_failed")
            return False

    def get_text(self, by, value, timeout=10):
        """Get text from an element"""
        try:
            element = self.find_element(by, value, timeout)
            if element:
                return element.text
            return ""
        except Exception as e:
            logger.error(f"Failed to get text: {e}")
            return ""

    def take_screenshot(self, name="screenshot"):
        """Take a screenshot of the current page"""
        return ScreenshotUtil.take_screenshot(self.driver, name)

    def is_element_present(self, by, value, timeout=5):
        """Check if an element is present"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def get_page_title(self):
        """Get the current page title"""
        return self.driver.title
