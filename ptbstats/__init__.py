#!/usr/bin/env python
"""A library that provides a Python interface to the Telegram Bot API"""

from .version import __version__  # noqa: F401

__author__ = 'ptbstats@mahlerhome.de'

from .basestats import BaseStats
from .simplestats import SimpleStats
from .register import set_dispatcher, register_stats

__all__ = ['BaseStats', 'SimpleStats', 'set_dispatcher', 'register_stats']
