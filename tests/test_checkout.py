import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import logger
from selenium.webdriver.common.by import By
import time


class TestCheckout:
    """Test suite for checkout functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, driver, test_data):
        """Setup for checkout tests - login and add item first"""
        self.driver = driver

        # Get valid user and checkout data
        valid_users = test_data.get("valid_users", [])
        if valid_users:
            self.user = valid_users[0]

        self.checkout_info = test_data.get("products", {}).get("checkout_info", {})

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(self.user["username"], self.user["password"])

        # Initialize pages
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)

        # Add a product to cart
        product_names = self.inventory_page.get_product_names()
        if product_names:
            self.inventory_page.add_item_to_cart(product_names[0])
            logger.info(f"Added {product_names[0]} to cart for checkout test")

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_complete_checkout(self):
        """
        Test complete checkout process
        """
        logger.info("Starting test_complete_checkout")

        # Go to cart
        self.inventory_page.go_to_cart()
        time.sleep(1)

        # Proceed to checkout
        success = self.cart_page.proceed_to_checkout()
        assert success, "Failed to proceed to checkout"
        time.sleep(1)

        # Fill checkout information
        self.checkout_page.fill_checkout_info(
            self.checkout_info.get("first_name", "John"),
            self.checkout_info.get("last_name", "Doe"),
            self.checkout_info.get("postal_code", "12345"),
        )
        time.sleep(1)

        # Continue to overview
        self.checkout_page.continue_checkout()
        time.sleep(1)

        # Get total before finishing
        total = self.checkout_page.get_total()
        assert total > 0, f"Total should be greater than 0, got {total}"

        # Finish checkout
        self.checkout_page.finish_checkout()
        time.sleep(2)

        # Verify order complete
        assert self.checkout_page.is_order_complete(), "Order not complete"

        # Get confirmation message
        confirmation = self.checkout_page.get_order_confirmation()
        assert (
            "Thank you for your order" in confirmation or "Thank you" in confirmation
        ), f"Expected thank you message, got {confirmation}"

        logger.info("Complete checkout test passed")

    @pytest.mark.regression
    def test_checkout_without_items(self, driver, test_data):
        """
        Test checkout with empty cart
        """
        logger.info("Starting test_checkout_without_items")

        # Get valid user
        valid_users = test_data.get("valid_users", [])
        if valid_users:
            user = valid_users[0]

        # Login fresh (without adding items)
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(user["username"], user["password"])
        time.sleep(1)

        # Go to cart
        inventory_page = InventoryPage(driver)
        inventory_page.go_to_cart()
        time.sleep(1)

        # The class-level setup already put an item in the cart,
        # so empty the cart first to make this a real "empty cart" test.
        driver.implicitly_wait(0)  # don't wait 10s when no Remove buttons are left
        try:
            while True:
                remove_buttons = driver.find_elements(
                    By.CSS_SELECTOR, "button[data-test^='remove']"
                )
                if not remove_buttons:
                    break
                remove_buttons[0].click()
                time.sleep(0.5)
        finally:
            driver.implicitly_wait(10)

        # Try to checkout
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        time.sleep(1)

        # Fill checkout info
        checkout_info = test_data.get("products", {}).get("checkout_info", {})
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_checkout_info(
            checkout_info.get("first_name", "John"),
            checkout_info.get("last_name", "Doe"),
            checkout_info.get("postal_code", "12345"),
        )
        time.sleep(1)

        # Continue
        checkout_page.continue_checkout()
        time.sleep(1)

        # Verify total is 0 (no items)
        total = checkout_page.get_total()
        assert total == 0, f"Expected total 0, got {total}"

        logger.info("Empty cart checkout test passed")

    @pytest.mark.regression
    def test_checkout_with_missing_info(self):
        """
        Test checkout with missing required information
        """
        logger.info("Starting test_checkout_with_missing_info")

        # Go to cart
        self.inventory_page.go_to_cart()
        time.sleep(1)

        # Proceed to checkout
        self.cart_page.proceed_to_checkout()
        time.sleep(1)

        # Click continue without filling info
        self.checkout_page.continue_checkout()
        time.sleep(1)

        # Verify error appears - SauceDemo shows red border on first name field
        # Check if the first name input has error class
        try:
            error_element = self.driver.find_element(
                By.CSS_SELECTOR, "[data-test='firstName'][class*='error']"
            )
            assert error_element is not None, (
                "Error indicator not shown for missing first name"
            )
            logger.info("Missing info checkout test passed - error displayed")
        except:
            # Alternative: check for any error message
            error_message = self.driver.find_element(
                By.CSS_SELECTOR, "[data-test='error']"
            )
            assert error_message is not None, "No error message displayed"
            logger.info("Missing info checkout test passed - error message found")
