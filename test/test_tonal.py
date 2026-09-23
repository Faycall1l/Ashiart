"""Tests for the tonal operators (CLAHE, DoG)."""

import unittest

import numpy as np
from PIL import Image

from ashiart.tonal import apply_clahe, apply_dog


def _gray(pixels, size):
    img = Image.new("L", size)
    img.putdata(pixels)
    return img


class TestClahe(unittest.TestCase):
    """Contrast-limited adaptive equalization."""

    def test_uniform_image_unchanged(self):
        """Clipping must not amplify noise in flat regions."""
        flat = Image.new("L", (32, 32), color=128)
        self.assertTrue(np.array_equal(np.asarray(apply_clahe(flat)), np.asarray(flat)))

    def test_narrow_range_widens(self):
        """Local equalization must spread compressed tones."""
        narrow = _gray([(x % 41) + 100 for x in range(32 * 32)], (32, 32))
        out = np.asarray(apply_clahe(narrow))
        before = np.asarray(narrow)
        self.assertGreater(int(out.max()) - int(out.min()),
                           int(before.max()) - int(before.min()))

    def test_output_geometry_and_range(self):
        """Shape preserved, values stay in byte range."""
        img = _gray([(x * 7) % 256 for x in range(40 * 30)], (40, 30))
        out = apply_clahe(img)
        self.assertEqual(out.size, (40, 30))
        self.assertEqual(out.mode, "L")


class TestDog(unittest.TestCase):
    """Difference-of-Gaussians detail emphasis."""

    def test_uniform_image_unchanged(self):
        """No detail band means no change."""
        flat = Image.new("L", (32, 32), color=128)
        self.assertTrue(np.array_equal(np.asarray(apply_dog(flat)), np.asarray(flat)))

    def test_step_edge_gains_overshoot(self):
        """Mid-gray steps must overshoot on both sides of the edge."""
        pixels = [100 if x < 16 else 180 for _ in range(32) for x in range(32)]
        step = _gray(pixels, (32, 32))
        out = np.asarray(apply_dog(step, small=0.8, large=2.0, amplify=2.0))
        self.assertFalse(np.array_equal(out, np.asarray(step)))
        self.assertLess(int(out.min()), 100)
        self.assertGreater(int(out.max()), 180)

    def test_rejects_inverted_sigmas(self):
        """Large sigma must exceed small sigma."""
        flat = Image.new("L", (8, 8), color=128)
        with self.assertRaises(ValueError):
            apply_dog(flat, small=2.0, large=0.8)


if __name__ == "__main__":
    unittest.main()
