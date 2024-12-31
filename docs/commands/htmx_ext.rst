htmx_ext
========

This command downloads an htmx extension. The list of extensions is pulled from `htmx-extensions.oluwatobi.dev <https://htmx-extensions.oluwatobi.dev/>`_. If you run
the command without specifying any arguments, it will list all the available extensions instead.
Similar to the `htmx` commands, this will also use your ``pyproject.toml`` file if it's found. However,
it's solely for downloading the extensions file next to your ``htmx.min.js`` file, in case no path was specified in the command.

.. cappa:: falco.management.commands.HtmxExtension

**Example**

.. code-block:: bash

   falco htmx-ext sse
