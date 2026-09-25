Flask UI Template
=============================

The **Flask UI Template** adds server-rendered web pages on top of the shared `Flask Template <../flask/index.html>`_ — it depends on ``flask`` and can be installed together with, or independently of, the `Flask API Template <../flask_api/index.html>`_.

It adds ``presentation/web/ui/`` (``views/``, Jinja ``templates/``, ``static/`` assets), which ``flask``'s own router auto-discovers: every view function under ``views/`` gets a URL rule, and every ``.html`` file under ``templates/pages/`` gets a static route — no manual registration needed. It also brings in the ``flask-assets`` dependency for asset bundling.

If the ``sqlalchemy`` template is also installed, the shared ``flask`` template initializes the database connection automatically; without it, the UI runs without persistence.
