=========
Changelog
=========

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
