import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.logger import logger


class TestCart:
    """Test suite for cart functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, driver, test_data):
        """Setup for cart tests - login first"""
        self.driver = driver

        # Get valid user
        valid_users = test_data.get("valid_users", [])
        if valid_users:
            self.user = valid_users[0]

        # Login
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(self.user["username"], self.user["password"])

        # Initialize pages
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_add_item_to_cart(self):
        """
        Test adding a single item to cart
        """
        logger.info("Starting test_add_item_to_cart")

        # Get first product name
        product_names = self.inventory_page.get_product_names()
        assert len(product_names) > 0, "No products found"

        product_name = product_names[0]
        initial_count = self.inventory_page.get_cart_count()

        # Add product to cart
        success = self.inventory_page.add_item_to_cart(product_name)
        assert success, "Failed to add item to cart"

        # Verify cart count increased
        new_count = self.inventory_page.get_cart_count()
        assert new_count == initial_count + 1, (
            f"Expected {initial_count + 1}, got {new_count}"
        )

        logger.info("Add item to cart test passed")

    @pytest.mark.smoke
    def test_add_multiple_items_to_cart(self):
        """
        Test adding multiple items to cart
        """
        logger.info("Starting test_add_multiple_items_to_cart")

        # Get product names
        product_names = self.inventory_page.get_product_names()
        assert len(product_names) >= 2, "Need at least 2 products"

        # Add first two items
        for product_name in product_names[:2]:
            self.inventory_page.add_item_to_cart(product_name)

        # Verify cart count
        cart_count = self.inventory_page.get_cart_count()
        assert cart_count == 2, f"Expected 2 items, got {cart_count}"

        # Go to cart and verify items
        self.inventory_page.go_to_cart()
        item_names = self.cart_page.get_item_names()
        assert len(item_names) == 2, "Cart doesn't have 2 items"

        # Check items are correct
        for product in product_names[:2]:
            assert product in item_names, f"{product} not in cart"

        logger.info("Add multiple items test passed")

    @pytest.mark.regression
    def test_remove_item_from_cart(self):
        """
        Test removing item from cart
        """
        logger.info("Starting test_remove_item_from_cart")

        # Add product to cart
        product_names = self.inventory_page.get_product_names()
        product_name = product_names[0]
        self.inventory_page.add_item_to_cart(product_name)

        # Go to cart
        self.inventory_page.go_to_cart()

        # Verify item is in cart
        assert product_name in self.cart_page.get_item_names(), (
            f"{product_name} not in cart"
        )

        # Remove item
        self.cart_page.remove_item(product_name)

        # Verify cart is empty
        assert self.cart_page.is_cart_empty(), "Cart not empty after removal"

        logger.info("Remove item test passed")

    @pytest.mark.regression
    def test_cart_persistence(self):
        """
        Test cart items persist when navigating away and back
        """
        logger.info("Starting test_cart_persistence")

        # Add product to cart
        product_names = self.inventory_page.get_product_names()
        product_name = product_names[0]
        self.inventory_page.add_item_to_cart(product_name)

        # Go to cart
        self.inventory_page.go_to_cart()

        # Get initial cart items
        initial_items = self.cart_page.get_item_names()

        # Continue shopping
        self.cart_page.continue_shopping()

        # Wait for inventory page
        assert self.inventory_page.is_element_present(
            *self.inventory_page.PRODUCT_LIST
        ), "Did not return to inventory page"

        # Go back to cart
        self.inventory_page.go_to_cart()

        # Verify items still there
        current_items = self.cart_page.get_item_names()
        assert current_items == initial_items, "Cart items changed"

        logger.info("Cart persistence test passed")
