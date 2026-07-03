import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger import logger
import time


class TestLogin:
    """Test suite for login functionality"""
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_valid_login(self, driver, test_data):
        """
        Test valid login with valid credentials
        """
        logger.info("Starting test_valid_login")
        
        # Get valid user from test data
        valid_users = test_data.get('valid_users', [])
        if not valid_users:
            pytest.skip("No valid user data found")
        
        user = valid_users[0]
        
        # Initialize pages
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        
        # Open login page
        login_page.open()
        
        # Perform login
        login_page.login(user['username'], user['password'])
        
        # Verify login successful
        assert login_page.is_login_successful(), "Login failed"
        
        # Verify inventory page loaded
        assert inventory_page.is_element_present(*inventory_page.PRODUCT_LIST), \
            "Products not displayed"
        
        logger.info("Valid login test passed")
    
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_invalid_login(self, driver, test_data):
        """
        Test login with invalid credentials
        """
        logger.info("Starting test_invalid_login")
        
        # Get invalid user from test data
        invalid_users = test_data.get('invalid_users', [])
        if not invalid_users:
            pytest.skip("No invalid user data found")
        
        user = invalid_users[0]
        
        # Initialize pages
        login_page = LoginPage(driver)
        
        # Open login page
        login_page.open()
        
        # Perform login with invalid credentials
        login_page.login(user['username'], user['password'])
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        
        error_message = login_page.get_error_message()
        assert user['error_message'] in error_message, \
            f"Expected '{user['error_message']}', got '{error_message}'"
        
        logger.info("Invalid login test passed")
    
    @pytest.mark.smoke
    def test_locked_out_user(self, driver, test_data):
        """
        Test locked out user
        """
        logger.info("Starting test_locked_out_user")
        
        # Get locked out user from test data
        invalid_users = test_data.get('invalid_users', [])
        locked_user = next(
            (user for user in invalid_users if 'locked_out' in user['username']),
            None
        )
        
        if not locked_user:
            pytest.skip("No locked out user data found")
        
        # Initialize pages
        login_page = LoginPage(driver)
        
        # Open login page
        login_page.open()
        
        # Attempt login
        login_page.login(locked_user['username'], locked_user['password'])
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert locked_user['error_message'] in error_message
        
        logger.info("Locked out user test passed")
    
    @pytest.mark.regression
    def test_login_with_empty_credentials(self, driver):
        """
        Test login with empty credentials
        """
        logger.info("Starting test_login_with_empty_credentials")
        
        # Initialize pages
        login_page = LoginPage(driver)
        
        # Open login page
        login_page.open()
        
        # Click login without entering credentials
        login_page.click(*login_page.LOGIN_BUTTON)
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert "Username is required" in error_message
        
        logger.info("Empty credentials test passed")
    
    @pytest.mark.regression
    def test_login_with_only_username(self, driver):
        """
        Test login with only username provided
        """
        logger.info("Starting test_login_with_only_username")
        
        # Initialize pages
        login_page = LoginPage(driver)
        
        # Open login page
        login_page.open()
        
        # Enter only username
        login_page.type_text(*login_page.USERNAME_INPUT, "standard_user")
        login_page.click(*login_page.LOGIN_BUTTON)
        
        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_message = login_page.get_error_message()
        assert "Password is required" in error_message
        
        logger.info("Only username test passed")