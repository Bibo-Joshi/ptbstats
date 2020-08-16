#!/usr/bin/env python
"""Module containing some implementations of :class:`ptbstats.BaseStats`."""
import datetime as dtm
from tempfile import NamedTemporaryFile

import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import Optional, Dict, Any, Callable

from telegram import Update
from telegram.ext import CallbackContext

from ptbstats import BaseStats


class UserDayStats(BaseStats):
    """Simple implementation of :class:`ptbstats.BaseStats` collecting records per day and user.

    Attributes:
        command: The command that produces the statistics associated with this instance.
        records: For each :class:`datetime.date`, the dict value is a dict, containing for each
            user the number of recorded inline queries.


    Args:
        command: The command that should produce the statistics associated with this instance.
        check_update: A callable that determines, if an update should be handled or not. See
            :meth:`ptbstats.BaseStats.check_update` for the details.
    """

    def __init__(self, command: str, check_update: Callable[[Update], Optional[bool]]) -> None:
        super().__init__(command=command)
        self.records: Dict[dtm.date, Dict[int, int]] = defaultdict(lambda: defaultdict(int))
        self._check_update = check_update

    def check_update(self, update: Update) -> Optional[bool]:
        return bool(self._check_update(update))

    def process_update(self, update: Update) -> None:
        """
        Counts the number of inline queries per user and day.

        Args:
            update: The :class:`telegram.Update`.

        """
        today = dtm.date.today()
        self.records[today][update.effective_user.id] += 1

    def reply_statistics(self, update: Update, context: CallbackContext) -> None:
        """
        Sends one picture with the two graphs of number of users per day and number of queries per
        day as reply.

        Args:
            update: The :class:`telegram.Update`.
            context: The :class:`telegram.ext.CallbackContext`
        """
        dates = matplotlib.dates.date2num(self.records.keys())
        number_users = [len(d) for d in self.records.values()]
        number_queries = [sum(d.values()) for d in self.records.values()]

        if not all([dates, number_users, number_queries]):
            update.effective_message.reply_text('No data to show.')
            return

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('date')
        ax1.set_ylabel('Number of different users', color=color)
        ax1.plot_date(dates, number_users, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('Number of InlineQueries', color=color)
        ax2.plot(dates, number_queries, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        with NamedTemporaryFile(suffix='.png', delete=False) as file:
            fig.savefig(file.name)
            file.close()

            update.effective_message.reply_photo(open(file.name, 'rb'))

    def persistent_data(self) -> Dict[str, Any]:
        """
        Persists :attr:`records`.

        Returns:
            Dict[:obj:`str`, Any]
        """
        return {'records': self.records}
