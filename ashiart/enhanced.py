"""Rendering modes, tonal controls, and Sobel edge overlay for ASCII art.

Exports EnhancedAsciiArtGenerator, the image_to_ascii entry point,
and the image_to_html_ascii HTML helper.
"""

import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

from .io import open_image, prepare_image


class EnhancedAsciiArtGenerator:
    """Image-to-ASCII converter with modes, tonal controls, and edge overlay."""

    # Default ASCII characters from darkest to lightest (trailing space =
    # paper white, matching the canonical density ramps)
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]
    
    # High-density character set, ordered by measured ink coverage
    # (darkest to lightest) so each step is a true tonal increase
    DENSE_CHARS = list('MW@%$BmwQ8O&0bdpqUChXkoaZ#nuYcxLzvJ?f1jtl[]{}Ir|!><(^*i/)+\\";~:_\'-.` ')
    
    # Unicode block characters for higher resolution
    BLOCK_CHARS = ["█", "▓", "▒", "░", " "]
    
    # Unicode braille patterns (can represent 8 pixels per character)
    BRAILLE_CHARS = [chr(0x2800 + i) for i in range(256)]

    def __init__(self, chars=None, width=100, height=None, mode="standard",
                 resample="lanczos"):
        """
        Initialize the enhanced ASCII art generator.
        
        Args:
            chars (list, optional): ASCII characters from darkest to lightest. 
                                    Defaults to None.
            width (int, optional): Width of output ASCII art. Defaults to 100.
            height (int, optional): Height of output ASCII art. Defaults to None.
            mode (str, optional): Rendering mode. Options: "standard", "dense", 
                                 "blocks", "braille". Defaults to "standard".
            resample (str, optional): Downsampling filter: "lanczos" (sharp)
                or "box" (area average). Defaults to "lanczos".
        """
        if resample not in ("lanczos", "box"):
            raise ValueError(f"Unknown resample filter: {resample}")
        self.mode = mode
        if chars is not None:
            self.chars = chars
        elif mode == "standard":
            self.chars = self.ASCII_CHARS
        elif mode == "dense":
            self.chars = self.DENSE_CHARS
        elif mode == "blocks":
            self.chars = self.BLOCK_CHARS
        elif mode == "braille":
            self.chars = self.BRAILLE_CHARS
        else:
            self.chars = self.ASCII_CHARS
            
        self.width = width
        self.height = height
        self.resample = resample
        
        # Image enhancement parameters
        self.contrast = 1.0
        self.brightness = 1.0
        self.sharpness = 1.0
        self.gamma = 1.0
        self.autocontrast = True
        self.dithering = False
        self.edge_enhance = False
        self.edges = False
        self.edge_threshold = 0.35
        self.invert = False

    def set_enhancement(self, contrast=None, brightness=None, sharpness=None, 
                        gamma=None, autocontrast=None, dithering=None,
                        edge_enhance=None, edges=None, edge_threshold=None,
                        invert=None):
        """
        Set image enhancement parameters.
        
        Args:
            contrast (float, optional): Contrast adjustment (1.0 is neutral). 
            brightness (float, optional): Brightness adjustment (1.0 is neutral).
            sharpness (float, optional): Sharpness adjustment (1.0 is neutral).
            gamma (float, optional): Tonal curve exponent (>1 darkens
                midtones). Defaults to 1.0.
            autocontrast (bool, optional): Stretch gray levels to the full
                ramp before mapping.
            dithering (bool, optional): Whether to apply dithering.
            edge_enhance (bool, optional): Whether to enhance edges.
            edges (bool, optional): Overlay directional edge glyphs
                (Sobel orientation) on strong contours.
            edge_threshold (float, optional): Normalized Sobel magnitude
                (0-1) above which a cell becomes an edge glyph.
            invert (bool, optional): Whether to invert the image.
        """
        if contrast is not None:
            self.contrast = contrast
        if brightness is not None:
            self.brightness = brightness
        if sharpness is not None:
            self.sharpness = sharpness
        if gamma is not None:
            if gamma <= 0:
                raise ValueError(f"Gamma must be positive: {gamma}")
            self.gamma = gamma
        if autocontrast is not None:
            self.autocontrast = autocontrast
        if dithering is not None:
            self.dithering = dithering
        if edge_enhance is not None:
            self.edge_enhance = edge_enhance
        if edges is not None:
            self.edges = edges
        if edge_threshold is not None:
            self.edge_threshold = edge_threshold
        if invert is not None:
            self.invert = invert

    def _resample_filter(self):
        """PIL filter selected by the resample option."""
        return Image.LANCZOS if self.resample == "lanczos" else Image.BOX

    def _resize_image(self, image):
        """
        Resize image to the specified width and height.
        
        Args:
            image (PIL.Image): The image to resize.
            
        Returns:
            PIL.Image: The resized image.
        """
        if self.mode == "braille":
            # For braille, we want 4x the width and 2x the height for proper mapping
            width = self.width * 2
            height = self.height * 4 if self.height else int(image.height * width / image.width / 1.25)
            return image.resize((width, height), self._resample_filter())
        else:
            width = self.width
            height = self.height or int(image.height * width / image.width * 0.5)
            return image.resize((width, height), self._resample_filter())

    def _enhance_image(self, image):
        """
        Apply various image enhancements.
        
        Args:
            image (PIL.Image): The image to enhance.
            
        Returns:
            PIL.Image: The enhanced image.
        """
        # Apply contrast adjustment
        if self.contrast != 1.0:
            image = ImageEnhance.Contrast(image).enhance(self.contrast)
        
        # Apply brightness adjustment
        if self.brightness != 1.0:
            image = ImageEnhance.Brightness(image).enhance(self.brightness)
        
        # Apply sharpness adjustment
        if self.sharpness != 1.0:
            image = ImageEnhance.Sharpness(image).enhance(self.sharpness)
        
        # Apply edge enhancement
        if self.edge_enhance:
            image = image.filter(ImageFilter.EDGE_ENHANCE)
        
        # Apply inversion
        if self.invert:
            image = ImageOps.invert(image)
        
        return image

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

    def _compute_edge_grid(self, grayscale_image):
        """
        Sobel edge-orientation grid for the char cells.

        Cells whose normalized gradient magnitude reaches
        ``edge_threshold`` get a directional glyph (``- / | \\``)
        matching the contour direction; other cells get None and keep
        their density character. Returns None when edge overlay is
        disabled, in braille mode, or on degenerate sizes.
        """
        if not self.edges or self.mode == "braille":
            return None
        a = np.asarray(grayscale_image, dtype=np.float64)
        if a.shape[0] < 3 or a.shape[1] < 3:
            return None

        gx = (a[:-2, 2:] + 2 * a[1:-1, 2:] + a[2:, 2:]
              - a[:-2, :-2] - 2 * a[1:-1, :-2] - a[2:, :-2])
        gy = (a[2:, :-2] + 2 * a[2:, 1:-1] + a[2:, 2:]
              - a[:-2, :-2] - 2 * a[:-2, 1:-1] - a[:-2, 2:])
        mag = np.pad(np.hypot(gx, gy), 1)
        peak = mag.max()
        if peak == 0:
            return None
        norm = mag / peak
        # Gradient is perpendicular to the contour: rotate 90 degrees,
        # fold into [0, 180), then snap to the nearest glyph axis.
        ang = np.pad((np.degrees(np.arctan2(gy, gx)) + 90.0) % 180.0, 1)

        grid = []
        for y in range(a.shape[0]):
            row = []
            for x in range(a.shape[1]):
                if norm[y, x] >= self.edge_threshold:
                    t = ang[y, x]
                    if t < 22.5 or t >= 157.5:
                        row.append("-")
                    elif t < 67.5:
                        row.append("/")
                    elif t < 112.5:
                        row.append("|")
                    else:
                        row.append("\\")
                else:
                    row.append(None)
            grid.append(row)
        return grid

    @staticmethod
    def _overlay_edges(ascii_image, edge_grid):
        """Substitute edge glyphs where the edge grid is set."""
        if edge_grid is None:
            return ascii_image
        return [[e if e is not None else c for c, e in zip(arow, erow)]
                for arow, erow in zip(ascii_image, edge_grid)]

    def _apply_dithering(self, image):
        """
        Apply Floyd-Steinberg dithering to the image.
        
        Args:
            image (PIL.Image): The grayscale image.
            
        Returns:
            PIL.Image: The dithered image.
        """
        if not self.dithering:
            return image
        
        # For true dithering, we need to use a 1-bit image with dithering
        # But for our ASCII art, we'll simulate it by using PIL's built-in dithering
        return image.convert("1").convert("L")

    def _map_pixels_to_ascii_standard(self, image):
        """
        Map each pixel to an ASCII character using standard mapping.
        
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

    def _map_pixels_to_ascii_braille(self, image):
        """
        Map pixels to braille characters (each braille character represents a 2x4 grid).
        
        Args:
            image (PIL.Image): The grayscale image.
            
        Returns:
            list: 2D list of braille characters.
        """
        pixels = np.array(image)
        height, width = pixels.shape
        
        # Calculate output dimensions
        out_height = height // 4
        out_width = width // 2
        
        ascii_image = []
        
        # Process 2x4 blocks of pixels
        for y in range(0, out_height):
            ascii_row = []
            for x in range(0, out_width):
                # Extract 2x4 block
                block = pixels[y*4:y*4+4, x*2:x*2+2]
                
                # Convert to binary (threshold at 128)
                binary_block = (block < 128).flatten()
                
                # Calculate braille pattern
                # Braille dot pattern:
                # 0 3
                # 1 4
                # 2 5
                # 6 7
                pattern = 0
                for i, bit in enumerate(binary_block):
                    if bit:
                        if i < 6:
                            pattern |= (1 << i)
                        else:
                            # Positions 6 and 7 are mapped to bits 6 and 7 in Unicode
                            pattern |= (1 << (i + 2))
                
                # Map to corresponding braille character
                braille_char = chr(0x2800 + pattern)
                ascii_row.append(braille_char)
            
            ascii_image.append(ascii_row)
        
        return ascii_image

    def _map_pixels_to_ascii(self, image):
        """
        Map pixels to ASCII characters based on the selected mode.
        
        Args:
            image (PIL.Image): The grayscale image.
            
        Returns:
            list: 2D list of characters.
        """
        if self.mode == "braille":
            return self._map_pixels_to_ascii_braille(image)
        else:
            return self._map_pixels_to_ascii_standard(image)

    def generate_from_image(self, image_path, ansi=False):
        """
        Generate ASCII art from an image file.
        
        Args:
            image_path (str): Local path or http(s) URL.
            ansi (bool, optional): Wrap characters in ANSI truecolor codes.
                Defaults to False.
            
        Returns:
            str: ASCII art as a string.
        """
        image = open_image(image_path)

        if ansi:
            return self.generate_ansi_from_pil_image(image)
        
        image = self._resize_image(image)
        image = self._enhance_image(image)
        grayscale_image = self._convert_to_grayscale(image)
        edge_grid = self._compute_edge_grid(grayscale_image)
        
        if self.dithering:
            grayscale_image = self._apply_dithering(grayscale_image)
        
        ascii_image = self._map_pixels_to_ascii(grayscale_image)
        ascii_image = self._overlay_edges(ascii_image, edge_grid)
        
        return "\n".join("".join(row) for row in ascii_image)

    def generate_from_pil_image(self, image, ansi=False):
        """
        Generate ASCII art from a PIL Image object.
        
        Args:
            image (PIL.Image): PIL Image object.
            ansi (bool, optional): Wrap characters in ANSI truecolor codes.
                Defaults to False.
            
        Returns:
            str: ASCII art as a string.
        """
        if ansi:
            return self.generate_ansi_from_pil_image(image)
        image = self._resize_image(prepare_image(image))
        image = self._enhance_image(image)
        grayscale_image = self._convert_to_grayscale(image)
        edge_grid = self._compute_edge_grid(grayscale_image)
        
        if self.dithering:
            grayscale_image = self._apply_dithering(grayscale_image)
        
        ascii_image = self._map_pixels_to_ascii(grayscale_image)
        ascii_image = self._overlay_edges(ascii_image, edge_grid)
        
        return "\n".join("".join(row) for row in ascii_image)

    def generate_ansi_from_pil_image(self, image):
        """
        Generate ANSI-colored ASCII art from a PIL Image object.

        Truecolor is sampled from the resized (and enhanced) image.
        In braille mode the color is the mean of each 2x4 block.

        Args:
            image (PIL.Image): PIL Image object.

        Returns:
            str: ANSI-colored ASCII art.
        """
        resized = self._resize_image(prepare_image(image).convert("RGB"))
        enhanced = self._enhance_image(resized)
        grayscale = self._convert_to_grayscale(enhanced)
        edge_grid = self._compute_edge_grid(grayscale)
        if self.dithering:
            grayscale = self._apply_dithering(grayscale)

        ascii_image = self._map_pixels_to_ascii(grayscale)
        ascii_image = self._overlay_edges(ascii_image, edge_grid)
        color_arr = np.array(enhanced)

        lines = []
        if self.mode == "braille":
            h, w, _ = color_arr.shape
            for y, row in enumerate(ascii_image):
                parts = []
                for x, char in enumerate(row):
                    block = color_arr[y * 4:y * 4 + 4, x * 2:x * 2 + 2]
                    r, g, b = block.reshape(-1, 3).mean(axis=0).astype(int)
                    parts.append(f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m")
                lines.append("".join(parts))
        else:
            flat = color_arr.reshape(-1, 3)
            width = color_arr.shape[1]
            for y, row in enumerate(ascii_image):
                parts = []
                for x, char in enumerate(row):
                    r, g, b = flat[y * width + x]
                    parts.append(f"\x1b[38;2;{r};{g};{b}m{char}\x1b[0m")
                lines.append("".join(parts))
        return "\n".join(lines)

    def generate_html(self, image_path, font_size=10, font_family="monospace", 
                      preserve_color=False, bg="black"):
        """
        Generate HTML representation of the ASCII art with optional color.
        
        Args:
            image_path (str): Local path or http(s) URL.
            font_size (int, optional): Font size in pixels. Defaults to 10.
            font_family (str, optional): Font family. Defaults to "monospace".
            preserve_color (bool, optional): Whether to preserve the original colors.
                                           Defaults to False.
            bg (str, optional): Page background, "black" or "white".
                Defaults to "black".
        
        Returns:
            str: HTML string representing the ASCII art.
        """
        if bg not in ("black", "white"):
            raise ValueError(f"Background must be black or white: {bg}")
        fg = "white" if bg == "black" else "black"
        image = open_image(image_path)
        original_image = image.copy()
        
        image = self._resize_image(image)
        image = self._enhance_image(image)
        grayscale_image = self._convert_to_grayscale(image)
        edge_grid = self._compute_edge_grid(grayscale_image)
        
        if self.dithering:
            grayscale_image = self._apply_dithering(grayscale_image)
        
        if preserve_color:
            color_image = self._resize_image(original_image)
            color_pixels = np.array(color_image)
        
        gray_pixels = np.array(grayscale_image)
        
        # Generate HTML
        html = f"""<!DOCTYPE html>
