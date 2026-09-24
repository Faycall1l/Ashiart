"""Image loading, orientation, and alpha flattening."""

from __future__ import annotations

import io
import os
import urllib.request

from PIL import Image, ImageDraw, ImageOps

_USER_AGENT = "ashiart"
_FLAT_BACKGROUND = (255, 255, 255)


def flatten_alpha(
    image: Image.Image, background: tuple[int, int, int] = _FLAT_BACKGROUND
) -> Image.Image:
    """Composite transparent pixels onto an opaque background.

    RGBA, LA, and paletted images carrying transparency are flattened;
    anything else passes through untouched.

    Args:
        image (PIL.Image): The decoded image.
        background (tuple): RGB backdrop for transparent pixels.

    Returns:
        PIL.Image: Opaque RGB image, or the input unchanged.
    """
    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        alpha = image.convert("RGBA").split()[-1]
        base = Image.new("RGBA", image.size, (*background, 255))
        base.paste(image, mask=alpha)
        return base.convert("RGB")
    return image


def apply_exif_orientation(image: Image.Image) -> Image.Image:
    """Rotate the image per its EXIF orientation tag, if present.

    Phone photos are stored unrotated with an orientation flag; without
    this they convert sideways. Images without the tag pass through.

    Args:
        image (PIL.Image): The decoded image.

    Returns:
        PIL.Image: Correctly oriented image.
    """
    return ImageOps.exif_transpose(image)


def prepare_image(image: Image.Image) -> Image.Image:
    """Orient then flatten: the common entry for all decode paths.

    Args:
        image (PIL.Image): The decoded image.

    Returns:
        PIL.Image: Oriented, opaque RGB-ready image.
    """
    return flatten_alpha(apply_exif_orientation(image))


def demo_image(size: tuple[int, int] = (240, 120)) -> Image.Image:
    """Procedural calibration image: luma gradient, disc, bars, diagonal.

    Exercises the full ramp plus straight and curved contours with no
    input files involved.

    Args:
        size (tuple): Pixel dimensions.

    Returns:
        PIL.Image: RGB test image.
    """
    width, height = size
    gradient = Image.new("L", size)
    gradient.putdata(
        [int(255 * x / (width - 1)) for y in range(height) for x in range(width)]
    )
    image = gradient.convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.ellipse(
        [(width // 4, height // 6), (width // 2, height - height // 6)],
        fill=(0, 0, 0),
    )
    draw.rectangle(
        [(width // 2 + 10, height // 3), (width - 10, 2 * height // 3)],
        fill=(255, 255, 255),
    )
    draw.line([(0, height - 1), (width - 1, 0)], fill=(128, 128, 128), width=3)
    return image


def open_raw(source: str | bytes | bytearray, timeout: float = 15) -> Image.Image:
    """Decode an image without orientation or flattening.

    Unlike open_image, the result stays seekable, so GIF frames can be
    iterated. Callers own orientation handling for multi-frame sources.

    Args:
        source (str or bytes): Filesystem path, raw image bytes, or URL.
        timeout (float): Download timeout in seconds; URLs only.

    Raises:
        FileNotFoundError: Local path does not exist.
        ValueError: Download failed or bytes do not decode as an image.

    Returns:
        PIL.Image: The decoded image.
    """
    if isinstance(source, (bytes, bytearray)):
        try:
            image = Image.open(io.BytesIO(source))
            image.load()
        except Exception as error:
            raise ValueError(f"Bytes are not an image: {error}") from error
        return image
    if isinstance(source, str) and source.startswith(("http://", "https://")):
        request = urllib.request.Request(source, headers={"User-Agent": _USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read()
        except Exception as error:
            raise ValueError(f"Could not download image: {error}") from error
        try:
            return Image.open(io.BytesIO(data))
        except Exception as error:
            raise ValueError(f"Downloaded bytes are not an image: {error}") from error
    if not os.path.exists(source):
        raise FileNotFoundError(f"Image file not found: {source}")
    try:
        return Image.open(source)
    except Exception as error:
        raise ValueError(f"Error opening image: {error}") from error


def open_image(source: str | bytes | bytearray, timeout: float = 15) -> Image.Image:
    """Open a PIL image from a local path, bytes, or an http(s) URL.

    Args:
        source (str or bytes): Filesystem path, raw image bytes
            (e.g. piped stdin), or http(s) URL.
        timeout (float): Download timeout in seconds; URLs only.

    Raises:
        FileNotFoundError: Local path does not exist.
        ValueError: Download failed or bytes do not decode as an image.

    Returns:
        PIL.Image: Oriented, opaque RGB-ready image.
    """
    try:
        return prepare_image(open_raw(source, timeout))
    except (FileNotFoundError, ValueError):
        raise
    except Exception as error:
        raise ValueError(f"Error opening image: {error}") from error
