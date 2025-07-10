# Contributing to Selenium Python Test Automation Framework

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed and what behavior you expected
- Include screenshots if applicable
- Include your environment details (OS, Python version, browser, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- List some other frameworks or applications where this enhancement exists

### Pull Requests

1. Fork the repository
2. Create a new branch from `main` for your feature or bug fix
3. Make your changes
4. Add or update tests as necessary
5. Ensure all tests pass
6. Update documentation if needed
7. Submit a pull request

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Exemplify777/selenium-python-framework.git
   cd selenium-python-framework
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

5. **Run tests**:
   ```bash
   pytest
   ```

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for linting
- Use mypy for type checking

### Code Quality

- Write clear, readable code with meaningful variable and function names
- Add docstrings to all public functions and classes
- Include type hints where appropriate
- Write comprehensive tests for new functionality
- Maintain test coverage above 80%

### Commit Messages

- Use clear and meaningful commit messages
- Start with a verb in the imperative mood (e.g., "Add", "Fix", "Update")
- Keep the first line under 50 characters
- Reference issues and pull requests when applicable

Example:
```
Add support for Edge browser testing

- Implement Edge browser configuration in browser_manager.py
- Add Edge-specific options and capabilities
- Update documentation with Edge setup instructions

Closes #123
```

## Testing Guidelines

### Writing Tests

- Follow the AAA pattern (Arrange, Act, Assert)
- Use descriptive test names that explain what is being tested
- Group related tests in classes
- Use appropriate pytest markers (@pytest.mark.smoke, @pytest.mark.ui, etc.)
- Add Allure annotations for better reporting

### Test Structure

```python
@allure.epic("Feature Area")
@allure.feature("Specific Feature")
class TestFeatureName:
    
    @allure.story("User Story")
    @allure.title("Test case description")
    @pytest.mark.smoke
    def test_specific_functionality(self, browser_session):
        # Arrange
        page = SomePage()
        
        # Act
        with allure.step("Perform action"):
            result = page.perform_action()
        
        # Assert
        with allure.step("Verify result"):
            assert result.is_successful()
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/ui/test_example.py

# Run with specific markers
pytest -m smoke

# Run with coverage
pytest --cov=framework

# Run with HTML report
pytest --html=reports/report.html
```

## Documentation

- Update README.md if your changes affect setup or usage
- Add docstrings to new functions and classes
- Update inline comments for complex logic
- Include examples in docstrings where helpful

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with new features and fixes
3. Create a new release on GitHub
4. Tag the release with semantic versioning (e.g., v1.2.0)

## Questions?

If you have questions about contributing, please:

1. Check the existing documentation
2. Search through existing issues
3. Create a new issue with the "question" label
4. Join our discussions on GitHub Discussions

Thank you for contributing! 🎉
