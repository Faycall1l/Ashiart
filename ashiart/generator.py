"""ASCII Art Generator module."""

import os
from PIL import Image, ImageOps


class AsciiArtGenerator:
    """A class to generate ASCII art from images."""

    # ASCII characters from darkest to lightest (trailing space = paper white,
    # per the canonical density ramps: Bourke, "@%#*+=-:. ", etc.)
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]

    # Monospace glyphs are ~2x taller than wide; sample half as many rows.
    ASPECT_CORRECTION = 0.5

    def __init__(self, chars=None, width=100, height=None, autocontrast=True):
        """
        Initialize the ASCII art generator.
        
        Args:
            chars (list, optional): ASCII characters from darkest to lightest. 
                                    Defaults to None.
            width (int, optional): Width of output ASCII art. Defaults to 100.
            height (int, optional): Height of output ASCII art. Defaults to None.
            autocontrast (bool, optional): Stretch gray levels to use the full
                ramp (ImageOps.autocontrast). Defaults to True.
        """
        self.chars = chars or self.ASCII_CHARS
        self.width = width
        self.height = height
        self.autocontrast = autocontrast

    def _resize_image(self, image):
        """
        Resize image to the specified width and height.
        
        Args:
            image (PIL.Image): The image to resize.
            
        Returns:
            PIL.Image: The resized image.
        """
        width = self.width
        height = self.height or int(image.height * width / image.width * self.ASPECT_CORRECTION)
        # LANCZOS: highest-quality downsampling; NEAREST (the default)
        # aliases high-frequency detail into noise at char resolution.
        return image.resize((width, height), Image.LANCZOS)

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
        
        # Split the pixel list into rows
        for i in range(0, len(pixels), width):
            row = pixels[i:i + width]
            ascii_row = []
            
            for pixel in row:
                # Map pixel value (0-255) to a ramp index; round (not trunc)
                # so each character owns a symmetric brightness bucket.
                index = round(pixel * (len(self.chars) - 1) / 255)
                index = max(0, min(index, len(self.chars) - 1))
                ascii_row.append(self.chars[index])
            
            ascii_image.append(ascii_row)
        
        return ascii_image

    def generate_from_image(self, image_path, color=False):
        """
        Generate ASCII art from an image file.
        
        Args:
            image_path (str): Path to the image file.
            color (bool, optional): Wrap characters in ANSI truecolor codes
                sampled from the original image. Defaults to False.
            
        Returns:
            str: ASCII art as a string.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            image = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"Error opening image: {e}")
        
        if color:
            return self.generate_ansi_from_pil_image(image)

        # Process the image
        image = self._resize_image(image)
        grayscale_image = self._convert_to_grayscale(image)
        ascii_image = self._map_pixels_to_ascii(grayscale_image)
        
        # Convert 2D list to string
        return "\n".join("".join(row) for row in ascii_image)

    def generate_from_pil_image(self, image, color=False):
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
        # Process the image
        image = self._resize_image(image)
        grayscale_image = self._convert_to_grayscale(image)
        ascii_image = self._map_pixels_to_ascii(grayscale_image)
        
        # Convert 2D list to string
        return "\n".join("".join(row) for row in ascii_image)

    def generate_ansi_from_pil_image(self, image):
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
        color_image = self._resize_image(image.convert("RGB"))
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

    def save_to_file(self, ascii_art, output_path):
        """
        Save ASCII art to a file.
        
        Args:
            ascii_art (str): The ASCII art to save.
            output_path (str): Path to save the ASCII art.
        """
        with open(output_path, "w") as file:
            file.write(ascii_art)


def image_to_ascii(image_path, width=100, height=None, chars=None):
    """
    Convenience function to convert an image to ASCII art.
    
    Args:
        image_path (str): Path to the image file.
        width (int, optional): Width of output ASCII art. Defaults to 100.
        height (int, optional): Height of output ASCII art. Defaults to None.
        chars (list, optional): ASCII characters from darkest to lightest. 
                               Defaults to None.
        
    Returns:
        str: ASCII art as a string.
    """
    generator = AsciiArtGenerator(chars=chars, width=width, height=height)
    return generator.generate_from_image(image_path) 