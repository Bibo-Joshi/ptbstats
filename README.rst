PTB Stats
=========

.. image:: https://img.shields.io/badge/python-3.7+-blue
   :target: https://www.python.org/doc/versions/
   :alt: Supported Python versions

.. image:: https://img.shields.io/badge/python--telegram--bot->%3D13.0%2C<14.0-blue
   :target: https://python-telegram-bot.org/
   :alt: Supported PTB versions

.. image:: https://img.shields.io/badge/documentation-is%20here-orange
   :target: https://hirschheissich.gitlab.io/ptbstats/
   :alt: Documentation

A simple statistics plugin for Telegram bots build with the python-telegram-bot library

Installation
------------

Install via::

    pip install git+https://gitlab.com/HirschHeissIch/ptbstats.git@v1.3.1

``ptbstats`` does not have a proper package (yet), because the author is too lazy for unittests and stuff …

Quickstart
----------

Here is an example setup using the very basic `SimpleStats <https://hirschheissich.gitlab.io/ptbstats/ptbstats.simplestats.html>`_ statistics instance delivered along with ``ptbstats``.

.. code-block:: python

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    from telegram.ext import Updater, PicklePersistence, Filters
    from ptbstats import set_dispatcher, register_stats, SimpleStats

    def main():
        """Start the bot."""
        persistence = PicklePersistence('persistence.pickle')
        updater = Updater("TOKEN", use_context=True, persistence=persistence)

        # Set up stats
        set_dispatcher(updater.dispatcher)
        # Count number of text messages
        register_stats(SimpleStats('text', lambda u: bool(u.message and
                                                          (Filters.text & ~ Filters.command)(u))))
        # Count number of inline queries
        register_stats(SimpleStats('ilq', lambda u: bool(u.inline_query and u.inline_query.query)))

        # Register handlers
        updater.dispatcher.add_handler(ExampleHandler)

        # Start the Bot
        updater.start_polling()
        updater.idle()


    if __name__ == '__main__':
        main()

Advanced Usage
--------------

To create your own, customized statistics, subclass `BaseStats <https://hirschheissich.gitlab.io/ptbstats/ptbstats.basestats.html>`_.
