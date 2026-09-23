"""Image loading from local paths and URLs."""

import io
import os
import urllib.request

from PIL import Image

_USER_AGENT = "ashiart"


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
        return image
    if not os.path.exists(source):
        raise FileNotFoundError(f"Image file not found: {source}")
    try:
        return Image.open(source)
    except Exception as error:
        raise ValueError(f"Error opening image: {error}")
