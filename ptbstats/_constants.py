#!/usr/bin/env python
"""Module containing several constants."""
from typing import Optional

from telegram.ext import Application

MIN_INT = int(-10e10)
NEXT_HANDLER_GROUP = MIN_INT
COMMAND_HANDLER_GROUP = 0
APPLICATION: Optional[Application] = None
