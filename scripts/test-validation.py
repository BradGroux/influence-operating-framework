#!/usr/bin/env python3
"""Focused repository-maintenance regressions; not framework conformance tests."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("validator", Path(__file__).with_name("validate-repository.py"))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class ValidationTests(unittest.TestCase):
    def test_calendar_dates(self):
        for valid, expected in [("2026.09.05", "2026-09-05"), ("2026.09.05.1", "2026-09-05"), ("2028.02.29.12", "2028-02-29")]:
            self.assertEqual(v.edition_date(valid), expected)
        for invalid in ["2026.02.29", "2026.02.31", "2026.13.01", "2026.9.05", "2026.09.05.0", "2026.09.05.01", "2026.09.05-rc.1", "1.0.2"]:
            with self.assertRaises(ValueError, msg=invalid):
                v.edition_date(invalid)

    def test_active_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for edition in ["2026.09.05", "2028.02.29.2"]:
                released = v.edition_date(edition)
                content = {
                    "VERSION": edition,
                    "README.md": f"Edition {edition} is the current documentation edition.\n",
                    "CHANGELOG.md": f"## {edition} — {released}\n",
                    "GOVERNANCE.md": f"### Edition {edition}\n",
                    "framework/charter.md": f"- **Status:** Accepted {edition}\n",
                    "CITATION.cff": f'cff-version: 1.2.0\nversion: "{edition}"\ndate-released: {released}\nlicense: MIT\nrepository-code: "https://github.com/BradGroux/influence-operating-framework"\n',
                    f"project/releases/v{edition}-release-{released}.md": "# Release\n",
                }
                for name, text in content.items():
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(text)
                with patch.object(v, "ROOT", root):
                    errors = []
                    v.validate_release_metadata(errors)
                    self.assertEqual(errors, [])
                    for bad in [content["CITATION.cff"].replace(released, "2026-01-01"), content["CITATION.cff"] + 'version: "wrong"\n', content["CITATION.cff"].replace(f'"{edition}"', f'"{edition}.3"')]:
                        (root / "CITATION.cff").write_text(bad)
                        errors = []
                        v.validate_release_metadata(errors)
                        self.assertTrue(errors)
                    (root / "CITATION.cff").write_text(content["CITATION.cff"])
                    (root / "README.md").write_text(f"An old entry mentions {edition}.\n")
                    errors = []
                    v.validate_release_metadata(errors)
                    self.assertTrue(errors)

    def test_candidate_only_history(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)
            git("init", "-b", "main")
            git("config", "user.name", "Fixture")
            git("config", "user.email", "fixture" + chr(64) + "example.invalid")
            git("config", "commit.gpgsign", "false")
            (root / "README.md").write_text("# Safe\n")
            git("add", ".")
            git("commit", "-m", "Safe baseline")
            git("switch", "-c", "candidate")
            (root / "README.md").write_text("# Candidate\nReviewer " + "A\n")
            git("commit", "-am", "Candidate fixture")
            with patch.object(v, "ROOT", root):
                errors = []
                self.assertEqual(v.validate_public_history(errors), 2)
                self.assertTrue(any("legacy attribution" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
