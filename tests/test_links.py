from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_links(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py"), "--root", str(root), "--only", "links", "--no-report"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


class LinkAcceptanceTests(unittest.TestCase):
    def test_repository_local_links_and_heading_anchors_resolve(self) -> None:
        result = run_links(ROOT)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS links", result.stdout)

    def test_broken_relative_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            (fixture / "README.md").write_text("[Missing](docs/missing.md)\n", encoding="utf-8")
            result = run_links(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("docs/missing.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
