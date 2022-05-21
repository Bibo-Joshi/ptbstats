#!/usr/bin/env python
"""A library that provides a Python interface to the Telegram Bot API"""

__author__ = "ptbstats@mahlerhome.de"
__all__ = ["BaseStats", "SimpleStats", "set_application", "register_stats"]

from ._basestats import BaseStats
from ._register import register_stats, set_application
from ._simplestats import SimpleStats
