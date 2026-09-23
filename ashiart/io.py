"""Image loading, orientation, and alpha flattening."""

import io
import os
import urllib.request

from PIL import Image, ImageOps

_USER_AGENT = "ashiart"
_FLAT_BACKGROUND = (255, 255, 255)


def flatten_alpha(image, background=_FLAT_BACKGROUND):
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
        base = Image.new("RGBA", image.size, background + (255,))
        base.paste(image, mask=alpha)
        return base.convert("RGB")
    return image


def apply_exif_orientation(image):
    """Rotate the image per its EXIF orientation tag, if present.

    Phone photos are stored unrotated with an orientation flag; without
    this they convert sideways. Images without the tag pass through.

    Args:
        image (PIL.Image): The decoded image.

    Returns:
        PIL.Image: Correctly oriented image.
    """
    return ImageOps.exif_transpose(image)


def prepare_image(image):
    """Orient then flatten: the common entry for all decode paths.

    Args:
        image (PIL.Image): The decoded image.

    Returns:
        PIL.Image: Oriented, opaque RGB-ready image.
    """
    return flatten_alpha(apply_exif_orientation(image))


def open_image(source, timeout=15):
    """Open a PIL image from a local path, bytes, or an http(s) URL.

    Args:
        source (str or bytes): Filesystem path, raw image bytes
            (e.g. piped stdin), or http(s) URL.
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
            raise ValueError(f"Bytes are not an image: {error}")
        return prepare_image(image)
    if isinstance(source, str) and source.startswith(("http://", "https://")):
        request = urllib.request.Request(source, headers={"User-Agent": _USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                data = response.read()
        except Exception as error:
            raise ValueError(f"Could not download image: {error}")
        try:
            image = Image.open(io.BytesIO(data))
            image.load()
        except Exception as error:
            raise ValueError(f"Downloaded bytes are not an image: {error}")
        return prepare_image(image)
    if not os.path.exists(source):
        raise FileNotFoundError(f"Image file not found: {source}")
    try:
        return prepare_image(Image.open(source))
    except Exception as error:
        raise ValueError(f"Error opening image: {error}")
