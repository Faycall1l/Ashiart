"""Tests for the ASCII art generator CLI."""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

from ashiart.cli import main


class TestCLI(unittest.TestCase):
    """Test the command-line interface."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a test image
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_image_path = os.path.join(self.temp_dir.name, "test_image.png")
        self.output_path = os.path.join(self.temp_dir.name, "output.txt")

        # Create a simple test image
        test_image = Image.new("RGB", (10, 10), color="white")
        test_image.save(self.test_image_path)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_stdin_dash_reads_piped_bytes(self):
        """image_path '-' must consume piped stdin bytes."""
        import io as stdlib_io
        import types

        with open(self.test_image_path, "rb") as file:
            payload = file.read()
        fake_stdin = types.SimpleNamespace(buffer=stdlib_io.BytesIO(payload))
        with patch.object(sys, "stdin", fake_stdin), patch(
            "builtins.print"
        ) as mock_print:
            result = main(["-", "-w", "5", "-H", "3"])
        self.assertEqual(result, 0)
        mock_print.assert_called_once()
        self.assertEqual(len(mock_print.call_args[0][0].split("\n")), 3)

    def test_no_color_strips_ansi(self):
        """NO_COLOR must disable --color even when requested."""
        import contextlib
        import io as stdlib_io

        buffer = stdlib_io.StringIO()
        with patch.dict(os.environ, {"NO_COLOR": "1"}), contextlib.redirect_stdout(
            buffer
        ):
            result = main([self.test_image_path, "--color", "-w", "5", "-H", "3"])
        self.assertEqual(result, 0)
        self.assertNotIn("\x1b[", buffer.getvalue())

    def test_module_entry_point(self):
        """python -m ashiart must expose the CLI."""
        import subprocess

        completed = subprocess.run(
            [sys.executable, "-m", "ashiart", "--help"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn("usage: ashiart", completed.stdout)

    def test_demo_needs_no_input(self):
        """--demo must render without any image argument."""
        with patch("builtins.print") as mock_print:
            result = main(["--demo", "-w", "20"])
        self.assertEqual(result, 0)
        mock_print.assert_called_once()

    def test_missing_input_is_usage_error(self):
        """No image and no --demo must exit with code 2."""
        with self.assertRaises(SystemExit) as context, patch("sys.stderr"):
            main([])
        self.assertEqual(context.exception.code, 2)

    def test_open_requires_html(self):
        """--open without --html must exit with code 2."""
        with self.assertRaises(SystemExit) as context, patch("sys.stderr"):
            main([self.test_image_path, "--open"])
        self.assertEqual(context.exception.code, 2)

    def test_open_launches_browser(self):
        """--open must open the written HTML file URL."""
        with patch("webbrowser.open") as mock_open, patch("builtins.print"):
            result = main(
                [
                    self.test_image_path,
                    "--html",
                    self.output_path + ".html",
                    "--open",
                    "-w",
                    "5",
                    "-H",
                    "3",
                ]
            )
        self.assertEqual(result, 0)
        mock_open.assert_called_once()
        self.assertTrue(mock_open.call_args[0][0].startswith("file://"))

    def test_no_cache_flag_runs(self):
        """--no-cache must be accepted and bypass download caching."""
        with patch("builtins.print"):
            result = main([self.test_image_path, "--no-cache", "-w", "5", "-H", "3"])
        self.assertEqual(result, 0)

    def test_tonal_flags_run(self):
        """--clahe, --dog, --gamma, --resample, --bg must all be accepted."""
        html_path = os.path.join(self.temp_dir.name, "tonal.html")
        with patch("builtins.print"):
            result = main(
                [
                    self.test_image_path,
                    "-w",
                    "8",
                    "-H",
                    "4",
                    "--clahe",
                    "--dog",
                    "0.8",
                    "2.0",
                    "2.0",
                    "--gamma",
                    "1.2",
                    "--resample",
                    "box",
                    "--html",
                    html_path,
                    "--bg",
                    "white",
                ]
            )
        self.assertEqual(result, 0)
        with open(html_path, encoding="utf-8") as file:
            self.assertIn("background-color: white", file.read())

    def test_width_defaults_to_terminal_size(self):
        """No -w on a tty must use the terminal width."""
        import contextlib
        import io as stdlib_io
        import shutil as shutil_module

        buffer = stdlib_io.StringIO()
        with contextlib.redirect_stdout(buffer), patch.object(
            buffer, "isatty", return_value=True
        ), patch.object(
            shutil_module, "get_terminal_size", return_value=os.terminal_size((40, 24))
        ):
            result = main([self.test_image_path])
        self.assertEqual(result, 0)
        self.assertTrue(
            all(len(line) == 40 for line in buffer.getvalue().split("\n") if line)
        )

    def _write_gif(self):
        black = Image.new("RGB", (8, 8), color="black")
        white = Image.new("RGB", (8, 8), color="white")
        path = os.path.join(self.temp_dir.name, "anim.gif")
        black.save(
            path, save_all=True, append_images=[white], duration=[50, 50], loop=0
        )
        return path

    def test_play_gif_loops_once(self):
        """--play --loop 1 must render every frame and stop."""
        import contextlib
        import io as stdlib_io

        buffer = stdlib_io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = main(
                [self._write_gif(), "--play", "--loop", "1", "-w", "8", "-H", "4"]
            )
        self.assertEqual(result, 0)
        self.assertIn("\x1b[2J", buffer.getvalue())

    def test_play_with_html_exports_animation(self):
        """--play --html must write a looping HTML file."""
        import contextlib
        import io as stdlib_io

        html_path = os.path.join(self.temp_dir.name, "anim.html")
        buffer = stdlib_io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = main(
                [
                    self._write_gif(),
                    "--play",
                    "--loop",
                    "1",
                    "-w",
                    "8",
                    "-H",
                    "4",
                    "--html",
                    html_path,
                ]
            )
        self.assertEqual(result, 0)
        with open(html_path, encoding="utf-8") as file:
            self.assertIn("setTimeout", file.read())

    def test_video_without_extra_fails_cleanly(self):
        """mp4 input without OpenCV must exit 1 with guidance."""
        movie = os.path.join(self.temp_dir.name, "movie.mp4")
        with open(movie, "wb") as file:
            file.write(b"not a video")
        with patch.dict(sys.modules, {"cv2": None}), patch("sys.stderr"), patch(
            "builtins.print"
        ) as mock_print:
            result = main([movie, "--play"])
        self.assertEqual(result, 1)
        self.assertIn("ashiart[video]", mock_print.call_args[0][0])

    def test_webcam_streams_until_device_ends(self):
        """--webcam must render stubbed frames then stop at end of stream."""
        import contextlib
        import io as stdlib_io

        import numpy as np

        class Capture:
            def __init__(self, *args):
                self.calls = 0

            def read(self):
                self.calls += 1
                if self.calls > 2:
                    return False, None
                return True, np.zeros((8, 8, 3), dtype=np.uint8)

            def release(self):
                pass

        class FakeCv2:
            COLOR_BGR2RGB = 4

            def VideoCapture(self, *args):
                return Capture()

            def cvtColor(self, frame, code):
                return frame[:, :, ::-1]

        buffer = stdlib_io.StringIO()
        with patch.dict(sys.modules, {"cv2": FakeCv2()}), contextlib.redirect_stdout(
            buffer
        ):
            result = main(["--webcam", "-w", "8", "-H", "4"])
        self.assertEqual(result, 0)
        self.assertIn("\x1b[2J", buffer.getvalue())

    @patch("sys.argv")
    @patch("builtins.print")
    def test_main_with_output_file(self, mock_print, mock_argv):
        """Test CLI with output to file."""
        # Mock the command-line arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "ashiart",
            self.test_image_path,
            "-o",
            self.output_path,
            "-w",
            "5",
            "-H",
            "3",
        ][i]
        mock_argv.__len__.return_value = 7

        # Run the CLI
        result = main()

        # Check that the function completed successfully
        self.assertEqual(result, 0)

        # Check that the output file was created
        self.assertTrue(os.path.exists(self.output_path))

        # Check that the success message was printed
        mock_print.assert_called_with(f"ASCII art saved to {self.output_path}")

    @patch("sys.argv")
    @patch("builtins.print")
    def test_main_with_console_output(self, mock_print, mock_argv):
        """Test CLI with output to console."""
        # Mock the command-line arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "ashiart",
            self.test_image_path,
            "-w",
            "5",
            "-H",
            "3",
        ][i]
        mock_argv.__len__.return_value = 5

        # Run the CLI
        result = main()

        # Check that the function completed successfully
        self.assertEqual(result, 0)

        # Check that something was printed (the ASCII art)
        mock_print.assert_called()

    @patch("sys.argv")
    def test_main_with_nonexistent_file(self, mock_argv):
        """Test CLI with a non-existent file."""
        # Mock the command-line arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "ashiart",
            "nonexistent_file.jpg",
        ][i]
        mock_argv.__len__.return_value = 2

        # Run the CLI and check for error exit code
        with patch("builtins.print") as mock_print:
            result = main()
            self.assertEqual(result, 1)

            # Check that an error message was printed
            mock_print.assert_called()


if __name__ == "__main__":
    unittest.main()
