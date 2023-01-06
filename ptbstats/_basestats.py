#!/usr/bin/env python
"""Base class for storing and displaying statistics."""
from abc import ABC, abstractmethod
from typing import Any, Optional, TypeVar

from telegram import Update
from telegram.ext import Application, BaseHandler, CallbackContext

_CCT = TypeVar("_CCT", bound=CallbackContext)


class BaseStats(BaseHandler[Update, _CCT], ABC):
    """Base class for storing and displaying statistics.

    Warning:
        :attr:`command` must not appear twice between statistics instances!

    Args:
        command: The command that should produce the statistics associated with this instance.
        block_stats: Whether the :meth:`process_update` should be run blocking.
            Defaults to :obj:`True`.
        block_command: Whether :meth:`reply_statistics` should be run blocking.
            Defaults to :obj:`True`.

    Attributes:
        command: The command that produces the statistics associated with this instance.
        block_stats: Whether the :meth:`process_update` should be run blocking.
        block_command: Whether :meth:`reply_statistics` should be run blocking.
    """

    def __new__(cls, *args, **kwargs):  # type: ignore
        instance = super().__new__(cls, *args, **kwargs)
        orig_check_update = instance.check_update

        def check_update(update: Update) -> Optional[bool]:
            return isinstance(update, Update) and orig_check_update(update)

        instance.check_update = check_update
        return instance

    def __init__(self, command: str, block_stats: bool = True, block_command: bool = True):
        super().__init__(callback=self._callback, block=block_stats)
        self.command = command
        self.block_command = block_command

    async def _callback(self, update: Update, context: _CCT) -> None:
        await self.process_update(update)
        self.store_data(context)

    @abstractmethod
    def check_update(self, update: object) -> Optional[bool]:
        """
        This method is called to determine if an update should be processed by this statistics
        instance. It must always be overridden.

        Note:
            You can imitate Filters by this method by something like::

                def check_update(self, update: Update):
                    filters_check = (filters.TEXT | filters.STICKER).check_update(update)
                    return update.effective_message and filters_check

        Args:
            update (:class:`telegram.Update`): The update to be tested.

        Returns:
            Either :obj:`None` or :obj:`False` if the update should not be handled, :obj:`True`
            otherwise.
        """

    @abstractmethod
    async def process_update(self, update: Update) -> None:
        """
        This method is called on every update, that passes :meth:`check_update`. The
        :class:`telegram.ext.CallbackContext` argument is deliberately *not* passed, as this method
        should be independent from it.

        This method must be overridden to update the statistics in an appropriate manner.

        Args:
            update: The :class:`telegram.Update`.

        """

    @abstractmethod
    async def reply_statistics(self, update: Update, context: _CCT) -> None:
        """
        This method will be used as the callback of the :class:`telegram.ext.CommandHandler`
        associated with this statistics instance. It must be overridden to reply with the current
        status of the statistics in an appropriate manner.

        Args:
            update: The :class:`telegram.Update`.
            context: The :class:`telegram.ext.CallbackContext`
        """

    @abstractmethod
    def store_data(self, context: _CCT) -> None:
        """
        Will be called after handling an update. Any data that should be persisted must be stored
        in ``context.bot_data``. If you don't use persistence, just ``pass``.

        Args:
            context (:class:`telegram.ext.CallbackContext`): The callback context
        """

    @abstractmethod
    def load_data(self, application: Application[Any, _CCT, Any, Any, Any, Any]) -> None:
        """
        Will be called on startup to load the data stored by :meth:`store_data` from the
        persistence. If you don't use persistence, just ``pass``.

        Args:
            application (:class:`telegram.ext.Application`): The application that was set via
                :func:`ptbstats.set_application`.
        """
