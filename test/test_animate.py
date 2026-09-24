"""Tests for GIF/video/webcam animation support."""

import io as stdlib_io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image

from ashiart.animate import (
    fit_to_terminal,
    iter_gif_frames,
    play_animation,
    save_animation_html,
)


def _two_frame_gif(path):
    black = Image.new("RGB", (8, 8), color="black")
    white = Image.new("RGB", (8, 8), color="white")
    black.save(path, save_all=True, append_images=[white], duration=[100, 200], loop=0)


class TestGifFrames(unittest.TestCase):
    """GIF decoding."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.gif_path = os.path.join(self.temp_dir.name, "anim.gif")
        _two_frame_gif(self.gif_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_frames_and_durations(self):
        frames = iter_gif_frames(self.gif_path)
        self.assertEqual(len(frames), 2)
        self.assertEqual([duration for _, duration in frames], [100, 200])
        self.assertEqual(frames[0][0].size, (8, 8))


class TestPlayback(unittest.TestCase):
    """Frame playback."""

    def test_loops_once_and_clears(self):
        sleeps = []
        buffer = stdlib_io.StringIO()
        completed = play_animation(
            ["AA", "BB"], [100, 100], loops=1, output=buffer, sleeper=sleeps.append
        )
        self.assertEqual(completed, 1)
        out = buffer.getvalue()
        self.assertIn("\x1b[2J", out)
        self.assertIn("AA", out)
        self.assertIn("BB", out)
        self.assertTrue(sleeps)

    def test_max_fps_caps_rate(self):
        sleeps = []
        buffer = stdlib_io.StringIO()
        play_animation(
            ["AA"], 5, loops=1, max_fps=10, output=buffer, sleeper=sleeps.append
        )
        self.assertTrue(all(s >= 0.09 for s in sleeps))

    def test_fit_to_terminal(self):
        import shutil as shutil_module

        with patch.object(
            shutil_module, "get_terminal_size", return_value=os.terminal_size((60, 20))
        ):
            width, height = fit_to_terminal()
        self.assertEqual(width, 58)
        self.assertIsNone(height)


class TestAnimationHtml(unittest.TestCase):
    """Animated HTML export."""

    def test_frames_embedded_with_timer(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "anim.html")
            save_animation_html(["AA", "BB"], path, [100, 200])
            with open(path, encoding="utf-8") as file:
                html = file.read()
        self.assertIn("setTimeout", html)
        self.assertIn('"AA"', html)
        self.assertIn('"BB"', html)
        self.assertIn("[100, 200]", html)


class FakeCapture:
    """Minimal cv2.VideoCapture stub yielding two BGR frames."""

    def __init__(self, *args):
        self.calls = 0
        self.released = False

    def get(self, prop):
        return 10.0

    def read(self):
        self.calls += 1
        if self.calls > 2:
            return False, None
        return True, np.zeros((4, 4, 3), dtype=np.uint8)

    def release(self):
        self.released = True


class FakeCv2:
    CAP_PROP_FPS = 5
    COLOR_BGR2RGB = 4

    def __init__(self):
        self.captures = []

    def VideoCapture(self, *args):
        capture = FakeCapture(*args)
        self.captures.append(capture)
        return capture

    def cvtColor(self, frame, code):
        return frame[:, :, ::-1]


class TestVideo(unittest.TestCase):
    """Video and webcam input with stubbed OpenCV."""

    def test_video_frames(self):
        from ashiart.video import iter_video_frames

        fake = FakeCv2()
        with patch.dict(sys.modules, {"cv2": fake}):
            frames = list(iter_video_frames("movie.mp4"))
        self.assertEqual(len(frames), 2)
        image, duration = frames[0]
        self.assertEqual(image.size, (4, 4))
        self.assertEqual(duration, 100)
        self.assertTrue(fake.captures[0].released)

    def test_webcam_mirror_and_release(self):
        from ashiart.video import iter_webcam_frames

        fake = FakeCv2()
        with patch.dict(sys.modules, {"cv2": fake}):
            taken = []
            for frame in iter_webcam_frames(0):
                taken.append(frame)
                if len(taken) == 2:
                    break
        self.assertEqual(len(taken), 2)
        self.assertTrue(fake.captures[0].released)

    def test_missing_cv2_explains_extra(self):
        from ashiart.video import _require_cv2

        with (
            patch.dict(sys.modules, {"cv2": None}),
            self.assertRaises(ValueError) as context,
        ):
            _require_cv2()
        self.assertIn("ashiart[video]", str(context.exception))


if __name__ == "__main__":
    unittest.main()
