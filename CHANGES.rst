=========
Changelog
=========

Version 2.2
===========
*Released 2023-09-02*

* Upgrades ``python-telegram-bot`` to ``~=20.4``
* Upgrades ``plotly`` to ``~=5.16``
* Fixes smaller bugs

Version 2.1
===========
*Released 2023-01-06*

* Upgrades ``python-telegram-bot`` to ``~=20.0``
* Upgrades ``plotly`` to ``~=5.11``
* Fix a bug where all ``SimpleStats`` instances would override each other's stored data

Version 2.0.2
=============
*Released 2022-05-22*

* Fix a bug in ``SimpleStats``

Version 2.0.1
=============
*Released 2022-05-22*

* Fix a bug in ``SimpleStats``
* Fix ``pre-commit``

Version 2.0
===========
*Released 2022-05-21*

**Major changes:**
    * Upgrades to ``python-telegram-bot`` v20.0a0, introducing ``asyncio``. Not backwards compatible.
    * Persistence interface of ``BaseStats`` was completely reworked and is not backwards compatible.

Version 1.3.1
=============
*Released 2021-02-25*

**Minor changes for SimpleStats:**

* Send data as HTML instead of PDF
* Drop ``kaleido`` dependency

Version 1.3
===========
*Released 2020-10-11*

**Major changes:**

* Upgrade to PTB v13.0
* Add options to ``BaseStats`` to run ``process_update`` and/or ``reply_statistics`` asynchronously
* Run ``SimpleStats.reply_statistics`` asynchronously and improve sending of ``ChatAction``.

Version 1.2
===========
*Released 2020-08-24*

**Major changes:**

* Drop support for Python < 3.7

**Bug fixes and minor changes for** ``SimpleStats`` **:**

* Use ``dict`` instead of ``defaultdict`` as it seems to be more stable for persistence
* Fill missing dates already on processing updates to make retrieving stats quicker

Version 1.1
===========
*Released 2020-08-17*

**Bug fixes:**

* Add ``kaleido`` to requirements. *Note:* ``kaleido`` is currently not available for all architectures. See the `bug tracker <https://github.com/plotly/Kaleido/issues>`_ and e.g. this `issue <https://github.com/plotly/Kaleido/issues/7>`_.
* Fix wrong default groups for statistics handlers

Version 1.0
===========
*Released 2020-08-16*

Initial release. Adds basic functionality.
