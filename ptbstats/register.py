#!/usr/bin/env python
"""Module providing the :meth:`register_stats` method."""
from collections import defaultdict
from typing import Union, List
from telegram.ext import Dispatcher, Filters, CommandHandler

from ptbstats import BaseStats, constants


def set_dispatcher(dispatcher: Dispatcher) -> None:
    """
    Set the dispatcher to be used with ``ptbstats``.

    Args:
        dispatcher: The :class:`telegram.ext.Dispatcher``
    """
    constants.DISPATCHER = dispatcher


def register_stats(stats: BaseStats,
                   admin_id: Union[int, List[int]] = None,
                   stats_group: int = None,
                   command_group: int = None) -> None:
    """
    Register a statistics instance. This will register two handlers on the dispatcher set with
    :meth:`set_dispatcher`:

    1. The :attr:`stats` handler. By default, each of those handlers will get it's own group,
        starting with -10e10. That should be enough to not interfere with your other handlers.
    2. A :class:`telegram.ext.CommandHandler` that will listen for :attr:`command` and call
       :meth:`stats.reply_statistics` to report the current statistics. By default, all those
       command handlers will be added to group 0. If you register the statsistics before your other
       handlers, that should usually be enough to make sure that the command will not be catched by
       other handlers.

    Moreover, makes sure hat persisted data is loaded into the statistics instances. To store that
    data, ``dispatcher.bot_data['PTBStats']`` is used and will be assumed not to be occupied by
    other data.

    Args:
        stats: The statistics instance to be added.
        admin_id: Optional. If passed, only the admin/s with the corresponding user ids will be
            allowed to query the statistics.
        stats_group: Optional. The group to register the statistics handler to instead of the
            default.
        command_group: Optional. The group te register the command handler to instead of the
            default.

    Returns:

    """
    if constants.DISPATCHER is None:
        raise RuntimeError('You must set the dispatcher with set_dispatcher before calling '
                           'register_stats!')

    # Get persisted data
    bot_data = constants.DISPATCHER.bot_data
    if not bot_data.get(constants.BOT_DATA_KEY):
        bot_data[constants.BOT_DATA_KEY] = defaultdict(dict)
    stats.apply_persistent_data(bot_data[constants.BOT_DATA_KEY][stats.command])

    # Register stats handler
    if stats_group is None:
        constants.DISPATCHER.add_handler(stats, group=constants.NEXT_HANDLER_GROUP)
        constants.NEXT_HANDLER_GROUP += 1
    else:
        constants.DISPATCHER.add_handler(stats, group=stats_group)

    # Register command Handler
    filters = Filters.user(user_id=admin_id) if admin_id else None
    handler = CommandHandler(stats.command, stats.reply_statistics, filters=filters)
    constants.DISPATCHER.add_handler(handler,
                                     group=command_group or constants.COMMAND_HANDLER_GROUP)
