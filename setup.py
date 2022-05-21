#!/usr/bin/env python
"""The setup and build script for the ptbstats library."""

from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def requirements() -> List[str]:
    """Build the requirements list for this project"""
    requirements_list = []

    with open("requirements.txt") as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


packages = find_packages(exclude=["tests*"])
requirements = requirements()

setup(
    name="ptbstats",
    version="2.0",
    author="Hinrich Mahler",
    author_email="ptbstats@mahlerhome.de",
    url="https://Bibo-Joshi.github.io/ptbstats/",
    keywords="python-telegram-bot statistics plugin",
    description="A simple statistics plugin for Telegram bots build with the "
    "python-telegram-bot library",
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    packages=packages,
    install_requires=requirements,
    include_package_data=True,
)
