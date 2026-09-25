Pipenv Template
=============================

The **Pipenv Template** switches your project's dependency management to **Pipenv**.

It's an `exclusive template <../concepts/index.html#exclusive-templates>`_: it can't be installed alongside `Poetry <../poetry/index.html>`_ or `uv <../uv/index.html>`_, only instead of one of them.

Switching to Pipenv
----------------------

.. code-block:: bash

    appcraft add_template pipenv

This reads whatever dependencies the project currently has — from Poetry, uv, or an existing Pipfile — and writes them as a ``Pipfile``, replacing whichever format was previously in use. Nothing needs to be reinstalled by hand, and switching back to another manager later round-trips the same dependencies again.
