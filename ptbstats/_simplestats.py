#!/usr/bin/env python
"""Module containing some implementations of :class:`ptbstats.BaseStats`."""
import asyncio
import datetime as dtm
from dataclasses import dataclass, field
from io import StringIO
from typing import Any, Callable, Dict, Generator, Optional, Set, TypeVar

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CallbackContext

from ptbstats import BaseStats

_CCT = TypeVar("_CCT", bound=CallbackContext)


@dataclass
class _Record:
    user_ids: Set[int] = field(default_factory=set)
    queries: int = 0


class SimpleStats(BaseStats[_CCT]):
    """Simple implementation of :class:`ptbstats.BaseStats` collecting records per day and user.
    The command callback will run non-blocking.

    Args:
        command: The command that should produce the statistics associated with this instance.
        check_update: A callable that determines, if an update should be handled or not. See
            :meth:`ptbstats.BaseStats.check_update` for the details.

    Attributes:
        command: The command that produces the statistics associated with this instance.
        records: For each :class:`datetime.date`, the dict value is an object with two attributes
            ``user_ids`` and ``queries``. ``user_ids`` is a set of all user ids that where recorded
            on that day. ``queries`` is the total amount of recorded queries on that day.
    """

    def __init__(self, command: str, check_update: Callable[[object], Optional[bool]]) -> None:
        super().__init__(command=command, block_command=False)
        self.records: Dict[dtm.date, _Record] = {}
        self._check_update = check_update
        self._last_filled: Optional[dtm.date] = None

    def check_update(self, update: object) -> Optional[bool]:
        """See :meth:`ptbstats.BaseStats.check_update`."""
        return bool(self._check_update(update))

    @staticmethod
    def _date_range(date1: dtm.date, date2: dtm.date) -> Generator[dtm.date, None, None]:
        for number in range(int((date2 - date1).days) + 1):
            yield date1 + dtm.timedelta(number)

    def _fill(self) -> None:
        """Fills empty dates since the last record with zeros."""
        today = dtm.date.today()
        if self._last_filled is not None and today <= self._last_filled:
            return

        if not self.records:
            self.records[today] = _Record()

        # Fill gaps in records with zeros
        dates = list(self.records.keys())
        for date in self._date_range(dates[-1], today):
            if date not in self.records:
                self.records[date] = _Record()

        self._last_filled = today

    async def process_update(self, update: Update) -> None:
        """
        Records the update.

        Args:
            update: The :class:`telegram.Update`.
        """
        self._fill()
        today = dtm.date.today()
        self.records[today].user_ids.add(update.effective_user.id)  # type: ignore[union-attr]
        self.records[today].queries += 1

    async def reply_statistics(self, update: Update, context: CallbackContext) -> None:
        """
        Sends one HTML-file with the two graphs of number of users per day and number of queries
        per day as reply.

        Args:
            update: The :class:`telegram.Update`.
            context: The :class:`telegram.ext.CallbackContext`
        """
        task = context.application.create_task(self._reply_statistics(update), update=update)
        while not task.done():
            # Keep sending the chat action as long as the task is not completed
            await update.effective_chat.send_action(  # type: ignore[union-attr]
                ChatAction.UPLOAD_DOCUMENT
            )
            try:
                await asyncio.wait_for(task, 4.5)
            except asyncio.TimeoutError:
                pass

    async def _reply_statistics(self, update: Update) -> None:
        self._fill()

        if not (self.records and all(self.records.values())):
            await update.effective_message.reply_text(  # type: ignore[union-attr]
                "No data to show."
            )
            return

        # get the data
        dates = list(self.records.keys())
        number_users = list(len(r.user_ids) for r in self.records.values())
        number_queries = list(r.queries for r in self.records.values())

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=dates, y=number_users, name="Users"),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=dates, y=number_queries, name="Queries"),
            secondary_y=True,
        )

        # Set y-axes titles
        fig.update_yaxes(title_text="Number of different users", secondary_y=False)
        fig.update_yaxes(title_text="Number of received queries", secondary_y=True)

        # Save and send the file
        stream = StringIO()
        fig.write_html(stream)
        stream.seek(0)

        await update.effective_message.reply_document(  # type: ignore[union-attr]
            stream.read().encode("utf-8"), filename=f"{self.command}.html"
        )

    def store_data(self, context: _CCT) -> None:
        """Persists :attr:`records`.
        Assumes that ``context.bot_data`` is a dict and stores the data in
        ``context.bot_data['SimpleStats']``. Override to customize the behavior.
        """
        context.bot_data["SimpleStats"] = self.records

    def load_data(self, application: Application[Any, _CCT, Any, Any, Any, Any]) -> None:
        """Loads the data stored by :meth:`store_data`.
        Assumes that ``context.bot_data`` is a dict and loads the data from
        ``application.bot_data['SimpleStats']``. Override to customize the behavior.
        """
        if "SimpleStats" in application.bot_data:
            self.records = application.bot_data["SimpleStats"]
