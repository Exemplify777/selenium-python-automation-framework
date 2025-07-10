"""
Configuration settings for the test automation framework.
Manages environment variables and test configuration.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class TestConfig(BaseSettings):
    """Test configuration settings."""

    # Browser Configuration
    browser: str = Field(default="chrome", env="BROWSER")
    headless: bool = Field(default=False, env="HEADLESS")
    browser_version: str = Field(default="latest", env="BROWSER_VERSION")
    window_size: str = Field(default="1920x1080", env="WINDOW_SIZE")
    implicit_wait: int = Field(default=10, env="IMPLICIT_WAIT")
    explicit_wait: int = Field(default=30, env="EXPLICIT_WAIT")
    page_load_timeout: int = Field(default=30, env="PAGE_LOAD_TIMEOUT")

    # Test Environment
    base_url: str = Field(default="https://example.com", env="BASE_URL")
    environment: str = Field(default="staging", env="ENVIRONMENT")
    test_data_path: str = Field(default="tests/data", env="TEST_DATA_PATH")

    # Selenium Grid
    selenium_hub_url: Optional[str] = Field(default=None, env="SELENIUM_HUB_URL")
    remote_execution: bool = Field(default=False, env="REMOTE_EXECUTION")

    # Reporting
    allure_results_dir: str = Field(
        default="reports/allure-results", env="ALLURE_RESULTS_DIR"
    )
    html_report_dir: str = Field(default="reports", env="HTML_REPORT_DIR")
    screenshot_on_failure: bool = Field(default=True, env="SCREENSHOT_ON_FAILURE")
    video_recording: bool = Field(default=False, env="VIDEO_RECORDING")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="logs/test.log", env="LOG_FILE")

    # Test Credentials
    test_user_email: str = Field(default="test@example.com", env="TEST_USER_EMAIL")
    test_user_password: str = Field(default="testpassword123", env="TEST_USER_PASSWORD")

    # API Configuration
    api_base_url: str = Field(default="https://api.example.com", env="API_BASE_URL")
    api_key: Optional[str] = Field(default=None, env="API_KEY")
    api_timeout: int = Field(default=30, env="API_TIMEOUT")

    # Database Configuration
    db_host: str = Field(default="localhost", env="DB_HOST")
    db_port: int = Field(default=5432, env="DB_PORT")
    db_name: str = Field(default="testdb", env="DB_NAME")
    db_user: str = Field(default="testuser", env="DB_USER")
    db_password: str = Field(default="testpass", env="DB_PASSWORD")

    # Parallel Execution
    parallel_workers: int = Field(default=4, env="PARALLEL_WORKERS")
    reruns_on_failure: int = Field(default=2, env="RERUNS_ON_FAILURE")

    # Cloud Testing
    cloud_testing: bool = Field(default=False, env="CLOUD_TESTING")
    browserstack_username: Optional[str] = Field(
        default=None, env="BROWSERSTACK_USERNAME"
    )
    browserstack_access_key: Optional[str] = Field(
        default=None, env="BROWSERSTACK_ACCESS_KEY"
    )
    sauce_username: Optional[str] = Field(default=None, env="SAUCE_USERNAME")
    sauce_access_key: Optional[str] = Field(default=None, env="SAUCE_ACCESS_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def window_width(self) -> int:
        """Get window width from window_size setting."""
        return int(self.window_size.split("x")[0])

    @property
    def window_height(self) -> int:
        """Get window height from window_size setting."""
        return int(self.window_size.split("x")[1])

    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent.parent

    @property
    def reports_dir(self) -> Path:
        """Get reports directory path."""
        return self.project_root / "reports"

    @property
    def logs_dir(self) -> Path:
        """Get logs directory path."""
        return self.project_root / "logs"

    @property
    def screenshots_dir(self) -> Path:
        """Get screenshots directory path."""
        return self.project_root / "screenshots"


# Global configuration instance
config = TestConfig()
