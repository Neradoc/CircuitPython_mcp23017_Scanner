# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
#
# SPDX-License-Identifier: Unlicense

import board
from adafruit_mcp230xx.mcp23017 import MCP23017
from mcp23017_scanner import McpMatrixScanner

# MCP23017 port A pins for columns
COLUMNS = [0, 1, 2, 3, 4]
# MCP23017 port B pins for rows
ROWS = [0, 1, 2, 3, 4, 5]

mcp = MCP23017(board.I2C())
scanner = McpMatrixScanner(mcp, ROWS, COLUMNS, irq=board.D5)  # irq is optional

# this is profiling code, remove.
from profiler import Profiler

profiler = Profiler(100)

while True:
    with profiler:
        scanner.update()
        profiler.newline = len(scanner.events)

    while event := scanner.events.get():
        key = scanner.key_number_to_row_column(event.key_number)
        if event.pressed:
            print(f"Key pressed : {key}")
        if event.released:
            print(f"Key released: {key}")
