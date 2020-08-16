#!/usr/bin/env python
"""Module containing some implementations of :class:`ptbstats.BaseStats`."""
import datetime as dtm
import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tempfile import TemporaryDirectory
from collections import defaultdict
from typing import Optional, Dict, Any, Callable, Generator, Set

from telegram import Update, ChatAction
from telegram.ext import CallbackContext

from ptbstats import BaseStats


class Record:

    def __init__(self) -> None:
        self.user_ids: Set[int] = set()
        self.queries = 0


class SimpleStats(BaseStats):
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
        self.records: Dict[dtm.date, Record] = defaultdict(Record)
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
        self.records[today].user_ids.add(update.effective_user.id)
        self.records[today].queries += 1

    def reply_statistics(self, update: Update, context: CallbackContext) -> None:
        """
        Sends one PDF-file with the two graphs of number of users per day and number of queries per
        day as reply.

        Args:
            update: The :class:`telegram.Update`.
            context: The :class:`telegram.ext.CallbackContext`
        """

        def date_range(date1: dtm.date, date2: dtm.date) -> Generator[dtm.date, None, None]:
            for n in range(int((date2 - date1).days) + 1):
                yield date1 + dtm.timedelta(n)

        if not (self.records and [bool(d) for d in self.records.values()]):
            update.effective_message.reply_text('No data to show.')
            return

        # Send ChatAction, as file generation takes a moment
        update.effective_chat.send_action(ChatAction.UPLOAD_DOCUMENT)

        # Fill gaps in records with zeros
        dates = list(self.records.keys())
        for d in date_range(min(dates), max(dates)):
            assert isinstance(self.records[d], Record)
        self.records = dict(sorted(self.records.items()))

        dates = list(self.records.keys())
        number_users = [len(r.user_ids) for r in self.records.values()]
        number_queries = [r.queries for r in self.records.values()]

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=dates, y=number_users, name='Users'),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=dates, y=number_queries, name='Queries'),
            secondary_y=True,
        )

        # Set y-axes titles
        fig.update_yaxes(title_text='Number of different users', secondary_y=False)
        fig.update_yaxes(title_text='Number of received queries', secondary_y=True)

        # Save and send the file
        with TemporaryDirectory() as dir:
            filename = os.path.join(dir, f'{self.command}.pdf')
            fig.write_image(filename)

            update.effective_message.reply_document(open(filename, 'rb'))

    def persistent_data(self) -> Dict[str, Any]:
        """
        Persists :attr:`records`.

        Returns:
            Dict[:obj:`str`, Any]
        """
        return {'records': self.records}
