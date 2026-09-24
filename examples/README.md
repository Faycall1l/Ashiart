# AshiArt Examples

This directory contains examples demonstrating how to use the AshiArt package.

## Basic Usage Examples

- `basic_usage.py`: Demonstrates the basic features of the standard ASCII art generator
- `enhanced_demo.py`: Demonstrates the enhanced features including different rendering modes and HTML output

## Running the Examples

Make sure you have the ashiart package installed:

```bash
# Install from source
pip install -e ..
```

You can run any example by providing an image path:

```bash
# Basic usage example
python basic_usage.py path/to/image.jpg

# Enhanced features demo
python enhanced_demo.py path/to/image.jpg
```

If you run `basic_usage.py` without an image path, it generates a test
image automatically. `enhanced_demo.py` requires an image path argument.

## Example Output

`basic_usage.py` prints to stdout and writes `output.txt`.
`enhanced_demo.py` writes a `demo_outputs/` directory: one text file per
rendering mode and enhancement combination (`demo_standard*.txt`,
`demo_dense.txt`, `demo_blocks.txt`, `demo_braille.txt`), color-preserving
HTML renders (`demo_color*.html`), and an `index.html` gallery page
stitching them together. `examples/benchmark.py` reports render
throughput per mode and width. 