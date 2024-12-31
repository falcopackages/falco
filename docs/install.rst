
:description: Here is the guide on how to install the falco's cli.

Installation
============

Falco is available on PyPI and can be installed with pip or your favorite Python package manager.

.. tabs::

  .. tab:: uv

    .. code-block:: shell

        uv add falco-app

  .. tab:: pip

    .. code-block:: shell

        pip install falco-app

Add ``falco`` to your ``INSTALLED_APPS`` in your Django settings file:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'falco',
        ...
    ]
