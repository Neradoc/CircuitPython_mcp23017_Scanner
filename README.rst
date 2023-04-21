Introduction
============


.. image:: https://readthedocs.org/projects/CircuitPython-mcp23017-Scanner/badge/?version=latest
    :target: https://CircuitPython-mcp23017-Scanner.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/Neradoc/CircuitPython_mcp23017_Scanner/workflows/Build%20CI/badge.svg
    :target: https://github.com/Neradoc/CircuitPython_mcp23017_Scanner/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Scan a keyboard with a MCP23017 using an API modelled after the keypad module.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install mcp23017_scanner

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: shell

    import board
    from supervisor import ticks_ms
    from adafruit_mcp230xx.mcp23017 import MCP23017
    from mcp23017_scanner import McpMatrixScanner

    # MCP23017 port A pins for columns
    COLUMNS = [ 0, 1, 2, 3, 4 ]
    # MCP23017 port B pins for rows
    ROWS = [ 0, 1, 2, 3, 4, 5 ]

    mcp = MCP23017(board.I2C())
    scanner = McpMatrixScanner(mcp, ROWS, COLUMNS, irq=board.D5) # irq is optional

    while True:
        scanner.update()
        while event := scanner.events.get():
            key = scanner.key_number_to_row_column(event.key_number)
            if event.pressed:
                print(f"Key pressed : {key}")
            if event.released:
                print(f"Key released: {key}")


Documentation
=============
API documentation for this library can be found on `Read the Docs <https://CircuitPython_mcp23017_Scanner.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/Neradoc/CircuitPython_mcp23017_scanner/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
