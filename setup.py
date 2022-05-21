#!/usr/bin/env python
"""The setup and build script for the ptbstats library."""

import codecs
import os

from setuptools import setup, find_packages


def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as requirements:
        for install in requirements:
            requirements_list.append(install.strip())

    return requirements_list


packages = find_packages(exclude=['tests*'])
requirements = requirements()

with codecs.open('README.rst', 'r', 'utf-8') as fd:
    fn = os.path.join('ptbstats', 'version.py')
    with open(fn) as fh:
        code = compile(fh.read(), fn, 'exec')
        exec(code)

    setup(name='ptbstats',
          version=__version__,  # noqa: F821
          author='Hinrich Mahler',
          author_email='ptbstats@mahlerhome.de',
          url='https://Bibo-Joshi.github.io/ptbstats/',
          keywords='python-telegram-bot statistics plugin',
          description="A simple statistics plugin for Telegram bots build with the "
                      "python-telegram-bot library",
          long_description=fd.read(),
          packages=packages,
          install_requires=requirements,
          include_package_data=True,)