<html>
<head>
<title>ASCII Art</title>
<style>
  pre {{
    font-family: {font_family};
    font-size: {font_size}px;
    line-height: 1;
    letter-spacing: 0;
    background-color: {bg};
    color: {fg};
    display: inline-block;
    padding: 10px;
  }}
  span {{ 
    display: inline-block; 
  }}
</style>
</head>
<body>
<pre>
"""
        
        height, width = gray_pixels.shape
        
        for y in range(height):
            for x in range(width):
                if edge_grid is not None and edge_grid[y][x] is not None:
                    char = edge_grid[y][x]
                else:
                    pixel_value = gray_pixels[y, x]
                    index = round(pixel_value * (len(self.chars) - 1) / 255)
                    index = max(0, min(index, len(self.chars) - 1))
                    char = self.chars[index]
                
                if preserve_color and len(color_pixels.shape) > 2:
                    r, g, b = color_pixels[y, x][:3]
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    html += f'<span style="color:{color}">{char}</span>'
                else:
                    html += char
            
            html += '\n'
        
        html += """</pre>
</body>
</html>"""
        
        return html

    def save_to_file(self, ascii_art, output_path):
        """
        Save ASCII art to a file.
        
        Args:
            ascii_art (str): The ASCII art to save.
            output_path (str): Path to save the ASCII art.
        """
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(ascii_art)

    def save_html_to_file(self, html, output_path):
        """
        Save HTML to a file.
        
        Args:
            html (str): The HTML to save.
            output_path (str): Path to save the HTML.
        """
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html)


# Convenience functions
def image_to_ascii(image_path, width=100, height=None, mode="standard",
                   chars=None, resample="lanczos", contrast=1.0, brightness=1.0,
                   sharpness=1.0, gamma=1.0,
                   autocontrast=True, dithering=False, edge_enhance=False,
                   edges=False, edge_threshold=0.35,
                   invert=False, ansi=False):
    """
    Convert an image to ASCII art (single entry point).
    
    Args:
        image_path (str): Local path, bytes, or http(s) URL.
        width (int, optional): Width of output ASCII art. Defaults to 100.
        height (int, optional): Height of output ASCII art. Defaults to None.
        mode (str, optional): Rendering mode. Options: "standard", "dense", 
                             "blocks", "braille". Defaults to "standard".
        chars (list, optional): Custom characters, darkest to lightest.
        resample (str, optional): "lanczos" or "box" downsampling.
        contrast (float, optional): Contrast adjustment (1.0 is neutral).
        brightness (float, optional): Brightness adjustment (1.0 is neutral).
        sharpness (float, optional): Sharpness adjustment (1.0 is neutral).
        gamma (float, optional): Tonal curve exponent (>1 darkens midtones).
        autocontrast (bool, optional): Stretch gray levels to the full ramp.
        dithering (bool, optional): Whether to apply dithering.
        edge_enhance (bool, optional): Whether to enhance edges.
        edges (bool, optional): Overlay directional edge glyphs on contours.
        edge_threshold (float, optional): Normalized Sobel magnitude gate.
        invert (bool, optional): Whether to invert the image.
        ansi (bool, optional): Wrap output in ANSI truecolor codes.
        
    Returns:
        str: ASCII art as a string.
    """
    generator = EnhancedAsciiArtGenerator(chars=chars, width=width,
                                        height=height, mode=mode,
                                        resample=resample)
    generator.set_enhancement(contrast=contrast, brightness=brightness, 
                            sharpness=sharpness, gamma=gamma,
                            autocontrast=autocontrast,
                            dithering=dithering, 
                            edge_enhance=edge_enhance, edges=edges,
                            edge_threshold=edge_threshold, invert=invert)
    return generator.generate_from_image(image_path, ansi=ansi)


def image_to_html_ascii(image_path, width=100, height=None, mode="dense", 
                      preserve_color=True, font_size=8, font_family="monospace",
                      bg="black", contrast=1.2, brightness=1.0, dithering=False, 
                      edge_enhance=True, invert=False):
    """
    Convenience function to convert an image to HTML ASCII art with color.
    
    Args:
        image_path (str): Path to the image file.
        width (int, optional): Width of output ASCII art. Defaults to 100.
        height (int, optional): Height of output ASCII art. Defaults to None.
        mode (str, optional): Rendering mode. Options: "standard", "dense", 
                             "blocks", "braille". Defaults to "dense".
        preserve_color (bool, optional): Whether to preserve original colors.
        font_size (int, optional): Font size in pixels. Defaults to 8.
        font_family (str, optional): Font family. Defaults to "monospace".
        bg (str, optional): Page background, "black" or "white".
        contrast (float, optional): Contrast adjustment (1.0 is neutral).
        brightness (float, optional): Brightness adjustment (1.0 is neutral).
        dithering (bool, optional): Whether to apply dithering.
        edge_enhance (bool, optional): Whether to enhance edges.
        invert (bool, optional): Whether to invert the image.
        
    Returns:
        str: HTML string representing the ASCII art.
    """
    generator = EnhancedAsciiArtGenerator(width=width, height=height, mode=mode)
    generator.set_enhancement(contrast=contrast, brightness=brightness, 
                            dithering=dithering, edge_enhance=edge_enhance, 
                            invert=invert)
    return generator.generate_html(image_path, font_size=font_size, 
                                   font_family=font_family, 
                                   preserve_color=preserve_color, bg=bg)