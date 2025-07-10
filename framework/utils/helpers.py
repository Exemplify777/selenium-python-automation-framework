"""
Utility helper functions for test automation.
Provides common functionality used across tests.
"""

import json
import random
import string
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
from faker import Faker
from PIL import Image, ImageDraw, ImageFont

from framework.config.settings import config
from framework.utils.logger import get_logger


logger = get_logger(__name__)
fake = Faker()


class DataGenerator:
    """Generate test data for various scenarios."""
    
    @staticmethod
    def random_string(length: int = 10, include_digits: bool = True) -> str:
        """
        Generate a random string.
        
        Args:
            length: Length of the string
            include_digits: Whether to include digits
            
        Returns:
            Random string
        """
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def random_email(domain: str = "example.com") -> str:
        """
        Generate a random email address.
        
        Args:
            domain: Email domain
            
        Returns:
            Random email address
        """
        username = DataGenerator.random_string(8).lower()
        return f"{username}@{domain}"
    
    @staticmethod
    def random_phone() -> str:
        """Generate a random phone number."""
        return fake.phone_number()
    
    @staticmethod
    def random_name() -> Dict[str, str]:
        """
        Generate random first and last name.
        
        Returns:
            Dictionary with 'first_name' and 'last_name'
        """
        return {
            'first_name': fake.first_name(),
            'last_name': fake.last_name()
        }
    
    @staticmethod
    def random_address() -> Dict[str, str]:
        """
        Generate a random address.
        
        Returns:
            Dictionary with address components
        """
        return {
            'street': fake.street_address(),
            'city': fake.city(),
            'state': fake.state(),
            'zip_code': fake.zipcode(),
            'country': fake.country()
        }
    
    @staticmethod
    def random_date(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> datetime:
        """
        Generate a random date between start and end dates.
        
        Args:
            start_date: Start date (default: 1 year ago)
            end_date: End date (default: today)
            
        Returns:
            Random datetime
        """
        if not start_date:
            start_date = datetime.now() - timedelta(days=365)
        if not end_date:
            end_date = datetime.now()
        
        return fake.date_time_between(start_date=start_date, end_date=end_date)


class FileHelper:
    """File and directory operations helper."""
    
    @staticmethod
    def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Read JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @staticmethod
    def write_json(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
        """
        Write data to JSON file.
        
        Args:
            data: Data to write
            file_path: Path to JSON file
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    
    @staticmethod
    def read_text(file_path: Union[str, Path]) -> str:
        """
        Read text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    @staticmethod
    def write_text(content: str, file_path: Union[str, Path]) -> None:
        """
        Write content to text file.
        
        Args:
            content: Content to write
            file_path: Path to text file
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    
    @staticmethod
    def ensure_directory(directory_path: Union[str, Path]) -> Path:
        """
        Ensure directory exists, create if it doesn't.
        
        Args:
            directory_path: Path to directory
            
        Returns:
            Path object
        """
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        return path


class WaitHelper:
    """Wait and timing utilities."""
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, poll_interval: float = 0.5) -> bool:
        """
        Wait for a condition to be true.
        
        Args:
            condition_func: Function that returns True when condition is met
            timeout: Maximum time to wait in seconds
            poll_interval: Time between checks in seconds
            
        Returns:
            True if condition was met, False if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if condition_func():
                    return True
            except Exception as e:
                logger.debug(f"Condition check failed: {e}")
            
            time.sleep(poll_interval)
        
        return False
    
    @staticmethod
    def retry_on_exception(func, max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
        """
        Retry a function on exception.
        
        Args:
            func: Function to retry
            max_attempts: Maximum number of attempts
            delay: Delay between attempts in seconds
            exceptions: Tuple of exceptions to catch
            
        Returns:
            Function result
            
        Raises:
            Last exception if all attempts fail
        """
        last_exception = None
        
        for attempt in range(max_attempts):
            try:
                return func()
            except exceptions as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_attempts - 1:
                    time.sleep(delay)
        
        raise last_exception


class APIHelper:
    """API testing utilities."""
    
    def __init__(self, base_url: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        """
        Initialize API helper.
        
        Args:
            base_url: Base URL for API requests
            headers: Default headers for requests
        """
        self.base_url = base_url or config.api_base_url
        self.session = requests.Session()
        
        if headers:
            self.session.headers.update(headers)
        
        if config.api_key:
            self.session.headers.update({'Authorization': f'Bearer {config.api_key}'})
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make GET request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.get(url, params=params, timeout=config.api_timeout, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make POST request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.post(url, data=data, json=json, timeout=config.api_timeout, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make PUT request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.put(url, data=data, json=json, timeout=config.api_timeout, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.delete(url, timeout=config.api_timeout, **kwargs)


class ImageHelper:
    """Image processing utilities."""
    
    @staticmethod
    def create_test_image(width: int = 100, height: int = 100, color: str = 'red', text: str = 'TEST') -> Path:
        """
        Create a test image file.
        
        Args:
            width: Image width
            height: Image height
            color: Background color
            text: Text to add to image
            
        Returns:
            Path to created image
        """
        # Create image
        image = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(image)
        
        # Add text
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except Exception:
            font = None
        
        # Calculate text position (center)
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(text) * 6  # Approximate
            text_height = 11  # Approximate
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = config.project_root / "temp" / f"test_image_{timestamp}.png"
        image_path.parent.mkdir(parents=True, exist_ok=True)
        
        image.save(image_path)
        logger.info(f"Test image created: {image_path}")
        
        return image_path


class StringHelper:
    """String manipulation utilities."""
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Input text
            
        Returns:
            Text with normalized whitespace
        """
        return ' '.join(text.split())
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """
        Extract all numbers from text.
        
        Args:
            text: Input text
            
        Returns:
            List of extracted numbers
        """
        import re
        return [int(match) for match in re.findall(r'\d+', text)]
    
    @staticmethod
    def mask_sensitive_data(text: str, mask_char: str = '*') -> str:
        """
        Mask sensitive data in text (emails, phone numbers, etc.).
        
        Args:
            text: Input text
            mask_char: Character to use for masking
            
        Returns:
            Text with sensitive data masked
        """
        import re
        
        # Mask email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 
                     lambda m: m.group(0)[:2] + mask_char * (len(m.group(0)) - 4) + m.group(0)[-2:], text)
        
        # Mask phone numbers
        text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', 
                     lambda m: mask_char * 3 + '-' + mask_char * 3 + '-' + m.group(0)[-4:], text)
        
        return text
