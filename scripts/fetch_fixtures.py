#!/usr/bin/env python3
"""Fetch pinned test fixture images and verify their SHA256 digests.

Fixtures are real photos chosen for ASCII-friendliness: one simple
subject each, smooth backgrounds, no high-frequency clutter. They are
committed under test/fixtures/ so the suite stays offline and
deterministic; re-run this script to refresh them after verifying the
new digests by eye.

Provenance (Unsplash license, via Lorem Picsum):
- portrait.jpg: woman's face on a soft gray background (id 1027)
- waterlily.jpg: white bloom on dark water (id 306)

Usage: python scripts/fetch_fixtures.py [--check]
With --check, exits 1 when a committed fixture differs from its pin.
"""

import hashlib
import os
import sys
import urllib.request

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIXTURE_DIR = os.path.join(REPO_ROOT, "test", "fixtures")

SOURCES = (
    (
        "https://picsum.photos/id/1027/400/400",
        "portrait.jpg",
        "54b3a9cfae38c9556a1558d508de3b98540cbbfce89e40482248de3dc77e89dd",
    ),
    (
        "https://picsum.photos/id/306/400/400",
        "waterlily.jpg",
        "d11d24085949720b324c263fa59e0bb422024a0aa44aa6d511b4d1b1a84a7070",
    ),
)


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "ashiart-fixtures"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def main():
    check_only = "--check" in sys.argv[1:]
    failures = 0
    for url, filename, pinned in SOURCES:
        path = os.path.join(FIXTURE_DIR, filename)
        if check_only:
            with open(path, "rb") as file:
                digest = _digest(file.read())
            status = "ok" if digest == pinned else "MISMATCH"
            print(f"{filename}: {status}")
            failures += status != "ok"
            continue
        data = _fetch(url)
        digest = _digest(data)
        if digest != pinned:
            print(f"{filename}: upstream bytes changed ({digest}); refusing to write")
            failures += 1
            continue
        os.makedirs(FIXTURE_DIR, exist_ok=True)
        with open(path, "wb") as file:
            file.write(data)
        print(f"{filename}: fetched {len(data)} bytes, digest ok")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
