# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Neradoc
#
# SPDX-License-Identifier: Unlicense

from supervisor import ticks_ms


class Profiler:
    def __init__(self, sample_size=5):
        self.samples = sample_size
        self.times = [0] * sample_size
        self.index_times = 0
        self.time_start = 0
        self.newline = False

    def start(self):
        self.time_start = ticks_ms()

    def profile(self, newline=False):
        time_end = ticks_ms()
        self.times[self.index_times % self.samples] = time_end - self.time_start
        self.index_times += 1
        average = sum(self.times[: self.index_times + 1]) / min(
            self.index_times, self.samples
        )
        print(f"Average scan time: {average:8.2f}     ", end="\r")
        if bool(newline):
            print("")

    def section(self, newline):
        self.newline = newline
        return self

    def __enter__(self):
        self.time_start = ticks_ms()
        return self

    def __exit__(self, type_er, value, traceback):
        self.profile(self.newline)
