"""Tests for the ASCII art generator module."""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from PIL import Image, ImageDraw

from ashiart import image_to_ascii
from ashiart.generator import AsciiArtGenerator


class TestAsciiArtGenerator(unittest.TestCase):
    """Test the AsciiArtGenerator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.generator = AsciiArtGenerator(width=10, height=5)

        # Create a test image
        self.test_image = Image.new("RGB", (100, 50), color="white")
        draw = ImageDraw.Draw(self.test_image)
        draw.rectangle([(0, 0), (50, 25)], fill="black")

        # Create temp file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_image_path = os.path.join(self.temp_dir.name, "test_image.png")
        self.test_image.save(self.test_image_path)

        # Output path for saving tests
        self.output_path = os.path.join(self.temp_dir.name, "output.txt")

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_init(self):
        """Test initialization with default and custom values."""
        # Default ASCII characters
        self.assertEqual(self.generator.chars, AsciiArtGenerator.ASCII_CHARS)

        # Custom ASCII characters
        custom_chars = ["X", "O", "."]
        custom_generator = AsciiArtGenerator(chars=custom_chars)
        self.assertEqual(custom_generator.chars, custom_chars)

        # Custom dimensions
        self.assertEqual(self.generator.width, 10)
        self.assertEqual(self.generator.height, 5)

    def test_resize_image(self):
        """Test image resizing."""
        resized = self.generator._resize_image(self.test_image)
        self.assertEqual(resized.width, 10)
        self.assertEqual(resized.height, 5)

    def test_convert_to_grayscale(self):
        """Test grayscale conversion."""
        grayscale = self.generator._convert_to_grayscale(self.test_image)
        self.assertEqual(grayscale.mode, "L")

    def test_map_pixels_to_ascii(self):
        """Test pixel to ASCII character mapping."""
        # Create a small test image with a gradient
        test_img = Image.new("L", (2, 2))
        test_img.putdata([0, 128, 255, 32])  # Black, gray, white, dark gray

        # Use only 3 ASCII characters for simpler testing
        self.generator.chars = ["@", "O", "."]

        ascii_image = self.generator._map_pixels_to_ascii(test_img)

        # Buckets are symmetric via round(): 0 -> first, 128 -> middle,
        # 255 -> last, 32 (12% gray) -> first char
        self.assertEqual(ascii_image[0][0], "@")  # Darkest (0) -> first char
        self.assertEqual(ascii_image[0][1], "O")  # Mid gray (128) -> middle char
        self.assertEqual(ascii_image[1][0], ".")  # White (255) -> last char
        self.assertEqual(ascii_image[1][1], "@")  # Dark gray (32) -> first char

    def test_default_ramp_ends_with_space(self):
        """White must map to blank (paper), not a visible dot."""
        self.assertEqual(AsciiArtGenerator.ASCII_CHARS[-1], " ")

    def test_aspect_correction(self):
        """Monospace glyphs are ~2:1, so rows sample at half rate."""
        gen = AsciiArtGenerator(width=100)
        resized = gen._resize_image(Image.new("RGB", (200, 100)))
        self.assertEqual((resized.width, resized.height), (100, 25))

    def test_autocontrast_on_by_default(self):
        """Levels are stretched to the full ramp unless disabled."""
        self.assertTrue(AsciiArtGenerator(width=10).autocontrast)

    def test_resample_box_matches_dimensions(self):
        """Area-average resampling must keep output geometry."""
        art = AsciiArtGenerator(
            width=10, height=5, resample="box"
        ).generate_from_pil_image(self.test_image)
        lines = art.strip("\n").split("\n")
        self.assertEqual(len(lines), 5)
        self.assertTrue(all(len(line) == 10 for line in lines))

    def test_resample_rejects_unknown(self):
        """Unknown filter names must fail fast."""
        with self.assertRaises(ValueError):
            AsciiArtGenerator(resample="nearest")

    def test_gamma_darkens_midtones(self):
        """Gamma 2.0 must map 128 to ~64 before ramp lookup."""
        gray = Image.new("L", (4, 4), color=128)
        converted = AsciiArtGenerator(
            autocontrast=False, gamma=2.0
        )._convert_to_grayscale(gray.convert("RGB"))
        self.assertEqual(converted.getpixel((0, 0)), 64)

    def test_gamma_rejects_non_positive(self):
        """Gamma must stay positive."""
        with self.assertRaises(ValueError):
            AsciiArtGenerator(gamma=0)

    def test_generate_from_image(self):
        """Test generating ASCII art from an image file."""
        ascii_art = self.generator.generate_from_image(self.test_image_path)

        # Check that we get a string with the expected dimensions
        lines = ascii_art.strip("\n").split("\n")
        self.assertEqual(len(lines), 5)  # 5 rows
        self.assertEqual(len(lines[0]), 10)  # 10 columns

    def test_generate_from_pil_image(self):
        """Test generating ASCII art from a PIL Image object."""
        ascii_art = self.generator.generate_from_pil_image(self.test_image)

        # Check that we get a string with the expected dimensions
        lines = ascii_art.strip("\n").split("\n")
        self.assertEqual(len(lines), 5)  # 5 rows
        self.assertEqual(len(lines[0]), 10)  # 10 columns

    def test_save_to_file(self):
        """Test saving ASCII art to a file."""
        ascii_art = "TEST\nASCII\nART"
        self.generator.save_to_file(ascii_art, self.output_path)

        # Check that the file was created with the correct content
        with open(self.output_path, "r") as f:
            content = f.read()

        self.assertEqual(content, ascii_art)

    def test_file_not_found(self):
        """Test handling of non-existent files."""
        with self.assertRaises(FileNotFoundError):
            self.generator.generate_from_image("nonexistent_file.jpg")

    def test_generate_from_url(self):
        """Images served over HTTP must convert like local files."""
        import functools
        import http.server
        import threading

        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=self.temp_dir.name
        )
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            port = server.server_address[1]
            art = self.generator.generate_from_image(
                f"http://127.0.0.1:{port}/test_image.png"
            )
        finally:
            server.shutdown()
            thread.join()
        lines = art.strip("\n").split("\n")
        self.assertEqual(len(lines), 5)
        self.assertTrue(all(len(line) == 10 for line in lines))

    def test_bad_url_raises_value_error(self):
        """Unreachable hosts and non-image bytes raise ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_from_image("http://127.0.0.1:1/nope.png")

    def _http_server(self, counter):
        import functools
        import http.server
        import threading

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                counter["n"] += 1
                return super().do_GET()

            def log_message(self, *args):
                pass

        factory = functools.partial(Handler, directory=self.temp_dir.name)
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), factory)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread

    def test_url_cached_across_fetches(self):
        """Second fetch must not hit the network; cache survives shutdown."""
        import tempfile

        counter = {"n": 0}
        server, thread = self._http_server(counter)
        url = f"http://127.0.0.1:{server.server_address[1]}/test_image.png"
        with (
            tempfile.TemporaryDirectory() as cache_home,
            patch.dict(os.environ, {"XDG_CACHE_HOME": cache_home}),
        ):
            first = self.generator.generate_from_image(url)
            second = self.generator.generate_from_image(url)
            server.shutdown()
            thread.join()
            offline = self.generator.generate_from_image(url)
        self.assertEqual(counter["n"], 1)
        self.assertEqual(first, second)
        self.assertEqual(first, offline)

    def test_no_cache_refetches_every_time(self):
        """cache=False must hit the network on every fetch."""
        import tempfile

        counter = {"n": 0}
        server, thread = self._http_server(counter)
        try:
            url = f"http://127.0.0.1:{server.server_address[1]}/test_image.png"
            with (
                tempfile.TemporaryDirectory() as cache_home,
                patch.dict(os.environ, {"XDG_CACHE_HOME": cache_home}),
            ):
                self.generator.generate_from_image(url, cache=False)
                self.generator.generate_from_image(url, cache=False)
        finally:
            server.shutdown()
            thread.join()
        self.assertEqual(counter["n"], 2)

    def test_transient_error_retries_once(self):
        """One URLError must be retried before succeeding."""
        import urllib.error
        from ashiart import io as io_module

        with open(self.test_image_path, "rb") as file:
            payload = file.read()
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = payload
        calls = {"n": 0}

        def flaky(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise urllib.error.URLError("boom")
            return response

        with patch.object(io_module.urllib.request, "urlopen", side_effect=flaky):
            self.assertEqual(
                io_module.download_image("http://example.com/x.png", cache=False),
                payload,
            )
        self.assertEqual(calls["n"], 2)

    def test_client_error_does_not_retry(self):
        """HTTP 4xx must fail fast with the status in the message."""
        import urllib.error
        from ashiart import io as io_module

        error = urllib.error.HTTPError(
            "http://example.com/x.png", 404, "Not Found", {}, None
        )
        with (
            patch.object(
                io_module.urllib.request, "urlopen", side_effect=error
            ) as mock_open,
            self.assertRaises(ValueError) as context,
        ):
            io_module.download_image("http://example.com/x.png", cache=False)
        self.assertIn("404", str(context.exception))
        self.assertEqual(mock_open.call_count, 1)

    def _transparent_fixture(self):
        """Left half transparent, right half opaque black."""
        img = Image.new("RGBA", (8, 4), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(4, 0), (7, 3)], fill=(0, 0, 0, 255))
        return img

    def test_transparent_pixels_composite_onto_white(self):
        """Transparency must flatten to white, not decode as black."""
        gen = AsciiArtGenerator(width=8, height=4, autocontrast=False)
        for art in (
            gen.generate_from_pil_image(self._transparent_fixture()),
            gen.generate_from_image(self._save_fixture()),
        ):
            for line in art.split("\n"):
                self.assertEqual(line[:4], " " * 4)
                self.assertEqual(line[4:], "@" * 4)

    def _save_fixture(self):
        path = os.path.join(self.temp_dir.name, "alpha.png")
        self._transparent_fixture().save(path)
        return path

    def test_flatten_alpha_passes_opaque_through(self):
        """Images without alpha come back untouched."""
        from ashiart.io import flatten_alpha

        rgb = Image.new("RGB", (4, 4), color="red")
        self.assertIs(flatten_alpha(rgb), rgb)

    def test_open_image_accepts_raw_bytes(self):
        """Piped stdin bytes must decode like files."""
        import io as stdlib_io

        from ashiart.io import open_image

        buffer = stdlib_io.BytesIO()
        self.test_image.save(buffer, format="PNG")
        image = open_image(buffer.getvalue())
        self.assertEqual(image.size, (100, 50))

    def test_exif_orientation_applied(self):
        """EXIF orientation 6 must transpose stored landscape to portrait."""
        img = Image.new("RGB", (8, 4), color="white")
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (3, 3)], fill="black")
        exif = img.getexif()
        exif[0x0112] = 6
        path = os.path.join(self.temp_dir.name, "oriented.jpg")
        img.save(path, exif=exif, quality=95)

        from ashiart.io import open_image

        self.assertEqual(open_image(path).size, (4, 8))

        gen = AsciiArtGenerator(width=4, autocontrast=False)
        lines = gen.generate_from_image(path).split("\n")
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0][0], "@")
        self.assertEqual(lines[-1][0], " ")

    def test_image_to_ascii_function(self):
        """Test the convenience function."""
        ascii_art = image_to_ascii(self.test_image_path, width=10, height=5)

        # Check that we get a string with the expected dimensions
        lines = ascii_art.strip("\n").split("\n")
        self.assertEqual(len(lines), 5)  # 5 rows
        self.assertEqual(len(lines[0]), 10)  # 10 columns


if __name__ == "__main__":
    unittest.main()
