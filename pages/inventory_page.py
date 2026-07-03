from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class InventoryPage(BasePage):
    """Inventory/Products page object"""

    # Locators
    PRODUCT_LIST = (By.CLASS_NAME, "inventory_list")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    def add_item_to_cart(self, item_name):
        """
        Add a specific item to cart

        Args:
            item_name (str): Name of the item to add

        Returns:
            bool: True if successful
        """
        try:
            # Find the item and its add to cart button
            items = self.find_elements(*self.PRODUCT_ITEMS)

            for item in items:
                name_element = item.find_element(*self.PRODUCT_NAME)
                if name_element.text == item_name:
                    add_button = item.find_element(*self.ADD_TO_CART_BUTTON)
                    add_button.click()
                    logger.info(f"Added '{item_name}' to cart")
                    return True

            logger.warning(f"Item '{item_name}' not found")
            return False

        except Exception as e:
            logger.error(f"Failed to add item to cart: {e}")
            self.take_screenshot("add_to_cart_failed")
            return False

    def get_cart_count(self):
        """Get number of items in cart"""
        try:
            badge = self.find_element(*self.CART_BADGE, timeout=3)
            if badge:
                return int(badge.text)
            return 0
        except (NoSuchElementException, TimeoutException, ValueError):
            return 0

    def go_to_cart(self):
        """Navigate to cart page"""
        return self.click(*self.CART_ICON)

    def get_product_names(self):
        """Get list of all product names"""
        products = []
        items = self.find_elements(*self.PRODUCT_ITEMS)
        for item in items:
            name_element = item.find_element(*self.PRODUCT_NAME)
            products.append(name_element.text)
        return products

    def search_product(self, search_term):
        """Search for a product (SauceDemo doesn't have search, but we'll filter)"""
        products = self.find_elements(*self.PRODUCT_ITEMS)
        found_products = []

        for product in products:
            name = product.find_element(*self.PRODUCT_NAME).text
            if search_term.lower() in name.lower():
                found_products.append(name)

        return found_products
