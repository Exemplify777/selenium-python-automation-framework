"""
Browser management utilities for Selenium WebDriver.
Handles browser initialization, configuration, and cleanup.
"""

import logging
from typing import Optional

from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from framework.config.settings import config

logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages browser instances and configuration."""

    def __init__(self):
        self._driver: Optional[WebDriver] = None

    def setup_browser(self, browser_name: Optional[str] = None) -> WebDriver:
        """
        Set up and configure the browser.

        Args:
            browser_name: Browser to use (chrome, firefox, edge).
                         If None, uses config.browser.

        Returns:
            WebDriver instance
        """
        browser_name = browser_name or config.browser.lower()

        logger.info(f"Setting up {browser_name} browser")

        if browser_name == "chrome":
            self._driver = self._setup_chrome()
        elif browser_name == "firefox":
            self._driver = self._setup_firefox()
        elif browser_name == "edge":
            self._driver = self._setup_edge()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        # Configure browser settings
        self._configure_browser()

        # Configure Selene to use our driver
        browser.config.driver = self._driver
        browser.config.timeout = config.explicit_wait
        browser.config.base_url = config.base_url

        return self._driver

    def _setup_chrome(self) -> WebDriver:
        """Set up Chrome browser."""
        options = ChromeOptions()

        # Basic options
        if config.headless:
            options.add_argument("--headless")

        options.add_argument(f"--window-size={config.window_size}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        # Performance options
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")

        # Security options
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        # Set download preferences
        prefs = {
            "download.default_directory": str(config.project_root / "downloads"),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)

        # Remote execution
        if config.remote_execution and config.selenium_hub_url:
            return webdriver.Remote(
                command_executor=config.selenium_hub_url, options=options
            )

        # Local execution
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def _setup_firefox(self) -> WebDriver:
        """Set up Firefox browser."""
        options = FirefoxOptions()

        if config.headless:
            options.add_argument("--headless")

        options.add_argument(f"--width={config.window_width}")
        options.add_argument(f"--height={config.window_height}")

        # Set preferences
        options.set_preference("browser.download.folderList", 2)
        options.set_preference(
            "browser.download.dir", str(config.project_root / "downloads")
        )
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/octet-stream"
        )

        # Remote execution
        if config.remote_execution and config.selenium_hub_url:
            return webdriver.Remote(
                command_executor=config.selenium_hub_url, options=options
            )

        # Local execution
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    def _setup_edge(self) -> WebDriver:
        """Set up Edge browser."""
        options = EdgeOptions()

        if config.headless:
            options.add_argument("--headless")

        options.add_argument(f"--window-size={config.window_size}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Remote execution
        if config.remote_execution and config.selenium_hub_url:
            return webdriver.Remote(
                command_executor=config.selenium_hub_url, options=options
            )

        # Local execution
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    def _configure_browser(self) -> None:
        """Configure browser settings after initialization."""
        if not self._driver:
            return

        # Set timeouts
        self._driver.implicitly_wait(config.implicit_wait)
        self._driver.set_page_load_timeout(config.page_load_timeout)

        # Maximize window if not headless
        if not config.headless:
            self._driver.maximize_window()

    def quit_browser(self) -> None:
        """Quit the browser and clean up."""
        if self._driver:
            logger.info("Closing browser")
            self._driver.quit()
            self._driver = None

    @property
    def driver(self) -> Optional[WebDriver]:
        """Get the current WebDriver instance."""
        return self._driver


# Global browser manager instance
browser_manager = BrowserManager()
