from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class CartPage(BasePage):
    """Shopping Cart page object"""

    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test^='remove']")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")  # Added this

    def get_cart_items(self):
        """Get all items in cart"""
        return self.find_elements(*self.CART_ITEMS)

    def get_item_names(self):
        """Get names of all items in cart"""
        items = self.get_cart_items()
        names = []
        for item in items:
            name_element = item.find_element(*self.ITEM_NAME)
            names.append(name_element.text)
        return names

    def remove_item(self, item_name):
        """Remove an item from cart"""
        try:
            items = self.get_cart_items()
            for item in items:
                name_element = item.find_element(*self.ITEM_NAME)
                if name_element.text == item_name:
                    remove_button = item.find_element(*self.REMOVE_BUTTON)
                    remove_button.click()
                    logger.info(f"Removed '{item_name}' from cart")
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove item: {e}")
            return False

    def proceed_to_checkout(self):
        """Click checkout button"""
        return self.click(*self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        """Continue shopping button"""
        return self.click(*self.CONTINUE_SHOPPING)

    def is_cart_empty(self):
        """Check if cart is empty"""
        items = self.get_cart_items()
        return len(items) == 0

    def get_cart_count(self):
        """Get number of items in cart"""
        try:
            badge = self.find_element(*self.CART_BADGE, timeout=3)
            if badge:
                return int(badge.text)
            return 0
        except (NoSuchElementException, TimeoutException, ValueError):
            return 0
