from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger
import time


class CheckoutPage(BasePage):
    """Checkout page object"""

    # Locators - Step 1: Information
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")

    # Locators - Step 2: Overview
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Locators - Step 3: Complete
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")
    ORDER_COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")

    def fill_checkout_info(self, first_name, last_name, postal_code):
        """
        Fill checkout information

        Args:
            first_name (str): First name
            last_name (str): Last name
            postal_code (str): Postal code

        Returns:
            bool: True if successful
        """
        try:
            self.type_text(*self.FIRST_NAME_INPUT, first_name)
            self.type_text(*self.LAST_NAME_INPUT, last_name)
            self.type_text(*self.POSTAL_CODE_INPUT, postal_code)
            logger.info("Checkout information filled")
            return True
        except Exception as e:
            logger.error(f"Failed to fill checkout info: {e}")
            self.take_screenshot("checkout_info_failed")
            return False

    def continue_checkout(self):
        """Click continue button"""
        try:
            time.sleep(1)
            return self.click(*self.CONTINUE_BUTTON, timeout=10)
        except Exception as e:
            logger.error(f"Failed to click continue: {e}")
            return False

    def get_subtotal(self):
        """Get subtotal amount"""
        try:
            text = self.get_text(*self.SUBTOTAL_LABEL, timeout=10)
            if text and "$" in text:
                try:
                    return float(text.split("$")[1])
                except (IndexError, ValueError):
                    return 0
            return 0
        except Exception as e:
            logger.error(f"Failed to get subtotal: {e}")
            return 0

    def get_total(self):
        """Get total amount"""
        try:
            text = self.get_text(*self.SUMMARY_TOTAL, timeout=10)
            if text and "$" in text:
                try:
                    return float(text.split("$")[1])
                except (IndexError, ValueError):
                    return 0
            return 0
        except Exception as e:
            logger.error(f"Failed to get total: {e}")
            return 0

    def finish_checkout(self):
        """Click finish button"""
        try:
            time.sleep(1)
            return self.click(*self.FINISH_BUTTON, timeout=10)
        except Exception as e:
            logger.error(f"Failed to click finish: {e}")
            return False

    def is_order_complete(self):
        """Check if order is complete"""
        try:
            time.sleep(2)
            return self.is_element_present(*self.COMPLETE_HEADER, timeout=10)
        except Exception as e:
            logger.error(f"Failed to check order complete: {e}")
            return False

    def get_order_confirmation(self):
        """Get order confirmation message"""
        try:
            time.sleep(1)
            return self.get_text(*self.COMPLETE_HEADER, timeout=10)
        except Exception as e:
            logger.error(f"Failed to get confirmation: {e}")
            return ""

    def go_back_home(self):
        """Click back to home button"""
        return self.click(*self.BACK_HOME_BUTTON)
