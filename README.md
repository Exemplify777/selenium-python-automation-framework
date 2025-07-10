# 🚀 Selenium Python Test Automation Framework

[![Test Automation CI/CD](https://github.com/Exemplify777/selenium-python-automation-framework/actions/workflows/test-automation.yml/badge.svg)](https://github.com/Exemplify777/selenium-python-automation-framework/actions/workflows/test-automation.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Template Repository](https://img.shields.io/badge/template-repository-brightgreen.svg)](https://github.com/Exemplify777/selenium-python-automation-framework/generate)

A comprehensive, production-ready test automation framework built with Python, Selenium, and Selene. This framework provides a robust foundation for web application testing with modern best practices, rich reporting, and CI/CD integration.

> **🎯 Template Repository**: Click "Use this template" to create your own test automation project instantly!

## ✨ Features

- 🎯 **Modern Architecture**: Built with Python 3.8+ using Selene for elegant web automation
- 🔧 **Flexible Configuration**: Environment-based configuration with `.env` support
- 📊 **Rich Reporting**: HTML reports, Allure integration, and detailed logging
- 🚀 **CI/CD Ready**: GitHub Actions workflows with parallel execution
- 🧪 **Multiple Test Types**: UI, API, and integration testing support
- 🔄 **Cross-Browser**: Chrome, Firefox, and Edge support
- 📱 **Responsive Testing**: Configurable window sizes and mobile testing
- 🛡️ **Quality Assurance**: Pre-commit hooks, linting, and type checking
- 📦 **Template Ready**: Use as GitHub template for quick project setup

## 🏗️ Project Structure

```
selenium-python-framework/
├── framework/                  # Core framework components
│   ├── core/                  # Base classes and browser management
│   │   ├── base_page.py      # Base page object class
│   │   └── browser_manager.py # WebDriver management
│   ├── pages/                 # Page Object Model implementations
│   │   └── google_page.py    # Example page objects
│   ├── utils/                 # Utility functions and helpers
│   │   ├── helpers.py        # Common helper functions
│   │   └── logger.py         # Logging configuration
│   └── config/               # Configuration management
│       └── settings.py       # Settings and environment config
├── tests/                     # Test cases
│   ├── ui/                   # UI test cases
│   │   └── test_google_search.py
│   ├── api/                  # API test cases
│   │   └── test_example_api.py
│   └── data/                 # Test data files
│       └── test_users.json
├── reports/                   # Test reports and results
├── logs/                     # Log files
├── screenshots/              # Screenshots on failure
├── .github/workflows/        # GitHub Actions CI/CD
├── conftest.py              # Pytest configuration and fixtures
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Chrome, Firefox, or Edge browser

### Installation

1. **Use this template** (if using as GitHub template):
   ```bash
   # Click "Use this template" button on GitHub
   # Or clone the repository
   git clone https://github.com/Exemplify777/selenium-python-automation-framework.git
   cd selenium-python-automation-framework
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Run example tests**:
   ```bash
   # Run all tests
   pytest

   # Run specific test suite
   pytest tests/ui/ -m smoke

   # Run with specific browser
   pytest --browser=chrome --headless
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Browser Configuration
BROWSER=chrome
HEADLESS=false
WINDOW_SIZE=1920x1080

# Test Environment
BASE_URL=https://example.com
ENVIRONMENT=staging

# Reporting
SCREENSHOT_ON_FAILURE=true
ALLURE_RESULTS_DIR=reports/allure-results
```

### Command Line Options

```bash
# Browser selection
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge

# Headless mode
pytest --headless

# Environment
pytest --environment=staging
pytest --base-url=https://staging.example.com

# Parallel execution
pytest -n 4

# Test markers
pytest -m smoke
pytest -m "not slow"
```

## 📝 Writing Tests

### Page Objects

Create page objects by extending `BasePage`:

```python
from framework.core.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self):
        super().__init__(url_path="/login")

    # Locators
    EMAIL_INPUT = '[name="email"]'
    PASSWORD_INPUT = '[name="password"]'
    LOGIN_BUTTON = '[type="submit"]'

    def login(self, email: str, password: str):
        self.open()
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        return HomePage()
```

### Test Cases

Write tests using pytest and Allure:

```python
import pytest
import allure
from framework.pages.login_page import LoginPage

@allure.epic("Authentication")
@allure.feature("User Login")
class TestLogin:

    @allure.story("Valid Login")
    @pytest.mark.smoke
    def test_valid_login(self, browser_session, test_data):
        user = test_data["valid_users"][0]

        with allure.step("Open login page"):
            login_page = LoginPage()

        with allure.step("Perform login"):
            home_page = login_page.login(user["email"], user["password"])

        with allure.step("Verify successful login"):
            assert home_page.is_user_logged_in()
```

## 🧪 Test Execution

### Local Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/ui/test_google_search.py

# Run with markers
pytest -m smoke
pytest -m "ui and not slow"

# Run with custom configuration
pytest --browser=firefox --headless --base-url=https://staging.example.com

# Parallel execution
pytest -n 4 --dist=loadfile

# Generate reports
pytest --html=reports/report.html --alluredir=reports/allure-results
```

### CI/CD Execution

The framework includes GitHub Actions workflows:

- **Continuous Integration**: Runs on push/PR to main branches
- **Scheduled Tests**: Daily automated test runs
- **Manual Triggers**: On-demand test execution with parameters
- **Parallel Execution**: Matrix strategy for multiple browsers/Python versions

## 📊 Reporting

### HTML Reports

```bash
pytest --html=reports/report.html --self-contained-html
```

### Allure Reports

```bash
# Generate results
pytest --alluredir=reports/allure-results

# Serve report
allure serve reports/allure-results
```

### Logging

Structured logging with different levels:

```python
from framework.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Test step completed")
logger.error("Test failed", extra={"error_code": 500})
```

## 🔄 CI/CD Integration

### GitHub Actions

The framework includes comprehensive GitHub Actions workflows:

1. **Code Quality**: Linting, formatting, type checking
2. **Test Matrix**: Multi-browser and Python version testing
3. **Parallel Execution**: Fast test execution
4. **Allure Reports**: Automatic report generation and deployment
5. **Security Scanning**: Bandit security analysis

### Workflow Triggers

- Push to main/develop branches
- Pull requests
- Scheduled runs (daily at 2 AM UTC)
- Manual dispatch with parameters

## 🛠️ Development

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 .

# Type checking
mypy framework/
```

### Adding New Tests

1. Create page objects in `framework/pages/`
2. Add test cases in appropriate `tests/` subdirectory
3. Use appropriate pytest markers
4. Add test data to `tests/data/` if needed
5. Update documentation

## 📚 Best Practices

### Page Objects

- Use descriptive locator names
- Implement fluent interfaces (method chaining)
- Keep page objects focused and cohesive
- Use explicit waits instead of implicit waits

### Test Design

- Follow AAA pattern (Arrange, Act, Assert)
- Use meaningful test names and descriptions
- Implement proper test data management
- Use appropriate test markers for categorization

### Configuration

- Use environment variables for configuration
- Keep sensitive data out of code
- Use different configurations for different environments
- Document configuration options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](https://github.com/Exemplify777/selenium-python-automation-framework/wiki)
- 🐛 [Issue Tracker](https://github.com/Exemplify777/selenium-python-automation-framework/issues)
- 💬 [Discussions](https://github.com/Exemplify777/selenium-python-automation-framework/discussions)

## 🔧 Advanced Configuration

### Remote Execution (Selenium Grid)

```bash
# Set environment variables
REMOTE_EXECUTION=true
SELENIUM_HUB_URL=http://selenium-hub:4444/wd/hub

# Run tests
pytest --remote --hub-url=http://selenium-hub:4444/wd/hub
```

### Cloud Testing Integration

```bash
# BrowserStack
CLOUD_TESTING=true
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key

# Sauce Labs
SAUCE_USERNAME=your_username
SAUCE_ACCESS_KEY=your_access_key
```

### Docker Support

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["pytest", "--headless", "--browser=chrome"]
```

## 📋 Test Data Management

### JSON Test Data

```json
{
  "users": [
    {
      "email": "test@example.com",
      "password": "TestPass123!",
      "role": "user"
    }
  ]
}
```

### Dynamic Data Generation

```python
from framework.utils.helpers import DataGenerator

def test_user_registration(data_generator):
    user_data = {
        "email": data_generator.random_email(),
        "name": data_generator.random_name(),
        "phone": data_generator.random_phone()
    }
```

## 🔍 Debugging and Troubleshooting

### Common Issues

1. **WebDriver Issues**
   ```bash
   # Update WebDriver
   pip install --upgrade webdriver-manager
   ```

2. **Element Not Found**
   ```python
   # Use explicit waits
   element = self.wait_for_element_visible(locator, timeout=30)
   ```

3. **Flaky Tests**
   ```bash
   # Run with retries
   pytest --reruns 2 --reruns-delay 1
   ```

### Debug Mode

```bash
# Run with verbose output
pytest -v -s

# Run single test with debugging
pytest tests/ui/test_login.py::TestLogin::test_valid_login -v -s
```

## 🙏 Acknowledgments

- [Selene](https://github.com/yashaka/selene) - Elegant web automation
- [Pytest](https://pytest.org/) - Testing framework
- [Allure](https://docs.qameta.io/allure/) - Test reporting
- [Selenium](https://selenium.dev/) - Web automation standard

---

**Happy Testing! 🎉**
