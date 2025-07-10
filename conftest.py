"""
Pytest configuration and fixtures for the test automation framework.
Provides common fixtures and setup/teardown functionality.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Generator

import pytest
from selene import browser
from selenium.webdriver.remote.webdriver import WebDriver

from framework.config.settings import config
from framework.core.browser_manager import browser_manager
from framework.utils.helpers import FileHelper
from framework.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


def pytest_configure(config):
    """Configure pytest with custom settings."""
    from framework.config.settings import config as app_config

    # Ensure required directories exist
    FileHelper.ensure_directory(app_config.reports_dir)
    FileHelper.ensure_directory(app_config.logs_dir)
    FileHelper.ensure_directory(app_config.screenshots_dir)

    # Setup logging
    setup_logging()

    logger.info("Pytest configuration completed")


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default=config.browser,
        help="Browser to use for testing (chrome, firefox, edge)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=config.headless,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=config.base_url,
        help="Base URL for the application under test",
    )
    parser.addoption(
        "--environment",
        action="store",
        default=config.environment,
        help="Test environment (dev, staging, prod)",
    )
    parser.addoption(
        "--remote",
        action="store_true",
        default=config.remote_execution,
        help="Run tests on remote Selenium Grid",
    )
    parser.addoption(
        "--hub-url",
        action="store",
        default=config.selenium_hub_url,
        help="Selenium Grid hub URL",
    )


@pytest.fixture(scope="session", autouse=True)
def test_session_setup(request):
    """Session-level setup and teardown."""
    logger.info("Starting test session")

    # Update config with command line options
    config.browser = request.config.getoption("--browser")
    config.headless = request.config.getoption("--headless")
    config.base_url = request.config.getoption("--base-url")
    config.environment = request.config.getoption("--environment")
    config.remote_execution = request.config.getoption("--remote")

    if request.config.getoption("--hub-url"):
        config.selenium_hub_url = request.config.getoption("--hub-url")

    logger.info(
        f"Test configuration: Browser={config.browser}, Headless={config.headless}, "
        f"Environment={config.environment}, Base URL={config.base_url}"
    )

    yield

    logger.info("Test session completed")


@pytest.fixture(scope="function")
def driver(request) -> Generator[WebDriver, None, None]:
    """
    WebDriver fixture that provides a fresh browser instance for each test.

    Yields:
        WebDriver instance
    """
    logger.info(f"Setting up browser for test: {request.node.name}")

    # Setup browser
    driver_instance = browser_manager.setup_browser()

    yield driver_instance

    # Teardown
    if config.screenshot_on_failure and request.node.rep_call.failed:
        # Take screenshot on failure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"failure_{request.node.name}_{timestamp}.png"
        screenshot_path = config.screenshots_dir / screenshot_name

        try:
            driver_instance.save_screenshot(str(screenshot_path))
            logger.info(f"Failure screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")

    browser_manager.quit_browser()
    logger.info(f"Browser closed for test: {request.node.name}")


@pytest.fixture(scope="function")
def browser_session(driver) -> Generator[None, None, None]:
    """
    Browser session fixture that ensures Selene browser is properly configured.

    Args:
        driver: WebDriver fixture

    Yields:
        None (browser is available globally through selene.browser)
    """
    # Browser is already configured in browser_manager.setup_browser()
    yield

    # Additional cleanup if needed
    try:
        browser.quit()
    except Exception:
        pass  # Browser might already be closed


@pytest.fixture(scope="function")
def test_data():
    """
    Test data fixture that provides access to test data files.

    Returns:
        Dictionary with test data
    """
    test_data_path = config.project_root / config.test_data_path

    if not test_data_path.exists():
        return {}

    test_data = {}

    # Load JSON test data files
    for json_file in test_data_path.glob("*.json"):
        try:
            data = FileHelper.read_json(json_file)
            test_data[json_file.stem] = data
        except Exception as e:
            logger.warning(f"Failed to load test data from {json_file}: {e}")

    return test_data


@pytest.fixture(scope="function")
def api_client():
    """
    API client fixture for API testing.

    Returns:
        APIHelper instance
    """
    from framework.utils.helpers import APIHelper

    return APIHelper()


@pytest.fixture(scope="function")
def data_generator():
    """
    Data generator fixture for creating test data.

    Returns:
        DataGenerator instance
    """
    from framework.utils.helpers import DataGenerator

    return DataGenerator()


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Automatically log test information."""
    logger.info(f"Starting test: {request.node.name}")
    logger.info(f"Test file: {request.node.fspath}")

    yield

    logger.info(f"Finished test: {request.node.name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results for use in fixtures.
    This allows fixtures to know if a test passed or failed.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def allure_environment_properties():
    """Create allure environment properties file."""
    environment_properties = {
        "Browser": config.browser,
        "Browser.Version": config.browser_version,
        "Environment": config.environment,
        "Base.URL": config.base_url,
        "Headless": str(config.headless),
        "Remote.Execution": str(config.remote_execution),
        "Python.Version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        "Platform": os.name,
    }

    # Write environment properties for Allure
    allure_results_dir = Path(config.allure_results_dir)
    allure_results_dir.mkdir(parents=True, exist_ok=True)

    env_file = allure_results_dir / "environment.properties"
    with open(env_file, "w") as f:
        for key, value in environment_properties.items():
            f.write(f"{key}={value}\n")

    return environment_properties


# Pytest markers for test categorization
# pytest_plugins are automatically loaded when installed


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
        elif "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)

        # Add slow marker for tests that might take longer
        if "slow" in item.name.lower() or "integration" in item.name.lower():
            item.add_marker(pytest.mark.slow)


def pytest_html_report_title(report):
    """Customize HTML report title."""
    report.title = "Test Automation Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Customize HTML report summary."""
    prefix.extend(
        [
            f"<p>Environment: {config.environment}</p>",
            f"<p>Base URL: {config.base_url}</p>",
            f"<p>Browser: {config.browser}</p>",
        ]
    )
