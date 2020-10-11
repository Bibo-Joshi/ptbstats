#!/usr/bin/env python
"""Base class for storing and displaying statistics."""
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional, Dict, Any

from telegram import Update
from telegram.ext import CallbackContext, Handler

from ptbstats import constants


class BaseStats(Handler, ABC):
    """Base class for storing and displaying statistics.

    Attributes:
        command: The command that produces the statistics associated with this instance.
        async_command: Whether :meth:`reply_statistics` should be run asynchronously using
            :meth:`telegram.ext.Disptacher.run_async`.

    Args:
        command: The command that should produce the statistics associated with this instance.
        async_stats: Whether the :meth:`process_update` should be run asynchronously using
            :meth:`telegram.ext.Disptacher.run_async`. Defaults to :obj:`False`.
        async_command: Whether :meth:`reply_statistics` should be run asynchronously using
            :meth:`telegram.ext.Disptacher.run_async`. Defaults to :obj:`False`.

    Warning:
        :attr:`command` must not appear twice between statistics instances!
    """

    def __new__(cls, *args, **kwargs):  # type: ignore
        instance = super().__new__(cls)
        orig_check_update = instance.check_update

        def check_update(update: Update) -> Optional[bool]:
            return isinstance(update, Update) and orig_check_update(update)

        instance.check_update = check_update
        return instance

    def __init__(self, command: str, async_stats: bool = False, async_command: bool = False):
        super().__init__(callback=self._callback, run_async=async_stats)
        self.command = command
        self.async_command = async_command

    @abstractmethod
    def check_update(self, update: Update) -> Optional[bool]:
        """
        This method is called to determine if an update should be processed by this statistics
        instance. It must always be overridden.

        Note:
            You can imitate Filters by this method by something like::

                def check_update(self, update: Update):
                    return update.effective_message and (Filters.text | Filters.sticker)(update)

        Args:
            update (:class:`telegram.Update`): The update to be tested.

        Returns:
            Either :obj:`None` or :obj:`False` if the update should not be handled, :obj:`True`
            otherwise.
        """

    @abstractmethod
    def process_update(self, update: Update) -> None:
        """
        This method is called on every update, that passes :meth:`check_update`. The
        :class:`telegram.ext.CallbackContext` argument is deliberately *not* passed, as this method
        should be independent from it.

        This method must be overridden to update the statistics in an appropriate manner.

        Args:
            update: The :class:`telegram.Update`.

        """

    @abstractmethod
    def reply_statistics(self, update: Update, context: CallbackContext) -> None:
        """
        This method will be used as the callback of the :class:`telegram.ext.CommandHandler`
        associated with this statistics instance. It must be overridden to reply with the current
        status of the statistics in an appropriate manner.

        Args:
            update: The :class:`telegram.Update`.
            context: The :class:`telegram.ext.CallbackContext`
        """

    def persistent_data(self) -> Dict[str, Any]:
        """
        In order to make statistics instances persistent, you will have to do two things:

        1. Use persistence with your PTB setup
        2. Override this method.

        Warning:
            ptbstats uses stores data in ``bot_data['PTBStats']``. Do not store any other data
            there.

        Returns:
            Dict[:obj:`str`, Any]: Dictionary of attributes that are to be persisted. On reboot,
            this instances ``__dict__`` will be merged with this return value.
        """
        return {}

    def _callback(self, update: Update, context: CallbackContext) -> None:
        self.process_update(update)

        if not context.bot_data.get(constants.BOT_DATA_KEY):
            context.bot_data[constants.BOT_DATA_KEY] = defaultdict(dict)

        context.bot_data[constants.BOT_DATA_KEY][self.command].update(self.persistent_data())

    def apply_persistent_data(self, data: Dict[str, Any]) -> None:
        self.__dict__.update(data)
