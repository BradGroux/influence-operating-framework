from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_gate(root: Path, gate: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate.py"), "--root", str(root), "--only", gate, "--no-report"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def copy_safety_fixture(destination: Path) -> None:
    for directory in ("automations", "examples", "profiles", "schemas", "workflows"):
        shutil.copytree(ROOT / directory, destination / directory)


class StructureAcceptanceTests(unittest.TestCase):
    def test_required_structure_and_substantive_docs_exist(self) -> None:
        result = run_gate(ROOT, "structure")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS structure", result.stdout)
        self.assertIn("PASS documentation", result.stdout)

    def test_public_artifacts_preserve_privacy_and_human_outreach_boundary(self) -> None:
        result = run_gate(ROOT, "safety")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS public-data-safety", result.stdout)
        self.assertIn("PASS outreach-safety", result.stdout)

    def test_generated_repository_index_is_current(self) -> None:
        result = run_gate(ROOT, "index")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS index", result.stdout)

    def test_partial_validation_does_not_overwrite_full_report(self) -> None:
        report = ROOT / "reports" / "validation-report.md"
        before = report.read_bytes()
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate.py"), "--root", str(ROOT), "--only", "index"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, report.read_bytes())

    def test_possible_private_email_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            example_dir = fixture / "examples" / "fictional"
            example_dir.mkdir(parents=True)
            (example_dir / "unsafe.md").write_text("Contact: private.person@unsafe.test\n", encoding="utf-8")
            result = run_gate(fixture, "safety")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("possible private email", result.stdout)

    def test_invented_familiarity_requires_evidence_backed_relationship_claims(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_safety_fixture(fixture)
            path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["draft_content"] = "It was great meeting you. Would you review this?"
            record["relationship_claims"] = []
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_gate(fixture, "safety")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("invented familiarity", result.stdout)

    def test_sender_capability_is_rejected_anywhere_in_public_schemas(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_safety_fixture(fixture)
            path = fixture / "schemas" / "profile.schema.json"
            schema = json.loads(path.read_text(encoding="utf-8"))
            schema["send_message"] = {"type": "boolean"}
            path.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
            result = run_gate(fixture, "safety")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("prohibited sender field send_message", result.stdout)

    def test_transactional_person_vocabulary_is_rejected_in_public_examples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_safety_fixture(fixture)
            path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["human_notes"] = "Treat this fictional person as a prospect."
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_gate(fixture, "safety")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("transactional vocabulary", result.stdout)


if __name__ == "__main__":
    unittest.main()
