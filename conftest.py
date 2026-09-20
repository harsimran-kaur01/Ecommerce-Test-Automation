import pytest
import pytest_html
from utils.driver_factory import DriverFactory
from utils.logger import logger
from utils.screenshot import ScreenshotUtil
import os
from datetime import datetime


@pytest.fixture(scope="function")
def driver():
    """Fixture to create and destroy WebDriver"""
    logger.info("=" * 50)
    logger.info("Starting new test execution")

    # Create driver
    driver = DriverFactory.get_driver()
    driver.set_window_size(1920, 1080)

    yield driver

    # Teardown
    logger.info("Test execution completed")
    driver.quit()


@pytest.fixture(scope="session")
def test_data():
    """Load test data"""
    from utils.helpers import Helpers

    return Helpers.load_test_data("users.json")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on failure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Get driver from fixture
        driver = item.funcargs.get("driver", None)
        if driver:
            # Take screenshot
            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = ScreenshotUtil.take_screenshot(
                driver, f"{test_name}_failed"
            )
            logger.error(f"Test '{test_name}' failed. Screenshot: {screenshot_path}")

            # Add screenshot to report
            if screenshot_path:
                rep.extra = getattr(rep, "extra", [])
                rep.extra.append(
                    pytest_html.extras.image(screenshot_path, "Screenshot on failure")
                )


@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "E-Commerce Test Automation Report"


def pytest_configure(config):
    """Configure pytest"""
    # Create reports directory
    os.makedirs("reports", exist_ok=True)

    # Add custom markers
    config.addinivalue_line("markers", "smoke: Smoke test")
    config.addinivalue_line("markers", "regression: Regression test")
    config.addinivalue_line("markers", "critical: Critical path test")


@pytest.fixture(scope="function")
def setup_teardown(driver):
    """Fixture for setup and teardown"""
    logger.info("Setting up test")
    yield
    logger.info("Tearing down test")
