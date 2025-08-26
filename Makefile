.PHONY: help install install-dev test test-cov lint format clean docs build publish

# Default target
help:
	@echo "StoryMode Development Commands"
	@echo "=============================="
	@echo ""
	@echo "Installation:"
	@echo "  install      Install package in development mode"
	@echo "  install-dev  Install package with development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint         Run linters (flake8, mypy)"
	@echo "  format       Format code (black, isort)"
	@echo ""
	@echo "Documentation:"
	@echo "  docs         Build documentation"
	@echo ""
	@echo "Build & Publish:"
	@echo "  build        Build package"
	@echo "  clean        Clean build artifacts"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=storymode --cov-report=html --cov-report=term-missing

# Code Quality
lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

# Documentation
docs:
	cd docs && make html

# Build & Publish
build:
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf src/*.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Development helpers
check: format lint test

pre-commit: format lint

# Model testing
test-models:
	python -m storymode list-models

# Quick extraction test
test-extract:
	python -m storymode extract --help

# Environment setup
setup-env:
	conda env create -f environment.yml
	conda activate storymode
	pip install -e ".[dev]"
	pre-commit install

# Windows-specific commands
install-dev-windows:
	pip install -e ".[dev]"
	pre-commit install

test-windows:
	python -m pytest tests/ -v

format-windows:
	python -m black src/ tests/
	python -m isort src/ tests/

lint-windows:
	python -m flake8 src/ tests/
	python -m mypy src/

