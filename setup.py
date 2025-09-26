"""
Setup configuration for LNA Bot package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else ""

setup(
    name="lna-bot",
    version="1.0.0",
    author="LNA Development Team",
    author_email="lna-team@example.com",
    description="AI-Powered Learning Need Analysis Bot for Training Recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/lna-bot",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Education :: Training",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "click>=8.0.0",
        "rich>=12.0.0",
        "pydantic>=1.10.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lna-bot=lna_bot.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)