# AshiArt - ASCII Art Generator

![Python](https://img.shields.io/badge/python-3.6%2B-blue)

A Python package for converting images to ASCII art with standard and enhanced features.

## Features

### 🎨 Basic Features
- Convert images to ASCII art with customizable size
- Support for custom ASCII character sets
- Command-line interface for quick conversions
- Python API for integration into your applications
- Handles various image formats (JPEG, PNG, etc.)

### ✨ Enhanced Features
- **Multiple rendering modes**:
  - Standard ASCII characters
  - Dense character set (70+ shades)
  - Unicode block characters
  - Unicode braille patterns (higher resolution)
- **Image processing options**:
  - Contrast, brightness, and sharpness adjustments
  - Edge enhancement
  - Dithering
  - Image inversion
- **HTML output with original color preservation**
- Additional convenience functions

## Installation

```bash
# From PyPI
pip install ashiart

# From GitHub
pip install git+https://github.com/Faycall1l/Ashiart.git

# From source
git clone https://github.com/Faycall1l/Ashiart.git
cd ashiart
pip install .
```

## Usage

### Command Line Interface

```bash
# Basic usage (outputs to console)
ashiart docs/images/sample.jpg

# Save to file
ashiart docs/images/sample.jpg -o output.txt

# Change output width to 80 characters
ashiart docs/images/sample.jpg -w 80

# Specify both width and height
ashiart docs/images/sample.jpg -w 80 -H 40

# Use custom ASCII characters (from darkest to lightest)
ashiart docs/images/sample.jpg -c "#@%*+=-:. "
```

### Standard Python API

```python
from ashiart import AsciiArtGenerator, image_to_ascii

# Quick conversion with the convenience function
ascii_art = image_to_ascii("docs/images/sample.jpg", width=80)
print(ascii_art)

# Or use the full-featured class
generator = AsciiArtGenerator(width=80)
ascii_art = generator.generate_from_image("docs/images/sample.jpg")
print(ascii_art)

# Save the output to a file
generator.save_to_file(ascii_art, "output.txt")

# Use custom ASCII characters (from darkest to lightest)
custom_chars = ["@", "#", "O", "o", ".", " "]
generator = AsciiArtGenerator(chars=custom_chars, width=80)
```

### Enhanced Python API

The enhanced module provides advanced features like image processing options, HTML output with color preservation, and Unicode character modes.

```python
from ashiart import EnhancedAsciiArtGenerator, image_to_enhanced_ascii, image_to_html_ascii

# Basic enhanced usage
generator = EnhancedAsciiArtGenerator(width=80, mode="standard")
ascii_art = generator.generate_from_image("docs/images/example.jpg")
print(ascii_art)

# Apply image enhancements
generator.set_enhancement(
    contrast=1.5,       # Increase contrast
    brightness=1.1,     # Brighten slightly
    edge_enhance=True,  # Enhance edges
    dithering=True      # Apply dithering
)
ascii_art = generator.generate_from_image("docs/images/example.jpg")

# Use different rendering modes
# Standard ASCII characters
generator = EnhancedAsciiArtGenerator(width=80, mode="standard")

# Dense character set (70+ characters for more gradients)
generator = EnhancedAsciiArtGenerator(width=80, mode="dense")

# Unicode block characters
generator = EnhancedAsciiArtGenerator(width=80, mode="blocks")

# Unicode braille patterns (higher resolution)
generator = EnhancedAsciiArtGenerator(width=40, mode="braille")

# Generate HTML output with preserved colors
html = generator.generate_html(
    "docs/images/example.jpg",
    preserve_color=True,
    font_size=8
)
generator.save_html_to_file(html, "output.html")

# Convenience functions
ascii_art = image_to_enhanced_ascii(
    "docs/images/sample.jpg",
    width=80,
    mode="dense",
    contrast=1.3,
    edge_enhance=True
)

html = image_to_html_ascii(
    "docs/images/example.jpg",
    width=80,
    preserve_color=True
)
```

## Examples

Check out the [examples directory](examples/) for more detailed usage examples.

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/Faycall1l/Ashiart.git
cd ashiart

# Install in development mode
pip install -e .
```

### Testing

Run the tests with pytest:

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 