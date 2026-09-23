<p align="center">
  <img src="https://raw.githubusercontent.com/Faycall1l/Ashiart/main/docs/images/logo.svg" width="640" alt="AshiArt logo: sixteen amber cells fading from solid to empty on near-black" />
</p>

<h1 align="center">AshiArt</h1>

<p align="center">
  Convert images to ASCII art from the terminal or Python.
  Plain text, ANSI truecolor, and color-preserving HTML output.
</p>

<p align="center">
  <a href="https://pypi.org/project/ashiart/"><img src="https://img.shields.io/pypi/v/ashiart" alt="PyPI version" /></a>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python 3.8+" />
  <a href="https://github.com/Faycall1l/Ashiart/actions"><img src="https://github.com/Faycall1l/Ashiart/actions/workflows/python-package.yml/badge.svg" alt="Build status" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license" /></a>
</p>

## Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Command-line reference](#command-line-reference)
- [Python API](#python-api)
- [Rendering modes](#rendering-modes)
- [Character ramp](#character-ramp)
- [How it works](#how-it-works)
- [Examples](#examples)
- [Project structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Overview

AshiArt converts images to character grids for terminals, plain-text
documents, and color-preserving HTML pages. Each output cell encodes the
brightness — and optionally the contour direction — of its source pixels.

Decodes any image format Pillow supports, including JPEG, PNG, BMP, GIF,
and WebP — from a local path or directly from an http(s) URL.

Sample output (`docs/images/puppy.jpg`, width 60, standard mode with
edge overlay — contours drawn from Sobel orientation):

```text
%%*??*+++;::,.,. .     .,:, . ..,,,.....,,,.:;:;;;+*???%%S##
%?*++;;::,::,..----------------/   ----%+,:;+;::;;:::;+**?%%
?*+;;;::,,,,.\\---@@@@@@@@@@@--------@S+,::;;*;++;++;;++***?
**+;::,     \\@@@@@@#@@####S##@@--@@#SS-----::+*;:::;+***??%
;;:,,...   \\@@@@@@######%##SSS@@@@@###@@@@-//,:,,::;++*+**?
*+;;;;:::,\\@@@@@####S##S#@S%%SSSS###@@@@#@@@|,,,:;;;;;;+***
%*++;;:,, ||@@@@##S#SSS%SS##%%%%%SSSS#@@@@@@#|:;;;;;;+;+;+**
*+++;,,,, ||@@@@####S###%S#@S%S@#S@S##%#@@@@||;:::;::::;:;+?
+:;::,..,.//@@@@#SS###S#S#@@S%+%#SS%S#SS@@@#S+;;:;;++;;;:;;+
;:,,,.... ///##@##SS##%SSS@#@S+?%S%S#@@@@@\*******+?*****??*
:::::,..   //@###@####S#@#@@#@SS%%SS##@@@?*+***+++++*+****?%
;;;::,,...,.///####@###S#@@@@#@#%S#SS##@#?**++++;;;;+***?%%%
?*;,,,..,,.,.//--@@@#S#########S%S?%S##@@S%?*+*+++++++*????%
;;;::::::,,....-------%%#####@#%??%#@#@@\\++++*+**+****????%
;:::,,,:,.,,....  ---//SSSSS#@@@######S\\:;:;++++****????%??
*+**+;:,,,.,.,,,,.... //##@#@#@@##@@@@\\,:,:;;;;;;+;*?++%SSS
????*+;::;:,,,,,,,,... //S#@@@@#\-----\:::::;+;;+*%%%%?%%SSS
S%%%?**+**++;;:::,,,,,:,//#@@@@|\,---.,,,,,:::;+***??%%%%%S#
SS%%???*++++;;:;;::,,:::,/@#@@@\| ,.,,,,,,,:,,:;+**?%%%%SSS#
SSS%%??****++;+;;;;::::::;*?%%?;;::;;;++;;+++++**??%SSSSSS##
```

```bash
ashiart docs/images/puppy.jpg --width 60 --edges --edge-threshold 0.5
```

Photo: black puppy via Lorem Picsum (id 237, Unsplash license).
A dark, single-subject coat against light planks is the input profile
ASCII renders most faithfully: high contrast, one subject, clean edges.

The owl close-up (`docs/images/owl-face.jpg`, width 70) exercises fine
detail instead. Dense mode (69 levels) renders it best — try:

```bash
ashiart docs/images/owl-face.jpg --width 70 --mode dense
```

Truecolor terminal output (`docs/images/puppy-head.jpg`, dense mode,
`--color`), rendered here as an image since Markdown cannot show ANSI:

<p align="center">
  <img src="https://raw.githubusercontent.com/Faycall1l/Ashiart/main/docs/images/color-preview.png" width="630" alt="Truecolor ASCII art of a black puppy head" />
</p>

```bash
ashiart docs/images/puppy-head.jpg --width 70 --mode dense --color
```

## Features

- Image-to-ASCII conversion with explicit width, or proportional height
- Four rendering modes: standard, dense, blocks, braille
- Sobel edge overlay: strong contours drawn as directional `- / | \` glyphs
- ANSI truecolor terminal output, per-cell color sampled after enhancement
- Color-preserving HTML export with configurable font size
- Tonal controls: contrast, brightness, sharpness, autocontrast
  (level stretching, on by default), dithering, inversion
- Custom character ramps, ordered darkest to lightest
- Command-line interface and importable Python API
- Cross-platform: macOS, Linux, and Windows

## Requirements

- Python 3.8 or newer
- Pillow 10 or newer
- NumPy 1.20 or newer

## Installation

From PyPI:

```bash
pip install ashiart
```

From source:

```bash
git clone https://github.com/Faycall1l/Ashiart.git
cd Ashiart
pip install .
```

Development install:

```bash
pip install -e .
pip install pytest
```

## Quick start

Print ASCII art to the terminal:

```bash
ashiart docs/images/sample.jpg --width 80
```

No local file needed — URLs download on the fly:

```bash
ashiart https://picsum.photos/id/237/1200/800 --width 80
```

Nothing at hand at all — render the built-in calibration image:

```bash
ashiart --demo --width 80
```

Save plain-text output and a color HTML rendering in one run:

```bash
ashiart docs/images/sample.jpg \
  --width 80 \
  --mode dense \
  --contrast 1.3 \
  --edge-enhance \
  --output output.txt \
  --html output.html
```

Colorized terminal output with block characters:

```bash
ashiart docs/images/sample.jpg --mode blocks --color --width 100
```

Minimal Python usage:

```python
from ashiart import image_to_ascii

art = image_to_ascii("docs/images/sample.jpg", width=80)
print(art)
```

## Command-line reference

| Option | Default | Description |
| --- | --- | --- |
| `image_path` | required | Local path, http(s) URL, `-` for stdin; omit with `--demo` |
| `--demo` | off | Render the built-in calibration image |
| `-o, --output` | console | Text output file; prints to stdout when omitted |
| `-w, --width` | tty width, else `100` | Output width in characters |
| `-H, --height` | proportional | Output height in characters |
| `-c, --chars` | built-in ramp | Custom characters, darkest to lightest |
| `-m, --mode` | `standard` | `standard`, `dense`, `blocks`, or `braille` |
| `--contrast` | `1.0` | Contrast multiplier |
| `--brightness` | `1.0` | Brightness multiplier |
| `--sharpness` | `1.0` | Sharpness multiplier |
| `--edge-enhance` | off | PIL edge-enhancement filter before mapping |
| `--edges` | off | Sobel overlay: contours as `- / | \` glyphs |
| `--edge-threshold` | `0.35` | Normalized Sobel magnitude gate for `--edges` |
| `--no-autocontrast` | off | Disable automatic level stretching |
| `--dithering` | off | Apply dithering for texture |
| `--invert` | off | Invert brightness mapping |
| `--color` | off | Emit ANSI truecolor escape codes |
| `--html PATH` | none | Write color HTML rendering to `PATH` |
| `--open` | off | Open the `--html` output in a browser (requires `--html`) |
| `--font-size` | `8` | HTML font size in pixels |

Full help:

```bash
ashiart --help
```

## Python API

Basic generator:

```python
from ashiart import AsciiArtGenerator, image_to_ascii

generator = AsciiArtGenerator(width=80)
art = generator.generate_from_image("docs/images/sample.jpg")
generator.save_to_file(art, "output.txt")

# ANSI truecolor variant
color_art = generator.generate_from_image("docs/images/sample.jpg", color=True)
```

Enhanced generator:

```python
from ashiart import (
    EnhancedAsciiArtGenerator,
    image_to_ascii,
    image_to_html_ascii,
)

generator = EnhancedAsciiArtGenerator(width=80, mode="dense")
generator.set_enhancement(contrast=1.4, brightness=1.05, edge_enhance=True)
art = generator.generate_from_image("docs/images/sample.jpg")

# ANSI truecolor output
color_art = generator.generate_from_image("docs/images/sample.jpg", ansi=True)

# HTML output with original colors
html = generator.generate_html(
    "docs/images/sample.jpg",
    preserve_color=True,
    font_size=8,
)
generator.save_html_to_file(html, "output.html")

# Convenience functions (single text entry point + HTML)
art = image_to_ascii(
    "docs/images/sample.jpg",
    width=80,
    mode="dense",
    contrast=1.3,
    edge_enhance=True,
)
html = image_to_html_ascii("docs/images/sample.jpg", width=80)
```

## Rendering modes

| Mode | Character set | Best for |
| --- | --- | --- |
| `standard` | 12-level ASCII ramp | Legible terminal output |
| `dense` | 69-level measured ramp | Smooth gradients, photographic detail |
| `blocks` | 5-level block ramp (`█▓▒░ `) | High-contrast geometric look |
| `braille` | 256 dot patterns, 2×4 dots per cell | ~4× effective resolution |

## Character ramp

The default ramp is ordered strictly from darkest to lightest. It ends
with a space, so pure white renders as blank paper instead of a dot:

```text
@ # S % ? * + ; : , . (space)
```

The header logo states the same idea geometrically: a grid of cells
fading from solid to empty, i.e. brightness mapped to ink.
Custom ramps must preserve darkest-to-lightest ordering, for example:

```bash
ashiart input.jpg --chars "@%*+=-:. "
```

## How it works

Each output cell corresponds to exactly one resized pixel (braille packs
a 2×4 block per cell). The pipeline, in order:

0. **Load.** Decode from a local path or http(s) URL, apply EXIF
   orientation so phone photos render upright, and composite
   transparency onto white.
1. **Resample.** LANCZOS downscale to `width` columns. Rows default to
   `height × width / image_width × 0.5`, compensating the ~2:1
   height-to-width ratio of monospace glyphs; `--height` overrides it.
2. **Enhance.** Contrast, brightness, and sharpness multipliers, then an
   edge-enhancement filter and optional inversion. All default to neutral.
3. **Grayscale.** PIL `L` mode (ITU-R BT.601 luma). Autocontrast, on by
   default, stretches the used range to 0–255 with a 1% cutoff so the
   full ramp is exercised.
4. **Edge field (optional, `--edges`).** 3×3 Sobel gradients per cell,
   magnitude normalized by the frame peak. Cells at or above
   `--edge-threshold` (default 0.35) take a contour glyph from the
   gradient direction rotated 90° and folded into [0°, 180°):

   | Contour direction | Glyph | Angle range |
   | --- | --- | --- |
   | Horizontal | `-` | [0°, 22.5°) ∪ [157.5°, 180°) |
   | Diagonal | `/` | [22.5°, 67.5°) |
   | Vertical | `\|` | [67.5°, 112.5°) |
   | Diagonal | `\` | [112.5°, 157.5°) |

   Remaining cells keep their tonal character. Skipped in braille mode.
5. **Map.** `index = round(L / 255 × (N−1))`, clamped to the ramp.
   Rounding (not truncation) gives every character a symmetric
   brightness bucket. Braille cells threshold each of their 8 dots
   at 128 instead.
6. **Emit.** Plain text, ANSI truecolor foreground per cell, or HTML
   `<span>` elements preserving the enhanced per-cell color.

## Examples

- `examples/basic_usage.py`: minimal conversion and custom ramps
- `examples/enhanced_demo.py`: modes, enhancements, and HTML export

Run the basic example:

```bash
python examples/basic_usage.py docs/images/sample.jpg
```

## Project structure

```text
ashiart/
  __init__.py      Public exports: generators, image_to_ascii, HTML helper
  generator.py     NumPy-free single-ramp converter with ANSI support
  enhanced.py      Modes, enhancements, Sobel edge overlay, HTML, ANSI
  cli.py           Command-line interface (all flags in one parser)
test/
  test_generator.py
  test_enhanced.py
  test_cli.py
docs/images/
  logo.svg           Project logo and brightness-ramp reference
  sample.jpg         Sample input used in code snippets
  puppy.jpg          High-contrast hero sample used in this README
  puppy-head.jpg     Tight head crop for the color demo
  owl-face.jpg       Tight face crop for high-detail demos
  color-preview.png  Rendered truecolor preview shown above
examples/
  basic_usage.py
  enhanced_demo.py
```

## Development

Install an editable copy and run the test suite:

```bash
pip install -e .
pytest
```

Continuous integration runs `pytest` on Python 3.8 through 3.11 for pushes
and pull requests to `main`.

## Contributing

Contributions are welcome. Please open an issue to discuss a change before
submitting a pull request, keep new behavior covered by tests, and follow
the existing code style.

## Acknowledgements

- [BEPb/image_to_ascii](https://github.com/BEPb/image_to_ascii) for the
  URL-input, video-conversion, and gallery ideas this project adopts
- Paul Bourke for the canonical density ramps
  ([Character representation of grey scale images](http://www.paulbourke.net/dataformats/asciiart/))
- Alex Harri Jónsson and the pixquill benchmark for the shape-aware
  rendering literature behind the edge overlay and measured ramp
- Lorem Picsum for the puppy demo photo (id 237, Unsplash license)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.
