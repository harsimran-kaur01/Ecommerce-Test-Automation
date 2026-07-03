import json
import os
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)


class Helpers:
    """Helper functions for test automation"""

    @staticmethod
    def load_test_data(file_name):
        """
        Load test data from JSON file

        Args:
            file_name (str): JSON file name

        Returns:
            dict: Test data
        """
        file_path = os.path.join("testdata", file_name)
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Test data file not found: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return {}

    @staticmethod
    def wait_for_element(driver, by, value, timeout=10):
        """
        Wait for element to be present and visible

        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time

        Returns:
            WebElement: Found element or None
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {by}={value}")
            return None

    @staticmethod
    def wait_for_element_clickable(driver, by, value, timeout=10):
        """Wait for element to be clickable"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not clickable: {by}={value}")
            return None

    @staticmethod
    def safe_click(driver, by, value):
        """Safely click an element with retry"""
        try:
            element = Helpers.wait_for_element_clickable(driver, by, value)
            if element:
                element.click()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to click {by}={value}: {e}")
            return False

    @staticmethod
    def safe_send_keys(driver, by, value, text):
        """Safely send keys to an element"""
        try:
            element = Helpers.wait_for_element(driver, by, value)
            if element:
                element.clear()
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to send keys to {by}={value}: {e}")
            return False

    @staticmethod
    def get_text(driver, by, value):
        """Get text from an element safely"""
        try:
            element = Helpers.wait_for_element(driver, by, value)
            if element:
                return element.text
            return ""
        except Exception as e:
            logger.error(f"Failed to get text from {by}={value}: {e}")
            return ""
