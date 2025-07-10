"""
Google search page object for demonstration purposes.
Shows how to implement page objects using the framework.
"""

from typing import List

from selene import be, have
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from framework.core.base_page import BasePage
from framework.utils.logger import get_logger


logger = get_logger(__name__)


class GooglePage(BasePage):
    """Google search page object."""
    
    def __init__(self):
        super().__init__()
        self.url_path = ""  # Google is the base URL
    
    # Locators
    SEARCH_BOX = '[name="q"]'
    SEARCH_BUTTON = '[name="btnK"]'
    LUCKY_BUTTON = '[name="btnI"]'
    SEARCH_RESULTS = '#search .g'
    SEARCH_RESULT_TITLES = '#search .g h3'
    SEARCH_RESULT_LINKS = '#search .g a'
    SEARCH_STATS = '#result-stats'
    SUGGESTIONS = '.erkvQe li'
    LOGO = '#hplogo'
    
    def open_google(self) -> "GooglePage":
        """
        Open Google homepage.
        
        Returns:
            Self for method chaining
        """
        logger.info("Opening Google homepage")
        self.open()
        self.wait_for_page_load()
        return self
    
    def search(self, query: str) -> "GoogleSearchResultsPage":
        """
        Perform a search on Google.
        
        Args:
            query: Search query
            
        Returns:
            GoogleSearchResultsPage instance
        """
        logger.info(f"Searching for: {query}")
        
        # Wait for search box and enter query
        search_box = self.wait_for_element_visible(self.SEARCH_BOX)
        search_box.clear().type(query)
        
        # Press Enter or click search button
        search_box.press_enter()
        
        # Return search results page
        return GoogleSearchResultsPage()
    
    def search_with_button(self, query: str) -> "GoogleSearchResultsPage":
        """
        Perform a search using the search button.
        
        Args:
            query: Search query
            
        Returns:
            GoogleSearchResultsPage instance
        """
        logger.info(f"Searching for: {query} (using button)")
        
        # Enter search query
        self.type_text(self.SEARCH_BOX, query)
        
        # Click search button
        self.click_element(self.SEARCH_BUTTON)
        
        return GoogleSearchResultsPage()
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions for a query.
        
        Args:
            query: Partial search query
            
        Returns:
            List of search suggestions
        """
        logger.info(f"Getting suggestions for: {query}")
        
        # Type query to trigger suggestions
        search_box = self.wait_for_element_visible(self.SEARCH_BOX)
        search_box.clear().type(query)
        
        # Wait for suggestions to appear
        suggestions = self.find_elements(self.SUGGESTIONS)
        
        # Extract suggestion text
        suggestion_texts = []
        for suggestion in suggestions:
            try:
                text = suggestion.get_text()
                if text:
                    suggestion_texts.append(text)
            except Exception as e:
                logger.debug(f"Could not get suggestion text: {e}")
        
        return suggestion_texts
    
    def is_logo_visible(self) -> bool:
        """
        Check if Google logo is visible.
        
        Returns:
            True if logo is visible
        """
        return self.is_element_visible(self.LOGO)
    
    def click_lucky_button(self) -> "BasePage":
        """
        Click "I'm Feeling Lucky" button.
        
        Returns:
            BasePage instance (destination page is unknown)
        """
        logger.info("Clicking 'I'm Feeling Lucky' button")
        self.click_element(self.LUCKY_BUTTON)
        return BasePage()


class GoogleSearchResultsPage(BasePage):
    """Google search results page object."""
    
    def __init__(self):
        super().__init__()
    
    # Locators
    SEARCH_BOX = '[name="q"]'
    SEARCH_RESULTS = '#search .g'
    SEARCH_RESULT_TITLES = '#search .g h3'
    SEARCH_RESULT_LINKS = '#search .g a[href]'
    SEARCH_STATS = '#result-stats'
    NEXT_PAGE = '#pnnext'
    PREVIOUS_PAGE = '#pnprev'
    PAGE_NUMBERS = '#nav a'
    
    def wait_for_results(self) -> "GoogleSearchResultsPage":
        """
        Wait for search results to load.
        
        Returns:
            Self for method chaining
        """
        logger.info("Waiting for search results")
        self.wait_for_element_visible(self.SEARCH_RESULTS)
        return self
    
    def get_search_results_count(self) -> int:
        """
        Get the number of search results on the current page.
        
        Returns:
            Number of search results
        """
        results = self.find_elements(self.SEARCH_RESULTS)
        count = len(results)
        logger.info(f"Found {count} search results")
        return count
    
    def get_search_result_titles(self) -> List[str]:
        """
        Get titles of all search results.
        
        Returns:
            List of search result titles
        """
        titles = []
        title_elements = self.find_elements(self.SEARCH_RESULT_TITLES)
        
        for element in title_elements:
            try:
                title = element.get_text()
                if title:
                    titles.append(title)
            except Exception as e:
                logger.debug(f"Could not get title text: {e}")
        
        logger.info(f"Retrieved {len(titles)} search result titles")
        return titles
    
    def click_search_result(self, index: int = 0) -> "BasePage":
        """
        Click on a search result by index.
        
        Args:
            index: Index of the search result to click (0-based)
            
        Returns:
            BasePage instance
        """
        logger.info(f"Clicking search result at index {index}")
        
        result_links = self.find_elements(self.SEARCH_RESULT_LINKS)
        
        if index < len(result_links):
            result_links[index].click()
            return BasePage()
        else:
            raise IndexError(f"Search result index {index} is out of range")
    
    def search_again(self, new_query: str) -> "GoogleSearchResultsPage":
        """
        Perform a new search from the results page.
        
        Args:
            new_query: New search query
            
        Returns:
            GoogleSearchResultsPage instance
        """
        logger.info(f"Performing new search: {new_query}")
        
        search_box = self.wait_for_element_visible(self.SEARCH_BOX)
        search_box.clear().type(new_query).press_enter()
        
        return GoogleSearchResultsPage()
    
    def go_to_next_page(self) -> "GoogleSearchResultsPage":
        """
        Go to the next page of search results.
        
        Returns:
            GoogleSearchResultsPage instance
        """
        logger.info("Going to next page of results")
        
        if self.is_element_visible(self.NEXT_PAGE):
            self.click_element(self.NEXT_PAGE)
            return GoogleSearchResultsPage()
        else:
            raise Exception("Next page button is not available")
    
    def go_to_previous_page(self) -> "GoogleSearchResultsPage":
        """
        Go to the previous page of search results.
        
        Returns:
            GoogleSearchResultsPage instance
        """
        logger.info("Going to previous page of results")
        
        if self.is_element_visible(self.PREVIOUS_PAGE):
            self.click_element(self.PREVIOUS_PAGE)
            return GoogleSearchResultsPage()
        else:
            raise Exception("Previous page button is not available")
    
    def get_search_stats(self) -> str:
        """
        Get search statistics text.
        
        Returns:
            Search statistics text
        """
        if self.is_element_visible(self.SEARCH_STATS):
            stats = self.get_element_text(self.SEARCH_STATS)
            logger.info(f"Search stats: {stats}")
            return stats
        return ""
    
    def verify_search_term_in_results(self, search_term: str) -> bool:
        """
        Verify that the search term appears in the search results.
        
        Args:
            search_term: Term to search for in results
            
        Returns:
            True if search term is found in results
        """
        titles = self.get_search_result_titles()
        search_term_lower = search_term.lower()
        
        for title in titles:
            if search_term_lower in title.lower():
                logger.info(f"Search term '{search_term}' found in result: {title}")
                return True
        
        logger.warning(f"Search term '{search_term}' not found in any result titles")
        return False
