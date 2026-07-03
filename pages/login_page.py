from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import logger


class LoginPage(BasePage):
    """Login page object"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"
    
    def open(self):
        """Open the login page"""
        self.navigate_to(self.url)
        return self
    
    def login(self, username, password):
        """
        Perform login action
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: True if login successful
        """
        try:
            logger.info(f"Attempting login with username: {username}")
            
            # Type username
            self.type_text(*self.USERNAME_INPUT, username)
            
            # Type password
            self.type_text(*self.PASSWORD_INPUT, password)
            
            # Click login button
            success = self.click(*self.LOGIN_BUTTON)
            
            if success:
                logger.info("Login button clicked")
            
            return success
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            self.take_screenshot("login_failed")
            return False
    
    def get_error_message(self):
        """Get the error message text"""
        return self.get_text(*self.ERROR_MESSAGE)
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_present(*self.ERROR_MESSAGE)
    
    def is_login_successful(self):
        """Check if login was successful"""
        # Success indicator - dashboard/logo appears
        return self.is_element_present(*self.APP_LOGO, timeout=5)
    
    def clear_credentials(self):
        """Clear username and password fields"""
        self.find_element(*self.USERNAME_INPUT).clear()
        self.find_element(*self.PASSWORD_INPUT).clear()