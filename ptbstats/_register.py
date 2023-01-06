#!/usr/bin/env python
"""Module providing the :meth:`register_stats` method."""
from typing import Sequence, Union

from telegram.ext import Application, CommandHandler, filters

from ptbstats import BaseStats, _constants


def set_application(application: Application) -> None:
    """
    Set the application to be used with ``ptbstats``.

    Args:
        application: The :class:`telegram.ext.Application`.
    """
    _constants.APPLICATION = application


def register_stats(
    stats: BaseStats,
    admin_id: Union[int, Sequence[int]] = None,
    stats_group: int = None,
    command_group: int = None,
) -> None:
    """
    Register a statistics instance. This will register two handlers on the application set with
    :meth:`set_application`:

    1. The ``stats`` handler. By default, each of those handlers will get it's own group,
       starting with -10e10. That should be enough to not interfere with your other handlers.
    2. A :class:`telegram.ext.CommandHandler` that will listen for ``command`` and call
       ``stats.reply_statistics`` to report the current statistics. By default, all those
       command handlers will be added to group 0. If you register the statistics before your other
       handlers, that should usually be enough to make sure that the command will not be caught by
       other handlers.

    Moreover, makes sure hat persisted data is loaded into the statistics instances.

    Args:
        stats: The statistics instance to be added.
        admin_id: Optional. If passed, only the admin/s with the corresponding user ids will be
            allowed to query the statistics.
        stats_group: Optional. The group to register the statistics handler to instead of the
            default.
        command_group: Optional. The group te register the command handler to instead of the
            default.

    """
    if _constants.APPLICATION is None:
        raise RuntimeError(
            "You must set the application with `set_application` before calling `register_stats`!"
        )

    # Get persisted data
    stats.load_data(_constants.APPLICATION)

    # Register stats handler
    if stats_group is None:
        _constants.APPLICATION.add_handler(stats, group=_constants.NEXT_HANDLER_GROUP)
        _constants.NEXT_HANDLER_GROUP += 1
    else:
        _constants.APPLICATION.add_handler(stats, group=stats_group)

    # Register command Handler
    handler = CommandHandler(
        command=stats.command,
        callback=stats.reply_statistics,
        filters=filters.User(user_id=admin_id) if admin_id else None,
        block=stats.block_command,
    )
    _constants.APPLICATION.add_handler(
        handler, group=command_group or _constants.COMMAND_HANDLER_GROUP
    )
