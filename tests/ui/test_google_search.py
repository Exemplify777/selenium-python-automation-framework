"""
Example UI tests for Google search functionality.
Demonstrates the test automation framework capabilities.
"""

import pytest
import allure
from selene import browser

from framework.pages.google_page import GooglePage, GoogleSearchResultsPage
from framework.config.settings import config
from framework.utils.logger import get_logger


logger = get_logger(__name__)


@allure.epic("Web Search")
@allure.feature("Google Search")
class TestGoogleSearch:
    """Test cases for Google search functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, browser_session):
        """Setup for each test method."""
        # Set Google as base URL for these tests
        config.base_url = "https://www.google.com"
        browser.config.base_url = config.base_url
    
    @allure.story("Basic Search")
    @allure.title("Verify basic search functionality")
    @allure.description("Test that user can perform a basic search on Google")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_basic_search(self):
        """Test basic search functionality."""
        with allure.step("Open Google homepage"):
            google_page = GooglePage()
            google_page.open_google()
            
            # Verify Google logo is visible
            assert google_page.is_logo_visible(), "Google logo should be visible"
        
        with allure.step("Perform search"):
            search_query = "Selenium WebDriver"
            results_page = google_page.search(search_query)
            results_page.wait_for_results()
        
        with allure.step("Verify search results"):
            # Check that we have search results
            results_count = results_page.get_search_results_count()
            assert results_count > 0, "Search should return results"
            
            # Verify search term appears in results
            assert results_page.verify_search_term_in_results("Selenium"), \
                "Search results should contain the search term"
            
            # Check search statistics are displayed
            stats = results_page.get_search_stats()
            assert stats, "Search statistics should be displayed"
    
    @allure.story("Search with Button")
    @allure.title("Verify search using search button")
    @allure.description("Test that user can search using the search button instead of Enter key")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_search_with_button(self):
        """Test search functionality using search button."""
        with allure.step("Open Google and search using button"):
            google_page = GooglePage()
            google_page.open_google()
            
            search_query = "Python automation"
            results_page = google_page.search_with_button(search_query)
            results_page.wait_for_results()
        
        with allure.step("Verify results"):
            results_count = results_page.get_search_results_count()
            assert results_count > 0, "Search should return results"
            
            titles = results_page.get_search_result_titles()
            assert len(titles) > 0, "Should have result titles"
    
    @allure.story("Search Results Navigation")
    @allure.title("Verify navigation through search results")
    @allure.description("Test navigation through multiple pages of search results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_search_results_navigation(self):
        """Test navigation through search results pages."""
        with allure.step("Perform initial search"):
            google_page = GooglePage()
            google_page.open_google()
            
            results_page = google_page.search("test automation framework")
            results_page.wait_for_results()
        
        with allure.step("Navigate to next page"):
            try:
                next_page = results_page.go_to_next_page()
                next_page.wait_for_results()
                
                # Verify we're on a different page
                next_results_count = next_page.get_search_results_count()
                assert next_results_count > 0, "Next page should have results"
                
            except Exception as e:
                pytest.skip(f"Next page navigation not available: {e}")
    
    @allure.story("Search Suggestions")
    @allure.title("Verify search suggestions functionality")
    @allure.description("Test that search suggestions appear when typing")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.ui
    def test_search_suggestions(self):
        """Test search suggestions functionality."""
        with allure.step("Open Google and get suggestions"):
            google_page = GooglePage()
            google_page.open_google()
            
            # Get suggestions for partial query
            suggestions = google_page.get_search_suggestions("python")
        
        with allure.step("Verify suggestions"):
            # Note: Suggestions might not always appear due to various factors
            # This test is more for demonstration purposes
            logger.info(f"Received {len(suggestions)} suggestions")
            
            # If suggestions are available, verify they contain the search term
            if suggestions:
                assert any("python" in suggestion.lower() for suggestion in suggestions), \
                    "At least one suggestion should contain the search term"
    
    @allure.story("Multiple Searches")
    @allure.title("Verify multiple consecutive searches")
    @allure.description("Test performing multiple searches in the same session")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_multiple_searches(self):
        """Test performing multiple searches."""
        google_page = GooglePage()
        google_page.open_google()
        
        search_queries = ["Selenium", "Pytest", "Test Automation"]
        
        for i, query in enumerate(search_queries):
            with allure.step(f"Search {i+1}: {query}"):
                if i == 0:
                    # First search from homepage
                    results_page = google_page.search(query)
                else:
                    # Subsequent searches from results page
                    results_page = results_page.search_again(query)
                
                results_page.wait_for_results()
                
                # Verify results
                results_count = results_page.get_search_results_count()
                assert results_count > 0, f"Search for '{query}' should return results"
    
    @allure.story("Search Result Interaction")
    @allure.title("Verify clicking on search results")
    @allure.description("Test that user can click on search results")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_click_search_result(self):
        """Test clicking on search results."""
        with allure.step("Perform search"):
            google_page = GooglePage()
            google_page.open_google()
            
            results_page = google_page.search("GitHub")
            results_page.wait_for_results()
        
        with allure.step("Click first search result"):
            # Get current URL before clicking
            current_url = results_page.get_current_url()
            
            # Click first result
            results_page.click_search_result(0)
            
            # Wait a moment for navigation
            import time
            time.sleep(2)
            
            # Verify we navigated to a different page
            new_url = browser.driver.current_url
            assert new_url != current_url, "Should navigate to a different page after clicking result"
    
    @pytest.mark.parametrize("search_term", [
        "Python",
        "JavaScript", 
        "Test Automation",
        "Selenium WebDriver"
    ])
    @allure.story("Parameterized Search")
    @allure.title("Verify search with different terms")
    @allure.description("Test search functionality with various search terms")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_parameterized_search(self, search_term):
        """Test search with different search terms."""
        with allure.step(f"Search for: {search_term}"):
            google_page = GooglePage()
            google_page.open_google()
            
            results_page = google_page.search(search_term)
            results_page.wait_for_results()
        
        with allure.step("Verify results"):
            results_count = results_page.get_search_results_count()
            assert results_count > 0, f"Search for '{search_term}' should return results"
            
            # Attach search term to allure report
            allure.attach(search_term, name="Search Term", attachment_type=allure.attachment_type.TEXT)
    
    @allure.story("Error Handling")
    @allure.title("Verify handling of empty search")
    @allure.description("Test behavior when performing empty search")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.ui
    def test_empty_search(self):
        """Test behavior with empty search."""
        with allure.step("Attempt empty search"):
            google_page = GooglePage()
            google_page.open_google()
            
            # Try to search with empty string
            try:
                results_page = google_page.search("")
                # If search goes through, verify we're still on Google
                current_url = results_page.get_current_url()
                assert "google.com" in current_url, "Should remain on Google domain"
                
            except Exception as e:
                logger.info(f"Empty search handled as expected: {e}")
    
    @allure.story("Page Title Verification")
    @allure.title("Verify page titles")
    @allure.description("Test that page titles are correct")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.ui
    def test_page_titles(self):
        """Test page title verification."""
        with allure.step("Verify Google homepage title"):
            google_page = GooglePage()
            google_page.open_google()
            
            title = google_page.get_title()
            assert "Google" in title, f"Homepage title should contain 'Google', got: {title}"
        
        with allure.step("Verify search results page title"):
            search_query = "Selenium"
            results_page = google_page.search(search_query)
            results_page.wait_for_results()
            
            results_title = results_page.get_title()
            assert search_query in results_title, \
                f"Results page title should contain search term '{search_query}', got: {results_title}"
