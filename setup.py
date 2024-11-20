
from setuptools import setup, find_packages

setup(
    name="inventory_management",
    version="0.1",
    author="Charlee Kraiss",
    author_email="charlee.e.kraiss@vanderbilt.com",
    description="A Python package for inventory management, customer tracking, and report generation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CKraiss18/inventory_management.git",  # Optional, add if hosting on GitHub
    packages=find_packages(),  # Automatically finds all packages in the directory
    install_requires=[
        "pandas",  # Add any other dependencies here
    ],
    python_requires='>=3.6',  # Specify your Python version requirement
)
