"""
Setup script for ClickCheck API Python package
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="clickcheck",
    version="1.0.0",
    author="ClickCheck AI",
    author_email="support@getclickcheck.com",
    description="Official Python SDK for ClickCheck AI API - Analyze website privacy and security risks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ottili-ONE/clickcheck",
    project_urls={
        "Documentation": "https://docs.getclickcheck.com",
        "Source": "https://github.com/Ottili-ONE/clickcheck",
        "Website": "https://getclickcheck.com",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    keywords="clickcheck, security, privacy, api, sdk, website, analysis",
)

