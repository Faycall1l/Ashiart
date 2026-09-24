"""ASCII Art Generator Package."""

from .generator import AsciiArtGenerator

try:
    from .enhanced import (
        EnhancedAsciiArtGenerator,
        image_to_ascii,
        image_to_html_ascii,
    )

    HAS_ENHANCED = True
except ImportError:
    # Numpy missing: fall back to the baseline generator.
    HAS_ENHANCED = False

    def image_to_ascii(  # type: ignore[misc]
        image_path, width=100, height=None, chars=None, **kwargs
    ):
        """Convert an image to ASCII art (baseline fallback, no numpy)."""
        generator = AsciiArtGenerator(chars=chars, width=width, height=height)
        return generator.generate_from_image(image_path)


__version__ = "0.2.0"
__all__ = ["AsciiArtGenerator", "image_to_ascii"]

if HAS_ENHANCED:
    __all__ += ["EnhancedAsciiArtGenerator", "image_to_html_ascii"]
