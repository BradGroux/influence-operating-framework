from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_visuals(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py"), "--root", str(root), "--only", "visuals", "--no-report"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


class VisualAcceptanceTests(unittest.TestCase):
    def test_all_required_visuals_are_complete_and_synchronized(self) -> None:
        result = run_visuals(ROOT)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS visuals", result.stdout)
        self.assertIn("12", result.stdout)

    def test_source_change_requires_a_rerender(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            shutil.copytree(ROOT / "visuals", fixture / "visuals")
            source = fixture / "visuals" / "source" / "framework-overview.mmd"
            source.write_text(source.read_text(encoding="utf-8") + "\n%% changed\n", encoding="utf-8")
            result = run_visuals(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("hash mismatch", result.stdout)

    def test_lifecycle_visual_preserves_all_eleven_stages_and_repeat_decision(self) -> None:
        source = (ROOT / "visuals" / "source" / "influence-lifecycle.mmd").read_text(encoding="utf-8")
        description = (ROOT / "visuals" / "descriptions" / "influence-lifecycle.md").read_text(encoding="utf-8")
        for stage in ("Discover", "Research", "Verify", "Map", "Prioritize", "Contribute", "Engage", "Follow up", "Reflect", "Improve", "Repeat"):
            self.assertIn(stage, source)
        self.assertIn("Repeat", description)
        self.assertIn("human", description.lower())


if __name__ == "__main__":
    unittest.main()
