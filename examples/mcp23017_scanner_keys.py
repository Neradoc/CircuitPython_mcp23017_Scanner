# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
#
# SPDX-License-Identifier: Unlicense

import board
from supervisor import ticks_ms
from adafruit_mcp230xx.mcp23017 import MCP23017
from mcp23017_scanner import McpKeysScanner

# MCP23017 port A/B pins
PINS = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14]

mcp = MCP23017(board.I2C())
scanner = McpKeysScanner(mcp, PINS)  # , irq=board.D5)

while True:
    t0 = ticks_ms()
    scanner.update()
    while event := scanner.events.get():
        key = event.key_number
        if event.pressed:
            print(f"Key pressed : {key}")
        if event.released:
            print(f"Key released: {key}")

    # flood print the milliseconds passed:
    # print(ticks_ms() - t0)
