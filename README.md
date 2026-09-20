<p align="center">
  <img src="https://raw.githubusercontent.com/Faycall1l/Ashiart/main/docs/images/logo.svg" width="640" alt="AshiArt logo: terminal card showing the brightness ramp @ # S % ? * + ; : , . from dark to light" />
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
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform support" />
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
- [Examples](#examples)
- [Project structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

AshiArt maps image brightness to characters so pictures remain recognizable
as text. It is aimed at developers and artists who want fast previews in the
terminal, stylized text output for documents, and shareable HTML renderings
that keep the original colors.

Input formats are whatever Pillow supports, including JPEG and PNG.

Sample output (`docs/images/sample.jpg`, width 60, standard mode):

```text
SSSSS%*++++;;+?%SSSSSSSSS%*;::;+*+.    ,?SS###SSSSSSSSSSSSS#
S####SS%???**?%%%%%%SS%%%???**??%?:    ,%####SSSSSSSSSSSSSSS
###########SSSSS%%%%%??*?*++;::::::,.  ;S@##SSSSSS###S##SSSS
#######SSS#SSSSSS??%%%?;;;;+?%%**?***++;+?S##############SSS
############SSS%*%?+:,.....,,;**??*%S##?%?**S@##SSS#####SSSS
###############*?+:+**+:::.,:,::,.::,:;,:*%S?%#SS%%S####SSSS
#############@?+:+S@@@@S?**;:,::,,,;+;;+;:,;?+SSSSSSSS######
#####@@@##@@@S::+S#@@##@@@@?:,:;,,+S####@#%*:;?SSSS#########
############@*::+?%%@@@@@@#*:,;:,,%@@##@@@@#*:+%SSSS########
#####@######@;;;:**?S#@@@@%:,;%+;;S@@@@@S%S?:+++#SS#########
#####@@@@#@##:;%+:+++++*%?+,,+@?::S@###S?**+:*++############
#######@#####;:%@+:::,,:;:,,,?%;,:*??+;;+*++??++%#S#########
S###########@%;*S@: .,,:;+;,::;:;*+::,::::??*+*??###########
###########@@@*++%%:  .:+??+::;+?*+:,. .+?%++*%%?%@@@#######
#############@%?*+%S?:..,;*%????*;,.. :%#?++*S#SS?@@@@######
##############?*%**?%SS+:,,;??+;::::+%S?**?++S#S%?@@@@@#####
##############?+++*%??%SS%*;?*;+*%SSSS??%%??*%@S?%#@##@@@###
##############%*?**?*?%SSS#SS#S##SSS%%%%%?%S%%S#%%S#########
SSS##@@@######%%%%%%%SSSSSSS##SSSSSSSSS%SSSSSSSSSS%%########
SSS#####SSSS##SSSS%SSSSS#S#SSS#S##SS#SS##S#S##%%SSSSSS#SSSS#
```

A closer crop (`docs/images/owl-face.jpg`, width 70) resolves the eyes,
beak, and feather texture. Dense mode (70 levels) renders it best — try:

```bash
ashiart docs/images/owl-face.jpg --width 70 --mode dense
```

## Features

- Image-to-ASCII conversion with adjustable width and height
- Four rendering modes: standard, dense, blocks, braille
- ANSI truecolor terminal output sampled from the source image
- Color-preserving HTML export with configurable font size
- Image controls: contrast, brightness, sharpness, autocontrast,
  edge enhancement, dithering, and inversion
- Custom character ramps ordered from darkest to lightest
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
| `image_path` | required | Input image path |
| `-o, --output` | console | Text output file; prints to stdout when omitted |
| `-w, --width` | `100` | Output width in characters |
| `-H, --height` | proportional | Output height in characters |
| `-c, --chars` | built-in ramp | Custom characters, darkest to lightest |
| `-m, --mode` | `standard` | `standard`, `dense`, `blocks`, or `braille` |
| `--contrast` | `1.0` | Contrast multiplier |
| `--brightness` | `1.0` | Brightness multiplier |
| `--sharpness` | `1.0` | Sharpness multiplier |
| `--edge-enhance` | off | Enhance edges before mapping |
| `--no-autocontrast` | off | Disable automatic level stretching |
| `--dithering` | off | Apply dithering for texture |
| `--invert` | off | Invert brightness mapping |
| `--color` | off | Emit ANSI truecolor escape codes |
| `--html PATH` | none | Write color HTML rendering to `PATH` |
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
    image_to_enhanced_ascii,
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

# Convenience functions
art = image_to_enhanced_ascii(
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
| `standard` | 12-level ASCII ramp | Clean, readable terminal output |
| `dense` | 70+ characters | Smoother gradients and detail |
| `blocks` | Unicode block elements | High-contrast geometric look |
| `braille` | Unicode braille patterns | Higher effective resolution |

## Character ramp

The default ramp is ordered strictly from darkest to lightest. It ends
with a space, so pure white renders as blank paper instead of a dot:

```text
@ # S % ? * + ; : , . (space)
```

The header logo visualizes this same sequence as a brightness scale.
Custom ramps must preserve that ordering, for example:

```bash
ashiart input.jpg --chars "@%*+=-:. "
```

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
  __init__.py      Public package exports
  generator.py     Baseline ASCII generator with ANSI support
  enhanced.py      Modes, enhancements, HTML, and ANSI support
  cli.py           Command-line interface
test/
  test_generator.py
  test_enhanced.py
  test_cli.py
docs/images/
  logo.svg         Project logo and brightness-ramp reference
  sample.jpg       Sample input used in this README
  owl-face.jpg     Tight face crop for high-detail demos
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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE)
file for details.
