from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_schemas(root: Path, baseline_root: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(ROOT / "scripts" / "validate.py"), "--root", str(root), "--only", "schemas", "--no-report"]
    if baseline_root is not None:
        command.extend(["--baseline-root", str(baseline_root)])
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def copy_schema_fixture(destination: Path) -> None:
    shutil.copytree(ROOT / "schemas", destination / "schemas")
    shutil.copytree(ROOT / "examples", destination / "examples")


def approve_outreach(record: dict, *, decided_at: str = "2026-08-01T12:00:00Z", expires_at: str = "2026-08-08T12:00:00Z") -> None:
    record["disposition"] = "approve"
    record["review_history"] = [
        {
            "decision_id": "decision-outreach-accessibility-approve",
            "state": "approve",
            "decided_by_person_id": "person-lina-moreno",
            "decided_at": decided_at,
            "reason": "The fictional human approved this exact bounded draft.",
            "approval_scope": {
                "outreach_draft_id": record["id"],
                "recipient_person_id": record["recipient_person_id"],
                "content_sha256": hashlib.sha256(record["draft_content"].encode("utf-8")).hexdigest(),
                "channel": record["channel"],
                "expires_at": expires_at,
            },
        }
    ]


def make_outreach_eligible(fixture: Path) -> None:
    person_path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
    person = json.loads(person_path.read_text(encoding="utf-8"))
    person["communication_boundary"]["consent_status"] = "opted_in"
    person["communication_boundary"]["consent_history"][-1]["state"] = "opted_in"
    person["communication_boundary"]["consent_history"][-1]["reason"] = (
        "The fictional recipient explicitly opted in to this bounded review request."
    )
    person["communication_boundary"]["preferred_channels"] = ["community_platform_direct_message"]
    person["communication_boundary"]["restriction_history"][-1]["state"] = "none"
    person_path.write_text(json.dumps(person, indent=2) + "\n", encoding="utf-8")

    relationship_path = fixture / "examples" / "fictional" / "relationship-lina-jules.json"
    relationship = json.loads(relationship_path.read_text(encoding="utf-8"))
    relationship["disposition_history"][-1]["state"] = "consider"
    relationship_path.write_text(json.dumps(relationship, indent=2) + "\n", encoding="utf-8")


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

    def test_recipient_do_not_contact_overrides_an_approved_outreach_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            person_path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
            person = json.loads(person_path.read_text(encoding="utf-8"))
            person["communication_boundary"]["restriction_history"] = [
                {
                    "decision_id": "decision-jules-do-not-contact",
                    "state": "do_not_contact",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-02T12:00:00Z",
                    "reason": "The fictional recipient requested no contact."
                }
            ]
            person_path.write_text(json.dumps(person, indent=2) + "\n", encoding="utf-8")

            outreach_path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            outreach = json.loads(outreach_path.read_text(encoding="utf-8"))
            approve_outreach(outreach)
            outreach_path.write_text(json.dumps(outreach, indent=2) + "\n", encoding="utf-8")

            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("recipient has an active do-not-contact restriction", result.stdout)

    def test_linked_relationship_do_not_contact_overrides_approved_outreach(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            relationship_path = fixture / "examples" / "fictional" / "relationship-lina-jules.json"
            relationship = json.loads(relationship_path.read_text(encoding="utf-8"))
            relationship["disposition_history"][-1]["state"] = "do_not_contact"
            relationship_path.write_text(json.dumps(relationship, indent=2) + "\n", encoding="utf-8")
            outreach_path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            outreach = json.loads(outreach_path.read_text(encoding="utf-8"))
            approve_outreach(outreach)
            outreach_path.write_text(json.dumps(outreach, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("linked relationship has an active do-not-contact restriction", result.stdout)

    def test_relationship_do_not_contact_cannot_be_bypassed_by_dropping_contribution_edge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            make_outreach_eligible(fixture)
            relationship_path = fixture / "examples" / "fictional" / "relationship-lina-jules.json"
            relationship = json.loads(relationship_path.read_text(encoding="utf-8"))
            relationship["contribution_ids"] = []
            relationship["disposition_history"][-1]["state"] = "do_not_contact"
            relationship_path.write_text(json.dumps(relationship, indent=2) + "\n", encoding="utf-8")
            outreach_path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            outreach = json.loads(outreach_path.read_text(encoding="utf-8"))
            approve_outreach(outreach)
            outreach_path.write_text(json.dumps(outreach, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("linked relationship has an active do-not-contact restriction", result.stdout)

    def test_linked_opportunity_do_not_contact_overrides_approved_outreach(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            opportunity_path = fixture / "examples" / "fictional" / "opportunity-accessible-starter-guide.json"
            opportunity = json.loads(opportunity_path.read_text(encoding="utf-8"))
            opportunity["decision_history"][-1]["state"] = "do_not_contact"
            opportunity_path.write_text(json.dumps(opportunity, indent=2) + "\n", encoding="utf-8")
            outreach_path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            outreach = json.loads(outreach_path.read_text(encoding="utf-8"))
            approve_outreach(outreach)
            outreach_path.write_text(json.dumps(outreach, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("linked opportunity has an active do-not-contact restriction", result.stdout)

    def test_wait_and_opt_out_states_override_exact_outreach_approval(self) -> None:
        cases = ("person_wait", "relationship_wait", "opportunity_wait", "recipient_opted_out")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                copy_schema_fixture(fixture)
                make_outreach_eligible(fixture)
                if case in {"person_wait", "recipient_opted_out"}:
                    path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
                    record = json.loads(path.read_text(encoding="utf-8"))
                    if case == "person_wait":
                        record["communication_boundary"]["restriction_history"][-1]["state"] = "wait"
                    else:
                        record["communication_boundary"]["consent_status"] = "opted_out"
                        record["communication_boundary"]["consent_history"][-1]["state"] = "opted_out"
                elif case == "relationship_wait":
                    path = fixture / "examples" / "fictional" / "relationship-lina-jules.json"
                    record = json.loads(path.read_text(encoding="utf-8"))
                    record["disposition_history"][-1]["state"] = "wait"
                else:
                    path = fixture / "examples" / "fictional" / "opportunity-accessible-starter-guide.json"
                    record = json.loads(path.read_text(encoding="utf-8"))
                    record["decision_history"][-1]["state"] = "wait"
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                outreach_path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
                outreach = json.loads(outreach_path.read_text(encoding="utf-8"))
                approve_outreach(outreach)
                outreach_path.write_text(json.dumps(outreach, indent=2) + "\n", encoding="utf-8")
                result = run_schemas(fixture)
            self.assertNotEqual(0, result.returncode)
            self.assertRegex(result.stdout, r"active wait|consent status")

    def test_eligible_exact_outreach_approval_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            make_outreach_eligible(fixture)
            path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            approve_outreach(record)
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_unknown_consent_can_receive_contextual_human_approval_when_not_opted_out(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            make_outreach_eligible(fixture)
            person_path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
            person = json.loads(person_path.read_text(encoding="utf-8"))
            person["communication_boundary"]["consent_status"] = "unknown"
            person["communication_boundary"]["consent_history"][-1]["state"] = "unknown"
            person["communication_boundary"]["consent_history"][-1]["reason"] = (
                "No general opt-in exists; the authorized human is assessing one contextual request."
            )
            person_path.write_text(json.dumps(person, indent=2) + "\n", encoding="utf-8")
            outreach_path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            outreach = json.loads(outreach_path.read_text(encoding="utf-8"))
            approve_outreach(outreach)
            outreach_path.write_text(json.dumps(outreach, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_outreach_approval_uses_a_declared_preferred_channel(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            make_outreach_eligible(fixture)
            person_path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
            person = json.loads(person_path.read_text(encoding="utf-8"))
            person["communication_boundary"]["preferred_channels"] = ["email"]
            person_path.write_text(json.dumps(person, indent=2) + "\n", encoding="utf-8")
            outreach_path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            outreach = json.loads(outreach_path.read_text(encoding="utf-8"))
            approve_outreach(outreach)
            outreach_path.write_text(json.dumps(outreach, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("channel is not declared in recipient preferences", result.stdout)

    def test_relationship_participants_and_owners_allow_canonical_organizations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            relationship_path = fixture / "examples" / "fictional" / "relationship-lina-jules.json"
            relationship = json.loads(relationship_path.read_text(encoding="utf-8"))
            relationship["participant_ids"] = ["person-jules-okafor", "organization-riverbend-learning"]
            relationship_path.write_text(json.dumps(relationship, indent=2) + "\n", encoding="utf-8")
            contribution_path = fixture / "examples" / "fictional" / "contribution-accessible-starter-guide.json"
            contribution = json.loads(contribution_path.read_text(encoding="utf-8"))
            contribution["owner_id"] = "organization-riverbend-learning"
            contribution_path.write_text(json.dumps(contribution, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_semantically_typed_references_reject_existing_wrong_record_types(self) -> None:
        cases = {
            "recipient_person_id": (
                "outreach-draft-accessibility-review.json",
                lambda record: record.update({"recipient_person_id": "organization-riverbend-learning"}),
            ),
            "decided_by_person_id": (
                "relationship-lina-jules.json",
                lambda record: record["disposition_history"][-1].update({"decided_by_person_id": "organization-riverbend-learning"}),
            ),
            "owner_id": (
                "contribution-accessible-starter-guide.json",
                lambda record: record.update({"owner_id": "opportunity-accessible-starter-guide"}),
            ),
            "contribution_id": (
                "outreach-draft-accessibility-review.json",
                lambda record: record.update({"contribution_id": "opportunity-accessible-starter-guide"}),
            ),
            "opportunity_ids": (
                "contribution-accessible-starter-guide.json",
                lambda record: record.update({"opportunity_ids": ["person-jules-okafor"]}),
            ),
            "organizer_ids": (
                "event-riverbend-accessibility-lab.json",
                lambda record: record.update({"organizer_ids": ["contribution-accessible-starter-guide"]}),
            ),
            "beneficiary_ids": (
                "opportunity-accessible-starter-guide.json",
                lambda record: record.update({"beneficiary_ids": ["evidence-riverbend-program"]}),
            ),
        }
        for field, (filename, mutate) in cases.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                copy_schema_fixture(fixture)
                path = fixture / "examples" / "fictional" / filename
                record = json.loads(path.read_text(encoding="utf-8"))
                mutate(record)
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                result = run_schemas(fixture)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(f"{field} references", result.stdout)
                self.assertRegex(result.stdout, r"references .* record .*; expected")

    def test_outreach_approval_requires_profile_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            make_outreach_eligible(fixture)
            path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            approve_outreach(record)
            record["review_history"][-1]["decided_by_person_id"] = record["recipient_person_id"]
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("reviewer is not authorized by governing profile", result.stdout)

    def test_approval_is_bound_to_exact_content_recipient_channel_and_expiry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            reviewed_content = record["draft_content"]
            record["channel"] = "community_platform_direct_message"
            record["disposition"] = "approve"
            record["review_history"] = [
                {
                    "decision_id": "decision-outreach-accessibility-approve",
                    "state": "approve",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-01T12:00:00Z",
                    "reason": "The fictional human approved this exact bounded draft.",
                    "approval_scope": {
                        "outreach_draft_id": record["id"],
                        "recipient_person_id": record["recipient_person_id"],
                        "content_sha256": hashlib.sha256(reviewed_content.encode("utf-8")).hexdigest(),
                        "channel": record["channel"],
                        "expires_at": "2026-08-08T12:00:00Z"
                    }
                }
            ]
            record["draft_content"] = "This changed after the human review."
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("approved content hash does not match the current draft", result.stdout)

    def test_approval_scope_rejects_recipient_channel_and_expiry_mismatches(self) -> None:
        cases = {
            "recipient": ("approval scope recipient_person_id does not match", lambda record: record["review_history"][0]["approval_scope"].update({"recipient_person_id": "person-lina-moreno"})),
            "channel": ("approval scope channel does not match", lambda record: record.update({"channel": "different_channel"})),
            "expiry": ("approved outreach is expired", lambda record: record["review_history"][0]["approval_scope"].update({"expires_at": "2026-07-31T12:00:00Z"})),
        }
        for name, (message, mutate) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                copy_schema_fixture(fixture)
                path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
                record = json.loads(path.read_text(encoding="utf-8"))
                record["disposition"] = "approve"
                record["review_history"] = [
                    {
                        "decision_id": "decision-outreach-accessibility-approve",
                        "state": "approve",
                        "decided_by_person_id": "person-lina-moreno",
                        "decided_at": "2026-08-01T12:00:00Z",
                        "reason": "The fictional human approved this exact bounded draft.",
                        "approval_scope": {
                            "outreach_draft_id": record["id"],
                            "recipient_person_id": record["recipient_person_id"],
                            "content_sha256": hashlib.sha256(record["draft_content"].encode("utf-8")).hexdigest(),
                            "channel": record["channel"],
                            "expires_at": "2026-08-08T12:00:00Z"
                        }
                    }
                ]
                mutate(record)
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                result = run_schemas(fixture)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(message, result.stdout)

    def test_approval_expiry_cannot_precede_approval_decision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "outreach-draft-accessibility-review.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            approve_outreach(
                record,
                decided_at="2026-08-05T12:00:00Z",
                expires_at="2026-08-04T12:00:00Z",
            )
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("approval expires before its decision time", result.stdout)

    def test_decision_chronology_uses_instants_not_timestamp_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "relationship-lina-jules.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["disposition_history"] = [
                {
                    "decision_id": "decision-test-first",
                    "state": "wait",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-01T12:00:00-05:00",
                    "reason": "First instant is 17:00 UTC.",
                },
                {
                    "decision_id": "decision-test-second",
                    "state": "consider",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-01T16:00:00Z",
                    "reason": "Second instant is earlier in UTC.",
                    "supersedes_decision_id": "decision-test-first",
                },
            ]
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("out of chronological order", result.stdout)

    def test_authoritative_baseline_rejects_deleted_decision_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline"
            candidate = root / "candidate"
            copy_schema_fixture(baseline)
            path = baseline / "examples" / "fictional" / "person-jules-okafor.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["communication_boundary"]["restriction_history"] = [
                {
                    "decision_id": "decision-jules-do-not-contact",
                    "state": "do_not_contact",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-01T12:00:00Z",
                    "reason": "The fictional recipient requested no contact."
                }
            ]
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            shutil.copytree(baseline, candidate)
            candidate_path = candidate / "examples" / "fictional" / "person-jules-okafor.json"
            candidate_record = json.loads(candidate_path.read_text(encoding="utf-8"))
            candidate_record["communication_boundary"]["restriction_history"] = [
                {
                    "decision_id": "decision-jules-reopened",
                    "state": "none",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-02T12:00:00Z",
                    "reason": "The old restriction was silently replaced."
                }
            ]
            candidate_path.write_text(json.dumps(candidate_record, indent=2) + "\n", encoding="utf-8")

            result = run_schemas(candidate, baseline)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("rewrites authoritative decision history", result.stdout)

    def test_authoritative_baseline_must_exist_and_contain_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = root / "candidate"
            copy_schema_fixture(candidate)
            for baseline in (root / "missing", root / "empty"):
                with self.subTest(baseline=baseline.name):
                    if baseline.name == "empty":
                        baseline.mkdir()
                    result = run_schemas(candidate, baseline)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn("authoritative baseline", result.stdout)

    def test_schema3_initial_consent_decision_preserves_schema2_baseline_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            baseline = root / "baseline"
            candidate = root / "candidate"
            copy_schema_fixture(baseline)
            baseline_path = baseline / "examples" / "fictional" / "person-jules-okafor.json"
            baseline_record = json.loads(baseline_path.read_text(encoding="utf-8"))
            baseline_record["communication_boundary"]["consent_status"] = "opted_out"
            baseline_record["communication_boundary"].pop("consent_history")
            baseline_path.write_text(json.dumps(baseline_record, indent=2) + "\n", encoding="utf-8")
            shutil.copytree(baseline, candidate)
            candidate_path = candidate / "examples" / "fictional" / "person-jules-okafor.json"
            candidate_record = json.loads(candidate_path.read_text(encoding="utf-8"))
            candidate_record["communication_boundary"]["consent_status"] = "opted_in"
            candidate_record["communication_boundary"]["consent_history"] = [
                {
                    "decision_id": "decision-jules-consent-rewritten",
                    "state": "opted_in",
                    "decided_by_person_id": "person-lina-moreno",
                    "decided_at": "2026-08-02T12:00:00Z",
                    "reason": "The authoritative opt-out was not preserved.",
                }
            ]
            candidate_path.write_text(json.dumps(candidate_record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(candidate, baseline)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("initial consent decision does not preserve authoritative baseline status", result.stdout)

    def test_verified_or_high_confidence_records_require_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "opportunity-accessible-starter-guide.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["status"] = "verified"
            record["confidence"] = "high"
            record["evidence_ids"] = []
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("verified or high-confidence record requires evidence", result.stdout)

    def test_evidence_ids_must_reference_evidence_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "opportunity-accessible-starter-guide.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["status"] = "verified"
            record["confidence"] = "high"
            record["evidence_ids"] = ["person-jules-okafor"]
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("evidence_ids references non-evidence record person-jules-okafor", result.stdout)

    def test_record_update_cannot_precede_creation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["updated_at"] = "2026-07-31T12:00:00Z"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("updated_at precedes created_at", result.stdout)

    def test_consent_status_must_match_append_only_consent_history(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["communication_boundary"]["consent_status"] = "opted_in"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("consent status must match the latest consent decision", result.stdout)

    def test_event_end_cannot_precede_start(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "event-riverbend-accessibility-lab.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["ends_at"] = "2026-07-31T12:00:00Z"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("event ends_at precedes starts_at", result.stdout)

    def test_evidence_staleness_cannot_precede_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "evidence-riverbend-program.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["stale_after"] = "2026-07-31"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("evidence stale_after precedes accessed_at", result.stdout)

    def test_interaction_commitments_require_due_state_and_completion_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "interaction-riverbend-planning-session.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["commitments"][0].pop("due_state", None)
            record["commitments"][0].pop("completion_evidence_ids", None)
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("'due_state' is a required property", result.stdout)
        self.assertIn("'completion_evidence_ids' is a required property", result.stdout)

    def test_unknown_commitment_due_state_requires_a_reason(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "interaction-riverbend-planning-session.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["commitments"][0]["status"] = "open"
            record["commitments"][0]["completion_evidence_ids"] = []
            record["commitments"][0]["due_state"] = {"state": "unknown", "reason": "Timing has not been agreed."}
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            valid = run_schemas(fixture)
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
            record["commitments"][0]["due_state"] = "unknown"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            invalid = run_schemas(fixture)
        self.assertNotEqual(0, invalid.returncode)

    def test_contribution_requires_owner_delivery_care_and_stop_conditions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "contribution-accessible-starter-guide.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            for field in (
                "owner_id",
                "scope",
                "due_window",
                "accessibility_check",
                "maintenance_or_handoff",
                "risks",
                "stop_conditions",
            ):
                record.pop(field, None)
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        for field in ("owner_id", "scope", "due_window", "accessibility_check", "maintenance_or_handoff", "risks", "stop_conditions"):
            self.assertIn(f"'{field}' is a required property", result.stdout)

    def test_completed_contribution_requires_coherent_completion_evidence_and_review(self) -> None:
        cases = {
            "evidence": lambda record: record.update({"completion_evidence_ids": []}),
            "due_window": lambda record: record.update({"due_window": {"state": "planned"}}),
            "accessibility": lambda record: record.update(
                {"accessibility_check": {"status": "pending", "evidence_ids": [], "notes": "Still pending."}}
            ),
            "accessibility_evidence": lambda record: record.update(
                {"accessibility_check": {"status": "passed", "evidence_ids": [], "notes": "Unsupported pass."}}
            ),
        }
        for case, mutate in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                copy_schema_fixture(fixture)
                path = fixture / "examples" / "fictional" / "contribution-accessible-starter-guide.json"
                record = json.loads(path.read_text(encoding="utf-8"))
                record["status"] = "completed"
                record["due_window"] = {"state": "completed"}
                record["accessibility_check"] = {
                    "status": "passed",
                    "evidence_ids": ["evidence-riverbend-planning-session"],
                    "notes": "The fictional review passed.",
                }
                record["completion_evidence_ids"] = ["evidence-riverbend-planning-session"]
                mutate(record)
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                result = run_schemas(fixture)
            self.assertNotEqual(0, result.returncode)

    def test_commitment_status_and_due_state_must_agree(self) -> None:
        cases = (("completed", "overdue"), ("cancelled", "planned"), ("open", "completed"))
        for commitment_status, due_state in cases:
            with self.subTest(status=commitment_status, due_state=due_state), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                copy_schema_fixture(fixture)
                path = fixture / "examples" / "fictional" / "interaction-riverbend-planning-session.json"
                record = json.loads(path.read_text(encoding="utf-8"))
                record["commitments"][0]["status"] = commitment_status
                record["commitments"][0]["due_state"] = due_state
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                result = run_schemas(fixture)
            self.assertNotEqual(0, result.returncode)

    def test_unknown_contribution_due_window_requires_a_reason(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "contribution-accessible-starter-guide.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["due_window"] = {"state": "unknown", "reason": "The community has not agreed on timing."}
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            valid = run_schemas(fixture)
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
            record["due_window"] = {"state": "unknown"}
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            invalid = run_schemas(fixture)
        self.assertNotEqual(0, invalid.returncode)

    def test_reflection_requires_evidence_interpretation_burden_scope_and_readers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "reflection-riverbend-planning.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            for field in (
                "observed_evidence",
                "interpretation",
                "beneficiaries",
                "burdens",
                "lesson_scope",
                "artifact_review_targets",
                "authorized_reader_scope",
            ):
                record.pop(field, None)
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertNotEqual(0, result.returncode)
        for field in (
            "observed_evidence",
            "interpretation",
            "beneficiaries",
            "burdens",
            "lesson_scope",
            "artifact_review_targets",
            "authorized_reader_scope",
        ):
            self.assertIn(f"'{field}' is a required property", result.stdout)

    def test_partially_known_person_uses_structured_unknowns_without_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "person-jules-okafor.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["display_name"] = {"state": "unknown", "reason": "Identity is not yet verified."}
            record["summary"] = {"state": "unknown", "reason": "No supported summary is available."}
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_partially_known_organization_uses_structured_unknowns_without_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "organization-riverbend-learning.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            record["name"] = {"state": "unknown", "reason": "The public identity is not yet verified."}
            record["mission_summary"] = {"state": "unknown", "reason": "No authoritative mission statement is available."}
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_partially_known_event_preserves_unknown_volatile_facts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            copy_schema_fixture(fixture)
            path = fixture / "examples" / "fictional" / "event-riverbend-accessibility-lab.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            unknown = {"state": "unknown", "reason": "The public event detail is not yet verified."}
            for field in ("format", "starts_at", "ends_at", "location_summary", "accessibility_summary"):
                record[field] = unknown
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            result = run_schemas(fixture)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_event_known_fields_reject_placeholder_unknowns(self) -> None:
        for placeholder in ("TBD", "unknown", "To Be Determined", "N/A"):
            with self.subTest(placeholder=placeholder), tempfile.TemporaryDirectory() as directory:
                fixture = Path(directory)
                copy_schema_fixture(fixture)
                path = fixture / "examples" / "fictional" / "event-riverbend-accessibility-lab.json"
                record = json.loads(path.read_text(encoding="utf-8"))
                record["accessibility_summary"] = placeholder
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                result = run_schemas(fixture)
            self.assertNotEqual(0, result.returncode)

    def test_portable_profile_preserves_capacity_cadence_and_approver_authority(self) -> None:
        record = json.loads(
            (ROOT / "examples" / "fictional" / "profile-riverbend-learning.json").read_text(encoding="utf-8")
        )
        self.assertIn("capacity", record)
        self.assertIn("review_cadence", record)
        self.assertIn("accountable_human_id", record)
        self.assertIn("authorized_outreach_approver_ids", record)

    def test_riverbend_material_claims_use_claim_specific_evidence(self) -> None:
        expected_evidence = {
            "organization-riverbend-learning.json": "evidence-riverbend-organization-profile",
            "person-jules-okafor.json": "evidence-jules-accessibility-review-role",
            "person-lina-moreno.json": "evidence-lina-community-facilitator-role",
            "event-riverbend-accessibility-lab.json": "evidence-riverbend-accessibility-lab-details",
            "interaction-riverbend-planning-session.json": "evidence-riverbend-planning-session",
            "relationship-lina-jules.json": "evidence-riverbend-planning-session",
        }
        for filename, evidence_id in expected_evidence.items():
            with self.subTest(filename=filename):
                record = json.loads((ROOT / "examples" / "fictional" / filename).read_text(encoding="utf-8"))
                self.assertIn(evidence_id, record["evidence_ids"])

    def test_breaking_portable_record_changes_use_schema_v3_and_publish_migrations(self) -> None:
        common = json.loads((ROOT / "schemas" / "common.schema.json").read_text(encoding="utf-8"))
        self.assertEqual("3.0.0", common["$defs"]["record"]["properties"]["schema_version"]["const"])
        for path in sorted((ROOT / "examples" / "fictional").glob("*.json")):
            with self.subTest(path=path.name):
                record = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("3.0.0", record["schema_version"])
                self.assertEqual("1.0.0-rc.2", record["framework_version"])
        self.assertTrue((ROOT / "project" / "migrations" / "portable-records-1-to-2.md").is_file())
        self.assertTrue((ROOT / "project" / "migrations" / "portable-records-2-to-3.md").is_file())
        for filename in ("portable-records-1-to-2.md", "portable-records-2-to-3.md"):
            migration = (ROOT / "project" / "migrations" / filename).read_text(encoding="utf-8").lower()
            self.assertIn("deprecation window", migration)


if __name__ == "__main__":
    unittest.main()
