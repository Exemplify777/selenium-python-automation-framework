# 🚀 Template Usage Guide

## Creating Your Project from This Template

### 1. **Create Repository from Template**

1. Click the **"Use this template"** button on the main repository page
2. Choose **"Create a new repository"**
3. Fill in your repository details:
   - **Repository name**: `your-project-name`
   - **Description**: Your project description
   - **Visibility**: Public or Private
4. Click **"Create repository from template"**

### 2. **Clone Your New Repository**

```bash
git clone https://github.com/Exemplify777/your-project-name.git
cd your-project-name
```

### 3. **Initial Setup**

```bash
# Run the automated setup script
python setup.py

# Or manual setup:
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Run verification
python verify_setup.py
```

### 4. **Customize for Your Project**

#### **Update Configuration**
Edit `.env` file with your settings:
```bash
# Your application URL
BASE_URL=https://your-app.com

# Your preferred browser
BROWSER=chrome

# Your environment
ENVIRONMENT=staging
```

#### **Update Project Information**
The template cleanup workflow automatically updates most references, but you may want to customize:

1. **pyproject.toml**: Update project name, description, and author
2. **README.md**: Add your project-specific information
3. **Test data**: Update `tests/data/test_users.json` with your test data

#### **Add Your Page Objects**
1. Create page objects in `framework/pages/` for your application
2. Follow the examples in `google_page.py` and `example_form_page.py`
3. Use the `BasePage` class as your foundation

#### **Write Your Tests**
1. Add UI tests in `tests/ui/`
2. Add API tests in `tests/api/`
3. Use the existing examples as templates
4. Follow the established patterns and conventions

### 5. **Verify Everything Works**

```bash
# Run verification script
python verify_setup.py

# Run example tests
pytest tests/api/ -v

# Run with reporting
pytest --html=reports/report.html --alluredir=reports/allure-results
```

### 6. **Set Up CI/CD**

The GitHub Actions workflow is already configured and will run automatically when you:
- Push to main branch
- Create pull requests
- Run on schedule (daily)

You can customize the workflow in `.github/workflows/test-automation.yml`

### 7. **Customize GitHub Repository Settings**

#### **Enable Features**
- Go to Settings > General
- Enable Issues, Discussions
- Disable Wiki (documentation is in README)

#### **Set Up Branch Protection**
- Go to Settings > Branches
- Add protection rule for `main` branch
- Require pull request reviews
- Require status checks

#### **Configure Secrets** (if needed)
- Go to Settings > Secrets and variables > Actions
- Add any required secrets (API keys, credentials, etc.)

### 8. **Optional Enhancements**

#### **GitHub Pages for Reports**
If you want to publish Allure reports:
1. Go to Settings > Pages
2. Source: GitHub Actions
3. The workflow will automatically deploy reports

#### **Dependabot**
Already configured in `.github/dependabot.yml` for automatic dependency updates.

#### **Code Scanning**
Enable CodeQL in Settings > Security for automated security scanning.

## 📋 **Checklist for New Projects**

- [ ] Repository created from template
- [ ] Cloned locally
- [ ] Setup script executed successfully
- [ ] `.env` file configured
- [ ] Verification script passes
- [ ] Project information updated
- [ ] First custom page object created
- [ ] First custom test written
- [ ] CI/CD pipeline tested
- [ ] Repository settings configured

## 🆘 **Need Help?**

- **Documentation**: Check the comprehensive README.md
- **Examples**: Look at existing page objects and tests
- **Issues**: Create an issue in the original template repository
- **Discussions**: Use GitHub Discussions for questions

## 🎉 **You're Ready!**

Your test automation framework is now set up and ready for development. Start by:

1. Writing page objects for your application
2. Creating test cases for your key user journeys
3. Setting up test data for your scenarios
4. Customizing the CI/CD pipeline for your needs

Happy testing! 🚀
