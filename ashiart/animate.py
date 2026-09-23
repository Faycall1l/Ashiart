"""Terminal animation: render frame sequences as looping ASCII playback."""

import json
import shutil
import sys
import time

from .io import open_raw

CLEAR_SCREEN = "\x1b[2J"
CURSOR_HOME = "\x1b[H"


def iter_gif_frames(source):
    """Split an animated image into (RGB frame, duration_ms) pairs.

    Args:
        source: Local path, bytes, or URL of a GIF/WebP animation.

    Returns:
        list: [(PIL.Image, int)] with per-frame durations in
        milliseconds (100 fallback when the frame carries none).
    """
    image = open_raw(source)
    frames = []
    try:
        while True:
            frames.append((image.convert("RGB"), image.info.get("duration", 100)))
            image.seek(image.tell() + 1)
    except EOFError:
        pass
    return frames


def fit_to_terminal(width=None, height=None, aspect=0.5):
    """Resolve playback dimensions against the terminal size.

    Args:
        width (int or None): Desired columns; terminal width when None.
        height (int or None): Desired rows; derived when None.
        aspect (float): Row height compensation for monospace glyphs.

    Returns:
        tuple: (columns, rows or None).
    """
    try:
        columns, rows = shutil.get_terminal_size()
    except OSError:
        columns, rows = 80, 24
    width = min(width or columns - 2, columns - 2)
    if height is None:
        return max(width, 1), None
    return max(width, 1), max(min(height, rows - 4), 1)


def play_animation(frames, frame_ms=100, loops=0, max_fps=30,
                   output=None, sleeper=None):
    """Print ASCII frames as a looping terminal animation.

    Args:
        frames (list): Pre-rendered ASCII frame strings.
        frame_ms (int or list): Per-frame duration(s) in milliseconds.
        loops (int): Loop count; 0 loops forever until interrupted.
        max_fps (float): Upper frame-rate bound.
        output: Writable stream; defaults to stdout.
        sleeper: Sleep callable; defaults to time.sleep.

    Returns:
        int: Completed loop count.
    """
    output = output if output is not None else sys.stdout
    sleeper = sleeper if sleeper is not None else time.sleep
    if isinstance(frame_ms, (int, float)):
        frame_ms = [frame_ms] * len(frames)
    min_interval = 1.0 / max_fps if max_fps else 0.0
    completed = 0
    output.write(CLEAR_SCREEN)
    try:
        while loops == 0 or completed < loops:
            for text, duration in zip(frames, frame_ms):
                started = time.monotonic()
                output.write(CURSOR_HOME + text)
                output.flush()
                interval = max(duration / 1000.0, min_interval)
                remaining = interval - (time.monotonic() - started)
                if remaining > 0:
                    sleeper(remaining)
            completed += 1
    except KeyboardInterrupt:
        pass
    output.write("\n")
    return completed


def save_animation_html(frames, output_path, frame_ms=100, font_size=10,
                        font_family="monospace", bg="black"):
    """Write frames as a self-contained looping HTML animation.

    Args:
        frames (list): Pre-rendered ASCII frame strings.
        output_path (str): Destination .html path.
        frame_ms (int or list): Per-frame duration(s) in milliseconds.
        font_size (int): Font size in pixels.
        font_family (str): CSS font family.
        bg (str): Page background, "black" or "white".

    Returns:
        str: The output path.
    """
    if bg not in ("black", "white"):
        raise ValueError(f"Background must be black or white: {bg}")
    fg = "white" if bg == "black" else "black"
    if isinstance(frame_ms, (int, float)):
        frame_ms = [frame_ms] * len(frames)
    payload = json.dumps(frames).replace("</", "<\\/")
    timings = json.dumps(frame_ms)
    html = f"""<!DOCTYPE html>
<html>
<head>
<title>ASCII Animation</title>
<style>
  pre {{
    font-family: {font_family};
    font-size: {font_size}px;
    line-height: 1;
    letter-spacing: 0;
    background-color: {bg};
    color: {fg};
    display: inline-block;
    padding: 10px;
  }}
</style>
</head>
<body>
<pre id="frame"></pre>
<script>
const frames = {payload};
const timings = {timings};
let index = 0;
function tick() {{
  document.getElementById("frame").textContent = frames[index];
  setTimeout(tick, timings[index]);
  index = (index + 1) % frames.length;
}}
tick();
</script>
</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)
    return output_path
