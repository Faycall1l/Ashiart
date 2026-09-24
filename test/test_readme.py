"""README code blocks must execute without errors."""

import contextlib
import os
import re
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
READMES = ("README.md", "README.fr.md")
SCRATCH_FILES = ("output.txt", "output.html")


def _python_blocks(path):
    with open(path, encoding="utf-8") as file:
        text = file.read()
    return re.findall(r"```python\n(.*?)```", text, re.DOTALL)


class TestReadmeSnippets(unittest.TestCase):
    """Every python block in the READMEs must run cleanly."""

    def test_snippets_execute(self):
        previous = os.getcwd()
        os.chdir(REPO_ROOT)
        try:
            for name in READMES:
                blocks = _python_blocks(os.path.join(REPO_ROOT, name))
                self.assertTrue(blocks, f"No python blocks found in {name}")
                for index, block in enumerate(blocks):
                    with self.subTest(readme=name, block=index):
                        exec(compile(block, f"{name}#{index}", "exec"), {})
        finally:
            for scratch in SCRATCH_FILES:
                with contextlib.suppress(FileNotFoundError):
                    os.remove(os.path.join(REPO_ROOT, scratch))
            os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
