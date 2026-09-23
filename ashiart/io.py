"""Image loading from local paths and URLs."""

import io
import os
import urllib.request

from PIL import Image

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


def open_image(source, timeout=15):
    """Open a PIL image from a local path or an http(s) URL.

    Args:
        source (str): Filesystem path or http(s) URL.
        timeout (float): Download timeout in seconds; URLs only.

    Raises:
        FileNotFoundError: Local path does not exist.
        ValueError: Download failed or bytes do not decode as an image.

    Returns:
        PIL.Image: The decoded image.
    """
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
        return flatten_alpha(image)
    if not os.path.exists(source):
        raise FileNotFoundError(f"Image file not found: {source}")
    try:
        return flatten_alpha(Image.open(source))
    except Exception as error:
        raise ValueError(f"Error opening image: {error}")
