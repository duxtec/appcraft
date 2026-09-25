uv Template
=============================

The **uv Template** switches your project's dependency management to **uv**.

It's an `exclusive template <../concepts/index.html#exclusive-templates>`_: it can't be installed alongside `Poetry <../poetry/index.html>`_ or `Pipenv <../pipenv/index.html>`_, only instead of one of them.

Switching to uv
------------------

.. code-block:: bash

    appcraft add_template uv

This reads whatever dependencies the project currently has — from Poetry, Pipenv, or an existing uv-managed ``pyproject.toml`` — and writes them as native PEP 621 ``[project]``/``[dependency-groups]`` tables, replacing whichever format was previously in use. Nothing needs to be reinstalled by hand, and switching back to another manager later round-trips the same dependencies again.
