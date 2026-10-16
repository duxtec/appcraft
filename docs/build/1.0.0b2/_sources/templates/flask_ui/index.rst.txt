Flask UI Template
=============================

The **Flask UI Template** adds server-rendered web pages on top of the shared `Flask Template <../flask/index.html>`_ — it depends on ``flask`` and can be installed together with, or independently of, the `Flask API Template <../flask_api/index.html>`_.

It adds ``presentation/web/ui/`` (``views/``, Jinja ``templates/``, ``static/`` assets), which ``flask``'s own router auto-discovers: every view function under ``views/`` gets a URL rule, and every ``.html`` file under ``templates/pages/`` gets a static route — no manual registration needed. It also brings in the ``flask-assets`` dependency for asset bundling.

If the ``sqlalchemy`` template is also installed, the shared ``flask`` template initializes the database connection automatically; without it, the UI runs without persistence.

Adding a Page
-------------

There are two ways to add a page. Both are picked up automatically.

**A page with logic.** Add a function to a module under ``presentation/web/ui/views/``. The function name becomes the URL: ``products()`` is served at ``/products``, and ``index()`` at ``/``. The function renders a template from ``presentation/web/ui/templates/views/``. For example, ``presentation/web/ui/views/products.py``:

.. code-block:: python

    from flask import render_template


    def products():
        return render_template("views/products.html", names=["Notebook", "Mouse"])

and ``presentation/web/ui/templates/views/products.html``, which extends the shared layout:

.. code-block:: html

    {% extends "layouts/base.html" %}
    {% block content %}
    <h1>Products</h1>
    <ul>{% for name in names %}<li>{{ name }}</li>{% endfor %}</ul>
    {% endblock %}

``GET /products`` now returns the page. To show real data, pass the result of a use case to the template, using the same use case you wrote in :doc:`../../developing/recipes`. A view should stay as thin as a runner: fetch, render, return.

**A static page.** Any ``.html`` file in ``presentation/web/ui/templates/pages/`` is served at a route named after the file: ``about.html`` becomes ``/about``, and ``index.html`` becomes ``/``. Use this for content that doesn't depend on the database.
