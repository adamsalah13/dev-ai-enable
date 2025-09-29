"""
Setup script for Fintech AI Enable Labs package.
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="fintech-ai-enable",
    version="0.1.0",
    author="Adam Salah",
    author_email="contact@example.com",
    description="A comprehensive Python toolkit for financial technology and AI integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adamsalah13/dev-ai-enable",
    project_urls={
        "Bug Reports": "https://github.com/adamsalah13/dev-ai-enable/issues",
        "Source": "https://github.com/adamsalah13/dev-ai-enable",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "pytest-cov>=3.0.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "ipykernel>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fintech-ai-demo=fintech_ai.examples.basic_usage:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="fintech artificial-intelligence machine-learning finance trading",
)