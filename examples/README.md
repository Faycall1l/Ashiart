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

If you run the examples without providing an image path, most examples will generate a test image automatically.

## Example Output

The examples save their output to various files, which you can examine to see the different ASCII art styles and options. The enhanced demo in particular creates a `demo_outputs` directory with various formats and styles to explore. 