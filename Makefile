# Makefile for Selenium Python Test Automation Framework

.PHONY: help install install-dev setup test test-ui test-api test-smoke test-parallel clean lint format type-check security-scan reports serve-allure docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install          Install production dependencies"
	@echo "  install-dev      Install development dependencies"
	@echo "  setup            Complete project setup"
	@echo "  test             Run all tests"
	@echo "  test-ui          Run UI tests only"
	@echo "  test-api         Run API tests only"
	@echo "  test-smoke       Run smoke tests only"
	@echo "  test-parallel    Run tests in parallel"
	@echo "  lint             Run all linting checks"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run mypy type checking"
	@echo "  security-scan    Run security scan with bandit"
	@echo "  reports          Generate test reports"
	@echo "  serve-allure     Serve Allure reports"
	@echo "  clean            Clean up generated files"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run tests in Docker container"

# Installation
install:
	pip install -r requirements.txt

install-dev: install
	pip install pre-commit
	pre-commit install

setup: install-dev
	mkdir -p reports/html reports/allure-results logs screenshots
	cp .env.example .env
	@echo "Setup complete! Edit .env file with your configuration."

# Testing
test:
	pytest

test-ui:
	pytest tests/ui/ -v

test-api:
	pytest tests/api/ -v

test-smoke:
	pytest -m smoke -v

test-parallel:
	pytest -n 4 --dist=loadfile

test-headless:
	pytest --headless

test-chrome:
	pytest --browser=chrome

test-firefox:
	pytest --browser=firefox

test-edge:
	pytest --browser=edge

# Code Quality
lint: 
	flake8 .
	black --check .
	isort --check-only .

format:
	black .
	isort .

type-check:
	mypy framework/ --ignore-missing-imports

security-scan:
	bandit -r framework/ -f json -o reports/bandit-report.json

pre-commit:
	pre-commit run --all-files

# Reporting
reports:
	pytest --html=reports/html/report.html --self-contained-html --alluredir=reports/allure-results

serve-allure:
	allure serve reports/allure-results

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf reports/html/*
	rm -rf reports/allure-results/*
	rm -rf logs/*
	rm -rf screenshots/*

# Docker
docker-build:
	docker build -t selenium-python-framework .

docker-run:
	docker run --rm -v $(PWD)/reports:/app/reports selenium-python-framework

# Development helpers
dev-setup: setup
	@echo "Development environment ready!"
	@echo "Run 'make test-smoke' to verify setup"

quick-test:
	pytest tests/ui/test_google_search.py::TestGoogleSearch::test_basic_search -v

debug-test:
	pytest tests/ui/test_google_search.py::TestGoogleSearch::test_basic_search -v -s --pdb

# CI/CD helpers
ci-test:
	pytest --headless --browser=chrome --html=reports/html/ci-report.html --alluredir=reports/allure-results

ci-lint:
	black --check .
	isort --check-only .
	flake8 .
	mypy framework/ --ignore-missing-imports
