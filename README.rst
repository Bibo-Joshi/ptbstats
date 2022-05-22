PTB Stats
=========

.. image:: https://img.shields.io/badge/python-3.7+-blue
   :target: https://www.python.org/doc/versions/
   :alt: Supported Python versions

.. image:: https://img.shields.io/badge/python--telegram--bot-20.0a0-blue
   :target: https://python-telegram-bot.org/
   :alt: Supported PTB versions

.. image:: https://img.shields.io/badge/documentation-is%20here-orange
   :target: https://Bibo-Joshi.github.io/ptbstats/
   :alt: Documentation

.. image:: https://results.pre-commit.ci/badge/github/Bibo-Joshi/ptbstats/master.svg
   :target: https://results.pre-commit.ci/latest/github/Bibo-Joshi/ptbstats/master
   :alt: pre-commit.ci status

A simple statistics plugin for Telegram bots build with the python-telegram-bot library

Installation
------------

Install via::

    pip install git+https://github.com/Bibo-Joshi/ptbstats.git@v2.0.1

``ptbstats`` does not have a proper package (yet), because the author is too lazy for unittests and stuff …

Quickstart
----------

Here is an example setup using the very basic `SimpleStats <https://Bibo-Joshi.github.io/ptbstats/ptbstats.simplestats.html>`_ statistics instance delivered along with ``ptbstats``.

.. code-block:: python

    #!/usr/bin/env python3
    from telegram.ext import Application, PicklePersistence, filters, MessageHandler
    from ptbstats import set_application, register_stats, SimpleStats


    def main():
        """Start the bot."""
        persistence = PicklePersistence("persistence.pickle")
        application = Application.builder().token("TOKEN").persistence(persistence).build()

        # Set up stats
        set_application(application)
        # Count number of text messages
        register_stats(
            SimpleStats(
                "text", lambda u: bool(u.message and (filters.TEXT & ~filters.COMMAND).check_update(u))
            )
        )
        # Count number of inline queries
        register_stats(SimpleStats("ilq", lambda u: bool(u.inline_query and u.inline_query.query)))

        # Register handlers
        async def callback(u, c):
            await u.message.reply_text(u.message.text)

        application.add_handler(MessageHandler(filters.TEXT, callback))

        # Start the Bot
        application.run_polling()


    if __name__ == "__main__":
        main()

Advanced Usage
--------------

To create your own, customized statistics, subclass `BaseStats <https://Bibo-Joshi.github.io/ptbstats/ptbstats.basestats.html>`_.
