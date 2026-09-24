# API Reference

Generated from docstrings by `scripts/gen_api.py`. The package version is defined in `ashiart/__init__.py`.

## `ashiart.generator` — Baseline converter

### `AsciiArtGenerator(chars: 'list[str] | None' = None, width: 'int' = 100, height: 'int | None' = None, autocontrast: 'bool' = True, resample: 'str' = 'lanczos', gamma: 'float' = 1.0)`

A class to generate ASCII art from images.

## `ashiart.enhanced` — Modes, enhancements, HTML

### `EnhancedAsciiArtGenerator(chars: 'list[str] | None' = None, width: 'int' = 100, height: 'int | None' = None, mode: 'str' = 'standard', resample: 'str' = 'lanczos')`

Image-to-ASCII converter with modes, tonal controls, and edge overlay.

### `image_to_ascii(image_path: 'str | bytes', width: 'int' = 100, height: 'int | None' = None, mode: 'str' = 'standard', chars: 'list[str] | None' = None, resample: 'str' = 'lanczos', contrast: 'float' = 1.0, brightness: 'float' = 1.0, sharpness: 'float' = 1.0, gamma: 'float' = 1.0, autocontrast: 'bool' = True, dithering: 'bool' = False, edge_enhance: 'bool' = False, edges: 'bool' = False, edge_threshold: 'float' = 0.35, clahe: 'bool' = False, dog: 'tuple[float, float, float] | None' = None, invert: 'bool' = False, ansi: 'bool' = False, cache: 'bool' = True) -> 'str'`

Convert an image to ASCII art (single entry point).

### `image_to_html_ascii(image_path: 'str | bytes', width: 'int' = 100, height: 'int | None' = None, mode: 'str' = 'dense', preserve_color: 'bool' = True, font_size: 'int' = 8, font_family: 'str' = 'monospace', bg: 'str' = 'black', contrast: 'float' = 1.2, brightness: 'float' = 1.0, dithering: 'bool' = False, edge_enhance: 'bool' = True, invert: 'bool' = False, cache: 'bool' = True) -> 'str'`

Convenience function to convert an image to HTML ASCII art with color.

## `ashiart.animate` — Terminal animation

### `fit_to_terminal(width: 'int | None' = None, height: 'int | None' = None, aspect: 'float' = 0.5) -> 'tuple[int, int | None]'`

Resolve playback dimensions against the terminal size.

### `iter_gif_frames(source: 'str | bytes') -> 'list[tuple[Image.Image, int]]'`

Split an animated image into (RGB frame, duration_ms) pairs.

### `play_animation(frames: 'list[str]', frame_ms: 'int | float | list[int]' = 100, loops: 'int' = 0, max_fps: 'float' = 30, output: 'IO[str] | None' = None, sleeper: 'Callable[[float], None] | None' = None) -> 'int'`

Print ASCII frames as a looping terminal animation.

### `save_animation_html(frames: 'list[str]', output_path: 'str', frame_ms: 'int | float | list[int]' = 100, font_size: 'int' = 10, font_family: 'str' = 'monospace', bg: 'str' = 'black') -> 'str'`

Write frames as a self-contained looping HTML animation.

## `ashiart.video` — Video and webcam input (extra)

### `iter_video_frames(path: 'str', max_frames: 'int | None' = None) -> 'Iterator[tuple[Image.Image, int]]'`

Yield (RGB frame, duration_ms) pairs from a video file.

### `iter_webcam_frames(index: 'int' = 0, mirror: 'bool' = True) -> 'Iterator[Image.Image]'`

Yield RGB frames from a webcam until the generator is closed.

## `ashiart.tonal` — Tonal operators

### `apply_clahe(gray: 'Image.Image', tiles: 'int' = 8, clip: 'float' = 2.0) -> 'Image.Image'`

Contrast-limited adaptive histogram equalization.

### `apply_dog(gray: 'Image.Image', small: 'float' = 0.8, large: 'float' = 2.0, amplify: 'float' = 2.0) -> 'Image.Image'`

Difference-of-Gaussians detail emphasis.

## `ashiart.io` — Loading, orientation, flattening

### `apply_exif_orientation(image: 'Image.Image') -> 'Image.Image'`

Rotate the image per its EXIF orientation tag, if present.

### `demo_image(size: 'tuple[int, int]' = (240, 120)) -> 'Image.Image'`

Procedural calibration image: luma gradient, disc, bars, diagonal.

### `download_image(url: 'str', timeout: 'float' = 15, cache: 'bool' = True) -> 'bytes'`

Fetch URL bytes with a disk cache and one transient-error retry.

### `flatten_alpha(image: 'Image.Image', background: 'tuple[int, int, int]' = (255, 255, 255)) -> 'Image.Image'`

Composite transparent pixels onto an opaque background.

### `open_image(source: 'str | bytes | bytearray', timeout: 'float' = 15, cache: 'bool' = True) -> 'Image.Image'`

Open a PIL image from a local path, bytes, or an http(s) URL.

### `open_raw(source: 'str | bytes | bytearray', timeout: 'float' = 15, cache: 'bool' = True) -> 'Image.Image'`

Decode an image without orientation or flattening.

### `prepare_image(image: 'Image.Image') -> 'Image.Image'`

Orient then flatten: the common entry for all decode paths.

## `ashiart.cli` — Command-line interface

### `build_parser() -> 'argparse.ArgumentParser'`

Build the argument parser.

### `main(argv: 'list[str] | None' = None) -> 'int'`

Run the command-line interface.
