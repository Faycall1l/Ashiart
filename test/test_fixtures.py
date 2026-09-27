"""Real-photo fixture tests.

Fixtures live in test/fixtures/ (see scripts/fetch_fixtures.py for
provenance): one simple subject each, smooth backgrounds. Assertions
stay structural — exact glyphs vary with the Pillow build — while
geometry and determinism must hold exactly.
"""

import os
import unittest

from ashiart import image_to_ascii

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
PORTRAIT = os.path.join(FIXTURE_DIR, "portrait.jpg")
WATERLILY = os.path.join(FIXTURE_DIR, "waterlily.jpg")


class TestPhotoFixtures(unittest.TestCase):
    """Conversions of real photos must be stable and well-spread."""

    def test_fixtures_present(self):
        """Both pins must exist for the offline suite."""
        self.assertTrue(os.path.isfile(PORTRAIT))
        self.assertTrue(os.path.isfile(WATERLILY))

    def test_geometry(self):
        """Square fixtures at width 60 give 60x30 grids."""
        for path in (PORTRAIT, WATERLILY):
            with self.subTest(fixture=os.path.basename(path)):
                lines = image_to_ascii(path, width=60).split("\n")
                self.assertEqual(len(lines), 30)
                self.assertTrue(all(len(line) == 60 for line in lines))

    def test_deterministic(self):
        """Same input must byte-match across runs."""
        first = image_to_ascii(PORTRAIT, width=60, mode="dense")
        second = image_to_ascii(PORTRAIT, width=60, mode="dense")
        self.assertEqual(first, second)

    def test_tonal_spread(self):
        """Real photos must exercise the ramp, not one bucket."""
        for path in (PORTRAIT, WATERLILY):
            with self.subTest(fixture=os.path.basename(path)):
                art = image_to_ascii(path, width=60, mode="dense")
                glyphs = set(art.replace("\n", ""))
                self.assertGreaterEqual(len(glyphs), 20)

    def test_edges_trace_contours(self):
        """Edge overlay must fire on facial and petal contours."""
        for path in (PORTRAIT, WATERLILY):
            with self.subTest(fixture=os.path.basename(path)):
                art = image_to_ascii(path, width=60, edges=True, edge_threshold=0.5)
                strokes = sum(
                    line.count("/") + line.count("\\") + line.count("|")
                    for line in art.split("\n")
                )
                self.assertGreater(strokes, 20)

    def test_dark_subject_maps_dark(self):
        """The lily's dark water must render denser than its bloom."""
        art = image_to_ascii(WATERLILY, width=60, autocontrast=False)
        lines = art.split("\n")
        top = "".join(lines[:6])
        middle = "".join(lines[10:16])
        density = {
            "@": 9,
            "#": 8,
            "S": 7,
            "%": 6,
            "?": 5,
            "*": 4,
            "+": 3,
            ";": 2,
            ":": 1,
            ",": 0,
            ".": 0,
            " ": 0,
        }
        dark = sum(density.get(char, 4) for char in top) / max(len(top), 1)
        light = sum(density.get(char, 4) for char in middle) / max(len(middle), 1)
        self.assertGreater(dark, light)


if __name__ == "__main__":
    unittest.main()
