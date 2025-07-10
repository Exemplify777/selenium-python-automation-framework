"""
Base page class for Page Object Model implementation.
Provides common functionality for all page objects.
"""

import logging
from typing import Optional, Union, List
from urllib.parse import urljoin

from selene import browser, be, have
from selene.core.entity import Element, Collection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from framework.config.settings import config
from framework.utils.logger import get_logger


logger = get_logger(__name__)


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, url_path: str = ""):
        """
        Initialize the base page.
        
        Args:
            url_path: Relative URL path for this page
        """
        self.url_path = url_path
        self.wait = WebDriverWait(browser.driver, config.explicit_wait)
    
    @property
    def url(self) -> str:
        """Get the full URL for this page."""
        return urljoin(config.base_url, self.url_path)
    
    def open(self) -> "BasePage":
        """
        Open this page in the browser.
        
        Returns:
            Self for method chaining
        """
        logger.info(f"Opening page: {self.url}")
        browser.open(self.url)
        return self
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> "BasePage":
        """
        Wait for the page to load completely.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            Self for method chaining
        """
        timeout = timeout or config.explicit_wait
        
        try:
            self.wait_for_element_visible("body", timeout=timeout)
            logger.info("Page loaded successfully")
        except TimeoutException:
            logger.warning("Page load timeout exceeded")
        
        return self
    
    def get_title(self) -> str:
        """Get the page title."""
        return browser.driver.title
    
    def get_current_url(self) -> str:
        """Get the current URL."""
        return browser.driver.current_url
    
    def refresh(self) -> "BasePage":
        """
        Refresh the current page.
        
        Returns:
            Self for method chaining
        """
        logger.info("Refreshing page")
        browser.driver.refresh()
        return self
    
    def go_back(self) -> "BasePage":
        """
        Navigate back in browser history.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating back")
        browser.driver.back()
        return self
    
    def go_forward(self) -> "BasePage":
        """
        Navigate forward in browser history.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating forward")
        browser.driver.forward()
        return self
    
    def scroll_to_top(self) -> "BasePage":
        """
        Scroll to the top of the page.
        
        Returns:
            Self for method chaining
        """
        browser.driver.execute_script("window.scrollTo(0, 0);")
        return self
    
    def scroll_to_bottom(self) -> "BasePage":
        """
        Scroll to the bottom of the page.
        
        Returns:
            Self for method chaining
        """
        browser.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return self
    
    def scroll_to_element(self, locator: Union[str, tuple]) -> "BasePage":
        """
        Scroll to a specific element.
        
        Args:
            locator: Element locator (CSS selector or tuple)
            
        Returns:
            Self for method chaining
        """
        element = self.find_element(locator)
        browser.driver.execute_script("arguments[0].scrollIntoView(true);", element.locate())
        return self
    
    def find_element(self, locator: Union[str, tuple]) -> Element:
        """
        Find a single element using Selene.
        
        Args:
            locator: Element locator (CSS selector or tuple)
            
        Returns:
            Selene Element
        """
        if isinstance(locator, str):
            return browser.element(locator)
        elif isinstance(locator, tuple):
            by, value = locator
            return browser.element((by, value))
        else:
            raise ValueError(f"Invalid locator type: {type(locator)}")
    
    def find_elements(self, locator: Union[str, tuple]) -> Collection:
        """
        Find multiple elements using Selene.
        
        Args:
            locator: Element locator (CSS selector or tuple)
            
        Returns:
            Selene Collection
        """
        if isinstance(locator, str):
            return browser.all(locator)
        elif isinstance(locator, tuple):
            by, value = locator
            return browser.all((by, value))
        else:
            raise ValueError(f"Invalid locator type: {type(locator)}")
    
    def wait_for_element_visible(self, locator: Union[str, tuple], timeout: Optional[int] = None) -> Element:
        """
        Wait for an element to be visible.
        
        Args:
            locator: Element locator
            timeout: Maximum time to wait in seconds
            
        Returns:
            Selene Element
        """
        timeout = timeout or config.explicit_wait
        element = self.find_element(locator)
        element.with_(timeout=timeout).should(be.visible)
        return element
    
    def wait_for_element_clickable(self, locator: Union[str, tuple], timeout: Optional[int] = None) -> Element:
        """
        Wait for an element to be clickable.
        
        Args:
            locator: Element locator
            timeout: Maximum time to wait in seconds
            
        Returns:
            Selene Element
        """
        timeout = timeout or config.explicit_wait
        element = self.find_element(locator)
        element.with_(timeout=timeout).should(be.clickable)
        return element
    
    def wait_for_text_present(self, locator: Union[str, tuple], text: str, timeout: Optional[int] = None) -> Element:
        """
        Wait for specific text to be present in an element.
        
        Args:
            locator: Element locator
            text: Text to wait for
            timeout: Maximum time to wait in seconds
            
        Returns:
            Selene Element
        """
        timeout = timeout or config.explicit_wait
        element = self.find_element(locator)
        element.with_(timeout=timeout).should(have.text(text))
        return element
    
    def is_element_present(self, locator: Union[str, tuple]) -> bool:
        """
        Check if an element is present on the page.
        
        Args:
            locator: Element locator
            
        Returns:
            True if element is present, False otherwise
        """
        try:
            self.find_element(locator).should(be.present)
            return True
        except Exception:
            return False
    
    def is_element_visible(self, locator: Union[str, tuple]) -> bool:
        """
        Check if an element is visible on the page.
        
        Args:
            locator: Element locator
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            self.find_element(locator).should(be.visible)
            return True
        except Exception:
            return False
    
    def get_element_text(self, locator: Union[str, tuple]) -> str:
        """
        Get text content of an element.
        
        Args:
            locator: Element locator
            
        Returns:
            Element text content
        """
        return self.find_element(locator).get(browser.driver.text)
    
    def click_element(self, locator: Union[str, tuple]) -> "BasePage":
        """
        Click on an element.
        
        Args:
            locator: Element locator
            
        Returns:
            Self for method chaining
        """
        element = self.wait_for_element_clickable(locator)
        element.click()
        logger.info(f"Clicked element: {locator}")
        return self
    
    def type_text(self, locator: Union[str, tuple], text: str, clear_first: bool = True) -> "BasePage":
        """
        Type text into an element.
        
        Args:
            locator: Element locator
            text: Text to type
            clear_first: Whether to clear the field first
            
        Returns:
            Self for method chaining
        """
        element = self.wait_for_element_visible(locator)
        
        if clear_first:
            element.clear()
        
        element.type(text)
        logger.info(f"Typed text into element: {locator}")
        return self
    
    def select_dropdown_by_text(self, locator: Union[str, tuple], text: str) -> "BasePage":
        """
        Select dropdown option by visible text.
        
        Args:
            locator: Dropdown element locator
            text: Visible text of option to select
            
        Returns:
            Self for method chaining
        """
        element = self.wait_for_element_visible(locator)
        element.select_option(text)
        logger.info(f"Selected dropdown option: {text}")
        return self
    
    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Optional filename for the screenshot
            
        Returns:
            Path to the saved screenshot
        """
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_path = config.screenshots_dir / filename
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        
        browser.driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
        
        return str(screenshot_path)
