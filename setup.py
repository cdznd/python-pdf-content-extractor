from setuptools import setup, find_packages

setup(
    name="pdf-extractor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF", # runtime dependencies
    ],
    entry_points={
        "console_scripts": [
            "pdf-extractor=pdf_extractor.cli.commands:main",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for extracting text content from PDF files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cdznd/python-pdf-content-extractor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
    ],
) 