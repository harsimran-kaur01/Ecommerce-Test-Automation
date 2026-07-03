import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ScreenshotUtil:
    """Utility class for taking screenshots"""

    @staticmethod
    def take_screenshot(driver, name="screenshot"):
        """
        Take a screenshot and save it

        Args:
            driver: WebDriver instance
            name (str): Screenshot name

        Returns:
            str: Path to saved screenshot
        """
        try:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)

            # Generate timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Create filename
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(screenshots_dir, filename)

            # Take screenshot
            driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")

            return filepath

        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None
