"""End-to-end coverage for the runnable examples."""

import os
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class TestEnhancedDemo(unittest.TestCase):
    """enhanced_demo.py must produce its gallery, including index.html."""

    def test_demo_writes_index_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            image_path = os.path.join(tmp, "tiny.png")
            Image.new("RGB", (40, 30), color="gray").save(image_path)
            completed = subprocess.run(
                [
                    sys.executable,
                    os.path.join(REPO_ROOT, "examples", "enhanced_demo.py"),
                    image_path,
                ],
                capture_output=True,
                text=True,
                cwd=tmp,
                check=True,
            )
            self.assertEqual(completed.returncode, 0)
            gallery = os.path.join(tmp, "demo_outputs")
            index = os.path.join(gallery, "index.html")
            self.assertTrue(os.path.isfile(index))
            with open(index, encoding="utf-8") as file:
                html = file.read()
            self.assertIn("demo_dense.txt", html)
            self.assertTrue(os.path.isfile(os.path.join(gallery, "demo_dense.txt")))


if __name__ == "__main__":
    unittest.main()
