"""Single-ramp image-to-ASCII conversion.

Exports AsciiArtGenerator, the NumPy-free converter used directly and
as the fallback when enhanced dependencies are unavailable.
"""

from __future__ import annotations

from typing import ClassVar

from PIL import Image, ImageOps

from .io import open_image, prepare_image


class AsciiArtGenerator:
    """A class to generate ASCII art from images."""

    # ASCII characters from darkest to lightest (trailing space = paper white,
    # per the canonical density ramps: Bourke, "@%#*+=-:. ", etc.)
    ASCII_CHARS: ClassVar[list] = [
        "@",
        "#",
        "S",
        "%",
        "?",
        "*",
        "+",
        ";",
        ":",
        ",",
        ".",
        " ",
    ]

    # Monospace glyphs are ~2x taller than wide; sample half as many rows.
    ASPECT_CORRECTION: ClassVar[float] = 0.5

    RESAMPLE_FILTERS: ClassVar[dict] = {
        "lanczos": Image.Resampling.LANCZOS,
        "box": Image.Resampling.BOX,
    }

    def __init__(
        self,
        chars: list[str] | None = None,
        width: int = 100,
        height: int | None = None,
        autocontrast: bool = True,
        resample: str = "lanczos",
        gamma: float = 1.0,
    ):
        """
        Initialize the ASCII art generator.

        Args:
            chars (list, optional): ASCII characters from darkest to lightest.
                                    Defaults to None.
            width (int, optional): Width of output ASCII art. Defaults to 100.
            height (int, optional): Height of output ASCII art. Defaults to None.
            autocontrast (bool, optional): Stretch gray levels to use the full
                ramp (ImageOps.autocontrast). Defaults to True.
            resample (str, optional): Downsampling filter: "lanczos" (sharp)
                or "box" (area average). Defaults to "lanczos".
            gamma (float, optional): Tonal curve exponent applied to gray
                levels (>1 darkens midtones). Defaults to 1.0.
        """
        if resample not in self.RESAMPLE_FILTERS:
            raise ValueError(f"Unknown resample filter: {resample}")
        if gamma <= 0:
            raise ValueError(f"Gamma must be positive: {gamma}")
        self.chars = chars or self.ASCII_CHARS
        self.width = width
        self.height = height
        self.autocontrast = autocontrast
        self.resample = resample
        self.gamma = gamma

    def _resize_image(self, image):
        """
        Resize image to the specified width and height.

        Args:
            image (PIL.Image): The image to resize.

        Returns:
            PIL.Image: The resized image.
        """
        width = self.width
        height = self.height or int(
            image.height * width / image.width * self.ASPECT_CORRECTION
        )
        # LANCZOS: highest-quality downsampling; NEAREST (the default)
        # aliases high-frequency detail into noise at char resolution.
        return image.resize((width, height), self.RESAMPLE_FILTERS[self.resample])

    def _convert_to_grayscale(self, image):
        """
        Convert image to grayscale, stretching levels to the full ramp.

        Args:
            image (PIL.Image): The image to convert.

        Returns:
            PIL.Image: The grayscale image.
        """
        gray = image.convert("L")
        if self.autocontrast:
            gray = ImageOps.autocontrast(gray, cutoff=1)
        if self.gamma != 1.0:
            lut = [round(255 * (level / 255) ** self.gamma) for level in range(256)]
            gray = gray.point(lut)
        return gray

    def _map_pixels_to_ascii(self, image):
        """
        Map each pixel to an ASCII character.

        Args:
            image (PIL.Image): The grayscale image.

        Returns:
            list: 2D list of ASCII characters.
        """
        pixels = list(image.getdata())
        width = image.width
        ascii_image = []

        for i in range(0, len(pixels), width):
            row = pixels[i : i + width]
            ascii_row = []

            for pixel in row:
                # Round so buckets stay symmetric; clamp for short custom ramps.
                index = round(pixel * (len(self.chars) - 1) / 255)
                index = max(0, min(index, len(self.chars) - 1))
                ascii_row.append(self.chars[index])

            ascii_image.append(ascii_row)

        return ascii_image

    def generate_from_image(self, image_path: str | bytes, color: bool = False) -> str:
        """
        Generate ASCII art from an image file.

        Args:
            image_path (str): Local path or http(s) URL.
            color (bool, optional): Wrap characters in ANSI truecolor codes
                sampled after resizing. Defaults to False.

        Returns:
            str: ASCII art as a string.
        """
        image = open_image(image_path)

        if color:
            return self.generate_ansi_from_pil_image(image)

        image = self._resize_image(image)
        grayscale_image = self._convert_to_grayscale(image)
        ascii_image = self._map_pixels_to_ascii(grayscale_image)

        return "\n".join("".join(row) for row in ascii_image)

    def generate_from_pil_image(self, image: Image.Image, color: bool = False) -> str:
        """
        Generate ASCII art from a PIL Image object.

        Args:
            image (PIL.Image): PIL Image object.
            color (bool, optional): Wrap characters in ANSI truecolor codes.
                Defaults to False.

        Returns:
            str: ASCII art as a string.
        """
        if color:
            return self.generate_ansi_from_pil_image(image)
        image = self._resize_image(prepare_image(image))
        grayscale_image = self._convert_to_grayscale(image)
        ascii_image = self._map_pixels_to_ascii(grayscale_image)

        return "\n".join("".join(row) for row in ascii_image)

    def generate_ansi_from_pil_image(self, image: Image.Image) -> str:
        """
        Generate ANSI-colored ASCII art from a PIL Image object.

        Each character is wrapped in a truecolor foreground escape
        (``\\x1b[38;2;R;G;Bm``) sampled from the resized original image,
        reset with ``\\x1b[0m`` after every character.

        Args:
            image (PIL.Image): PIL Image object.

        Returns:
            str: ANSI-colored ASCII art.
        """
        color_image = self._resize_image(prepare_image(image).convert("RGB"))
        grayscale_image = self._convert_to_grayscale(color_image)
        ascii_image = self._map_pixels_to_ascii(grayscale_image)
        color_pixels = list(color_image.getdata())
        width = color_image.width

        lines = []
        for y, row in enumerate(ascii_image):
            parts = []
            for x, char in enumerate(row):
                r, g, b = color_pixels[y * width + x][:3]
                parts.append(f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m")
            lines.append("".join(parts))
        return "\n".join(lines)

    def save_to_file(self, ascii_art: str, output_path: str) -> None:
        """
        Save ASCII art to a file.

        Args:
            ascii_art (str): The ASCII art to save.
            output_path (str): Path to save the ASCII art.
        """
        with open(output_path, "w") as file:
            file.write(ascii_art)
