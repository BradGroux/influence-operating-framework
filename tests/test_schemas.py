from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_schemas(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py"), "--root", str(root), "--only", "schemas", "--no-report"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def copy_schema_fixture(destination: Path) -> None:
    shutil.copytree(ROOT / "schemas", destination / "schemas")
    shutil.copytree(ROOT / "examples", destination / "examples")


class SchemaAcceptanceTests(unittest.TestCase):
    def test_public_examples_validate_as_one_linked_dataset(self) -> None:
        result = run_schemas(ROOT)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS schemas", result.stdout)
        self.assertIn("PASS graph-references", result.stdout)

    def test_do_not_contact_cannot_be_reopened_without_a_traced_human_decision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "relationship-lina-jules.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["disposition_history"] = [
                {
                    "decision_id": "decision-test-do-not-contact",
                    "state": "do_not_contact",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-01T12:00:00Z",
                    "reason": "A fictional human set the restriction."
                },
                {
                    "decision_id": "decision-test-reopen",
                    "state": "consider",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-02T12:00:00Z",
                    "reason": "A fictional human reconsidered the restriction."
                }
            ]
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must supersede decision-test-do-not-contact", result.stdout)

    def test_reviewed_outreach_requires_a_named_human_time_and_reason(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["review_history"][0]["reason"] = ""
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("should be non-empty", result.stdout)


if __name__ == "__main__":
    unittest.main()
