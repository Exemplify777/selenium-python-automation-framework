#!/usr/bin/env python3
"""
Quick verification script to test the framework setup.
This script performs basic checks to ensure the framework is properly configured.
"""

import importlib
import sys
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"✅ Python {sys.version.split()[0]} - OK")
        return True
    else:
        print(f"❌ Python {sys.version.split()[0]} - Requires 3.8+")
        return False


def check_imports():
    """Check if required packages can be imported."""
    print("\n📦 Checking package imports...")

    required_packages = [
        ("selenium", "Selenium WebDriver"),
        ("selene", "Selene"),
        ("pytest", "Pytest"),
        ("requests", "Requests"),
        ("pydantic", "Pydantic"),
        ("faker", "Faker"),
        ("structlog", "Structlog"),
        ("dotenv", "Python-dotenv"),
        ("PIL", "Pillow"),
        ("allure_pytest", "Allure Pytest"),
    ]

    failed_imports = []

    for package, name in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - FAILED: {e}")
            failed_imports.append(name)

    return len(failed_imports) == 0


def check_framework_structure():
    """Check if framework structure is correct."""
    print("\n🏗️  Checking framework structure...")

    required_paths = [
        "framework/__init__.py",
        "framework/core/__init__.py",
        "framework/core/base_page.py",
        "framework/core/browser_manager.py",
        "framework/config/__init__.py",
        "framework/config/settings.py",
        "framework/pages/__init__.py",
        "framework/utils/__init__.py",
        "framework/utils/helpers.py",
        "framework/utils/logger.py",
        "tests/__init__.py",
        "tests/ui/__init__.py",
        "tests/api/__init__.py",
        "conftest.py",
        "requirements.txt",
        "pytest.ini",
        "pyproject.toml",
    ]

    missing_files = []

    for path in required_paths:
        if Path(path).exists():
            print(f"✅ {path} - OK")
        else:
            print(f"❌ {path} - MISSING")
            missing_files.append(path)

    return len(missing_files) == 0


def check_framework_imports():
    """Check if framework modules can be imported."""
    print("\n🔧 Checking framework imports...")

    framework_modules = [
        ("framework.config.settings", "Settings"),
        ("framework.core.browser_manager", "Browser Manager"),
        ("framework.core.base_page", "Base Page"),
        ("framework.utils.helpers", "Helpers"),
        ("framework.utils.logger", "Logger"),
        ("framework.pages.google_page", "Google Page"),
    ]

    failed_imports = []

    for module, name in framework_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {name} - OK")
        except ImportError as e:
            print(f"❌ {name} - FAILED: {e}")
            failed_imports.append(name)

    return len(failed_imports) == 0


def check_configuration():
    """Check configuration setup."""
    print("\n⚙️  Checking configuration...")

    try:
        from framework.config.settings import config

        print(f"✅ Configuration loaded - OK")
        print(f"   Browser: {config.browser}")
        print(f"   Base URL: {config.base_url}")
        print(f"   Environment: {config.environment}")
        print(f"   Headless: {config.headless}")

        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False


def check_test_data():
    """Check test data files."""
    print("\n📊 Checking test data...")

    test_data_files = [
        "tests/data/test_users.json",
        ".env.example",
    ]

    missing_files = []

    for file_path in test_data_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - OK")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)

    return len(missing_files) == 0


def check_directories():
    """Check required directories."""
    print("\n📁 Checking directories...")

    required_dirs = [
        "reports",
        "reports/html",
        "reports/allure-results",
        "logs",
        "screenshots",
        ".github",
        ".github/workflows",
    ]

    missing_dirs = []

    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/ - OK")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            missing_dirs.append(dir_path)

    return len(missing_dirs) == 0


def test_basic_functionality():
    """Test basic framework functionality."""
    print("\n🧪 Testing basic functionality...")

    try:
        # Test data generation
        from framework.utils.helpers import DataGenerator

        data_gen = DataGenerator()

        email = data_gen.random_email()
        name = data_gen.random_name()

        print(f"✅ Data generation - OK")
        print(f"   Generated email: {email}")
        print(f"   Generated name: {name['first_name']} {name['last_name']}")

        # Test logger
        from framework.utils.logger import get_logger

        logger = get_logger(__name__)
        logger.info("Test log message")
        print(f"✅ Logging - OK")

        # Test configuration
        from framework.config.settings import config

        print(f"✅ Configuration access - OK")

        return True

    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def run_verification():
    """Run all verification checks."""
    print("🚀 Framework Setup Verification")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Package Imports", check_imports),
        ("Framework Structure", check_framework_structure),
        ("Framework Imports", check_framework_imports),
        ("Configuration", check_configuration),
        ("Test Data", check_test_data),
        ("Directories", check_directories),
        ("Basic Functionality", test_basic_functionality),
    ]

    passed_checks = 0
    total_checks = len(checks)

    for check_name, check_function in checks:
        try:
            if check_function():
                passed_checks += 1
        except Exception as e:
            print(f"❌ {check_name} check failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Verification Results: {passed_checks}/{total_checks} checks passed")

    if passed_checks == total_checks:
        print("🎉 All checks passed! Framework is ready to use.")
        print("\n📋 Next steps:")
        print("1. Run: pytest --version")
        print(
            "2. Run: pytest tests/ui/test_google_search.py::TestGoogleSearch::test_basic_search -v"
        )
        print("3. Run: make test-smoke")
        return True
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print("\n🔧 Troubleshooting:")
        print(
            "1. Make sure all dependencies are installed: pip install -r requirements.txt"
        )
        print("2. Check that all files are present")
        print("3. Verify Python version is 3.8+")
        return False


if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
