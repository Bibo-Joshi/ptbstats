#!/usr/bin/env python
"""Module containing several constants."""
from typing import Optional

from telegram.ext import Dispatcher

MIN_INT = int(-10e10)
NEXT_HANDLER_GROUP = MIN_INT
COMMAND_HANDLER_GROUP = 0
BOT_DATA_KEY = 'PTBStats'
DISPATCHER: Optional[Dispatcher] = None
