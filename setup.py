#!/usr/bin/env python3
"""
Setup script for Selenium Python Test Automation Framework.
This script helps with initial project setup and configuration.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_git():
    """Check if Git is installed."""
    success, _, _ = run_command("git --version", check=False)
    if success:
        print("✅ Git is available")
        return True
    else:
        print("❌ Git is not installed or not in PATH")
        return False


def create_virtual_environment():
    """Create a virtual environment."""
    print("\n📦 Creating virtual environment...")
    
    if Path("venv").exists():
        print("Virtual environment already exists")
        return True
    
    success, stdout, stderr = run_command(f"{sys.executable} -m venv venv")
    if success:
        print("✅ Virtual environment created")
        return True
    else:
        print(f"❌ Failed to create virtual environment: {stderr}")
        return False


def get_activation_command():
    """Get the command to activate virtual environment based on OS."""
    if os.name == 'nt':  # Windows
        return "venv\\Scripts\\activate"
    else:  # Unix/Linux/macOS
        return "source venv/bin/activate"


def install_dependencies():
    """Install Python dependencies."""
    print("\n📚 Installing dependencies...")
    
    # Determine pip command based on OS
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip first
    success, _, stderr = run_command(f"{pip_cmd} install --upgrade pip")
    if not success:
        print(f"⚠️  Warning: Could not upgrade pip: {stderr}")
    
    # Install requirements
    success, stdout, stderr = run_command(f"{pip_cmd} install -r requirements.txt")
    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False


def setup_pre_commit():
    """Set up pre-commit hooks."""
    print("\n🔧 Setting up pre-commit hooks...")
    
    if os.name == 'nt':  # Windows
        precommit_cmd = "venv\\Scripts\\pre-commit"
    else:  # Unix/Linux/macOS
        precommit_cmd = "venv/bin/pre-commit"
    
    success, _, stderr = run_command(f"{precommit_cmd} install")
    if success:
        print("✅ Pre-commit hooks installed")
        return True
    else:
        print(f"❌ Failed to install pre-commit hooks: {stderr}")
        return False


def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = [
        "reports/html",
        "reports/allure-results", 
        "logs",
        "screenshots",
        "downloads",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")


def setup_environment_file():
    """Set up environment configuration file."""
    print("\n⚙️  Setting up environment configuration...")
    
    if not Path(".env").exists():
        if Path(".env.example").exists():
            shutil.copy(".env.example", ".env")
            print("✅ Environment file created from template")
            print("📝 Please edit .env file with your configuration")
        else:
            print("❌ .env.example file not found")
            return False
    else:
        print("Environment file already exists")
    
    return True


def run_test_verification():
    """Run a quick test to verify setup."""
    print("\n🧪 Running setup verification...")
    
    if os.name == 'nt':  # Windows
        pytest_cmd = "venv\\Scripts\\pytest"
    else:  # Unix/Linux/macOS
        pytest_cmd = "venv/bin/pytest"
    
    # Run a simple test to verify setup
    success, stdout, stderr = run_command(f"{pytest_cmd} --version", check=False)
    if success:
        print("✅ Pytest is working")
        
        # Try to run a quick smoke test
        print("Running a quick smoke test...")
        success, stdout, stderr = run_command(
            f"{pytest_cmd} tests/ui/test_google_search.py::TestGoogleSearch::test_basic_search -v --headless",
            check=False
        )
        if success:
            print("✅ Smoke test passed - setup is working!")
        else:
            print("⚠️  Smoke test failed, but basic setup is complete")
            print("You may need to configure your environment or check browser drivers")
        
        return True
    else:
        print(f"❌ Pytest verification failed: {stderr}")
        return False


def print_next_steps():
    """Print next steps for the user."""
    activation_cmd = get_activation_command()
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n📋 Next Steps:")
    print(f"1. Activate virtual environment: {activation_cmd}")
    print("2. Edit .env file with your configuration")
    print("3. Run tests: pytest")
    print("4. Run smoke tests: pytest -m smoke")
    print("5. Generate reports: pytest --html=reports/report.html")
    print("\n📚 Useful Commands:")
    print("- make help                 # Show all available commands")
    print("- pytest --help            # Show pytest options")
    print("- pytest -m smoke          # Run smoke tests")
    print("- pytest --browser=firefox # Run with Firefox")
    print("- pytest --headless        # Run in headless mode")
    print("\n📖 Documentation:")
    print("- README.md                # Complete documentation")
    print("- CONTRIBUTING.md          # Contributing guidelines")
    print("- .env file               # Environment configuration")
    print("\n🆘 Need Help?")
    print("- Check README.md for detailed instructions")
    print("- Create an issue on GitHub for support")
    print("="*60)


def main():
    """Main setup function."""
    print("🚀 Selenium Python Test Automation Framework Setup")
    print("="*60)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    check_git()  # Not critical, just informative
    
    # Setup steps
    steps = [
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up pre-commit hooks", setup_pre_commit),
        ("Creating directories", create_directories),
        ("Setting up environment file", setup_environment_file),
        ("Running verification", run_test_verification),
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        try:
            if not step_function():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            failed_steps.append(step_name)
    
    if failed_steps:
        print(f"\n⚠️  Some steps failed: {', '.join(failed_steps)}")
        print("Please check the errors above and run setup again if needed.")
    else:
        print_next_steps()


if __name__ == "__main__":
    main()
