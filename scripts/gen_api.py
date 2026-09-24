#!/usr/bin/env python3
"""Generate docs/API.md from live docstrings.

Usage: python scripts/gen_api.py [--check]
With --check, exits 1 when docs/API.md differs from generated output.
"""

import inspect
import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

import ashiart  # noqa: E402
import ashiart.animate  # noqa: E402
import ashiart.cli  # noqa: E402
import ashiart.enhanced  # noqa: E402
import ashiart.generator  # noqa: E402
import ashiart.io  # noqa: E402
import ashiart.tonal  # noqa: E402
import ashiart.video  # noqa: E402

MODULES = [
    ("ashiart.generator", ashiart.generator, "Baseline converter"),
    ("ashiart.enhanced", ashiart.enhanced, "Modes, enhancements, HTML"),
    ("ashiart.animate", ashiart.animate, "Terminal animation"),
    ("ashiart.video", ashiart.video, "Video and webcam input (extra)"),
    ("ashiart.tonal", ashiart.tonal, "Tonal operators"),
    ("ashiart.io", ashiart.io, "Loading, orientation, flattening"),
    ("ashiart.cli", ashiart.cli, "Command-line interface"),
]


def _summary(obj):
    doc = inspect.getdoc(obj) or ""
    return doc.split("\n\n")[0].replace("\n", " ")


def _members(module):
    found = []
    for name in dir(module):
        if name.startswith("_"):
            continue
        obj = getattr(module, name)
        if inspect.isfunction(obj) and obj.__module__ == module.__name__:
            found.append((name, obj))
        elif inspect.isclass(obj) and obj.__module__ == module.__name__:
            found.append((name, obj))
    return sorted(found)


def generate():
    lines = [
        "# API Reference",
        "",
        "Generated from docstrings by `scripts/gen_api.py`. "
        "The package version is defined in `ashiart/__init__.py`.",
        "",
    ]
    for dotted, module, blurb in MODULES:
        lines.append(f"## `{dotted}` — {blurb}")
        lines.append("")
        for name, obj in _members(module):
            try:
                signature = str(inspect.signature(obj))
            except (TypeError, ValueError):
                signature = ""
            lines.append(f"### `{name}{signature}`")
            lines.append("")
            lines.append(_summary(obj) or "No summary.")
            lines.append("")
    return "\n".join(lines)


def main():
    path = os.path.join(REPO_ROOT, "docs", "API.md")
    text = generate()
    if "--check" in sys.argv[1:]:
        with open(path, encoding="utf-8") as file:
            current = file.read()
        if current != text:
            print("docs/API.md is stale; run scripts/gen_api.py")
            return 1
        return 0
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
