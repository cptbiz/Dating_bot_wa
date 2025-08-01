#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script для WhatsApp бота BeHappy2Day
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dating-wa-bot",
    version="1.0.0",
    author="BeHappy2Day Team",
    author_email="polovinka@behappy2day.com",
    description="WhatsApp Bot для привлечения лидов на сайт знакомств BeHappy2Day",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cptbiz/Dating_bot_wa",
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
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dating-wa-bot=app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 