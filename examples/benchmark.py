#!/usr/bin/env python3
"""Render throughput benchmark: characters per second per mode."""

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ashiart import EnhancedAsciiArtGenerator

IMAGE = os.path.join(os.path.dirname(__file__), "..", "docs", "images", "puppy-head.jpg")
WIDTHS = (60, 100, 200)
MODES = ("standard", "dense", "blocks")
REPEATS = 5


def bench(mode, width):
    generator = EnhancedAsciiArtGenerator(width=width, mode=mode)
    art = generator.generate_from_image(IMAGE)  # warm up caches
    cells = sum(len(line) for line in art.split("\n"))
    best = min(
        _timed(generator, mode) for _ in range(REPEATS)
    )
    print(f"{mode:>8} w={width:<4} {cells / best:>12,.0f} chars/s")


def _timed(generator, mode):
    started = time.perf_counter()
    generator.generate_from_image(IMAGE)
    return time.perf_counter() - started


def main():
    print(f"image: {os.path.basename(IMAGE)} (best of {REPEATS})")
    for mode in MODES:
        for width in WIDTHS:
            bench(mode, width)


if __name__ == "__main__":
    main()
