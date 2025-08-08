from setuptools import setup, find_packages

setup(
    name="iso20022_rag",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
    ],
    author="Shivani Gade",
    author_email="gadeshivani@gmail.com",
    description="An Adaptive Multi-RAG Architecture for Financial Message Processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gadeshivani/iso20022_rag",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    copyright="Copyright (c) 2025 Shivani Gade"
) 