# Makefile for Fintech AI Enable Labs

.PHONY: help install test clean lint format run-example jupyter docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install the package and dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean up build artifacts"
	@echo "  run-example - Run the basic usage example"
	@echo "  jupyter     - Start Jupyter notebook server"
	@echo "  docs        - Generate documentation (future)"

# Install package and dependencies
install:
	pip install -r requirements.txt
	pip install -e .

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# Run tests
test:
	python -m pytest tests/ -v

# Run tests with coverage
test-cov:
	python -m pytest tests/ --cov=fintech_ai --cov-report=html --cov-report=term

# Lint code
lint:
	flake8 src/ tests/ examples/ --max-line-length=88 --extend-ignore=E203

# Format code
format:
	black src/ tests/ examples/

# Clean up build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run basic example
run-example:
	cd examples && python basic_usage.py

# Start Jupyter notebook
jupyter:
	jupyter notebook notebooks/

# Build package
build:
	python setup.py sdist bdist_wheel

# Install in development mode
dev-install:
	pip install -e ".[dev,notebooks]"

# Run all checks (format, lint, test)
check: format lint test

# Setup development environment
setup-dev: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make check' to verify everything works."