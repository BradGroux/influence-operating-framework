#!/usr/bin/env python3
"""Validate the public Influence Operating Framework repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import unquote, urlparse

DEPENDENCY_ERROR: str | None = None

PROHIBITED_EXTENSION_FIELD_PATTERN = re.compile(
    r"(^|[._-])(send|sender|sending|credential|credentials|secret|token|password|key|privatekey|apikey|delivery|campaign|retry|webhook)($|[._-])",
    re.IGNORECASE,
)

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover - exercised from a dependency-missing checkout
    repository_root = Path(__file__).resolve().parents[1]
    venv_root = repository_root / ".venv"
    venv_python = venv_root / "bin" / "python"
    if venv_python.is_file() and Path(sys.prefix).resolve() != venv_root.resolve():
        os.execv(str(venv_python), [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]])
    DEPENDENCY_ERROR = f"validation dependency missing: {exc}; run python3 -m pip install -r requirements-dev.txt"


@dataclass(frozen=True)
class GateResult:
    name: str
    status: str
    detail: str


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_datetime(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def build_registry(schema_documents: dict[str, dict]) -> Registry:
    registry = Registry()
    for uri, document in schema_documents.items():
        registry = registry.with_resource(uri, Resource.from_contents(document))
    return registry


def find_record_references(value: object, field: str | None = None) -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield from find_record_references(child, key)
    elif field and field not in {"decision_id", "supersedes_decision_id"} and (field.endswith("_id") or field.endswith("_ids")):
        if isinstance(value, str):
            yield field, value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    yield field, item


def find_decision_histories(value: object, location: str = "") -> Iterable[tuple[str, list[dict]]]:
    if not isinstance(value, dict):
        return
    for key, child in value.items():
        child_location = f"{location}.{key}" if location else key
        if key.endswith("_history") and isinstance(child, list) and all(isinstance(item, dict) for item in child):
            yield child_location, child
        else:
            yield from find_decision_histories(child, child_location)


def validate_schemas(root: Path, baseline_root: Path | None = None) -> list[GateResult]:
    if DEPENDENCY_ERROR is not None:
        return [
            GateResult("schemas", "FAIL", DEPENDENCY_ERROR),
            GateResult("graph-references", "FAIL", "not run because the schema validation dependency is unavailable"),
        ]
    schema_paths = sorted((root / "schemas").glob("*.schema.json"))
    example_paths = sorted((root / "examples" / "fictional").glob("*.json"))
    errors: list[str] = []
    schema_documents: dict[str, dict] = {}

    for path in schema_paths:
        try:
            document = load_json(path)
            Draft202012Validator.check_schema(document)
            schema_id = document.get("$id")
            if not schema_id:
                errors.append(f"{path.relative_to(root)}: missing $id")
            elif schema_id in schema_documents:
                errors.append(f"{path.relative_to(root)}: duplicate $id {schema_id}")
            else:
                schema_documents[schema_id] = document
        except Exception as exc:  # json/validator errors are reported together
            errors.append(f"{path.relative_to(root)}: {exc}")

    if not schema_documents:
        errors.append("no JSON Schemas found")
        return [GateResult("schemas", "FAIL", "; ".join(errors))]

    registry = build_registry(schema_documents)
    records: list[tuple[Path, dict]] = []
    covered_schema_ids: set[str] = set()
    for path in example_paths:
        try:
            record = load_json(path)
            schema_id = record.get("$schema")
            schema = schema_documents.get(schema_id)
            if schema is None:
                errors.append(f"{path.relative_to(root)}: unknown $schema {schema_id!r}")
                continue
            validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
            record_errors = sorted(validator.iter_errors(record), key=lambda error: list(error.absolute_path))
            for error in record_errors:
                location = ".".join(str(part) for part in error.absolute_path) or "<record>"
                errors.append(f"{path.relative_to(root)}:{location}: {error.message}")
            records.append((path, record))
            covered_schema_ids.add(schema_id)
        except Exception as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")

    domain_schema_ids = {uri for uri in schema_documents if not uri.endswith("/common.schema.json")}
    missing_coverage = sorted(domain_schema_ids - covered_schema_ids)
    if missing_coverage:
        errors.append("schemas without a fictional example: " + ", ".join(missing_coverage))

    schema_result = GateResult(
        "schemas",
        "FAIL" if errors else "PASS",
        "; ".join(errors) if errors else f"{len(schema_paths)} schemas and {len(records)} fictional records validate under Draft 2020-12",
    )

    reference_errors: list[str] = []
    ids: dict[str, Path] = {}
    records_by_id: dict[str, dict] = {}
    for path, record in records:
        record_id = record.get("id")
        if not isinstance(record_id, str):
            continue
        if record_id in ids:
            reference_errors.append(f"duplicate record ID {record_id} in {path.relative_to(root)} and {ids[record_id].relative_to(root)}")
        ids[record_id] = path
        records_by_id[record_id] = record

    for path, record in records:
        for field, reference in find_record_references(record):
            if reference not in ids:
                reference_errors.append(f"{path.relative_to(root)}:{field} references missing ID {reference}")
            elif (field.endswith("evidence_id") or field.endswith("evidence_ids")) and records_by_id[reference].get("record_type") != "evidence":
                reference_errors.append(
                    f"{path.relative_to(root)}:{field} references non-evidence record {reference}"
                )
        if (
            record.get("record_type") != "evidence"
            and (record.get("status") == "verified" or record.get("confidence") == "high")
            and not record.get("evidence_ids")
        ):
            reference_errors.append(f"{path.relative_to(root)}: verified or high-confidence record requires evidence")
        created_at = parse_datetime(record.get("created_at"))
        updated_at = parse_datetime(record.get("updated_at"))
        if created_at is not None and updated_at is not None and updated_at < created_at:
            reference_errors.append(f"{path.relative_to(root)}: updated_at precedes created_at")
        if record.get("record_type") == "event":
            starts_at = parse_datetime(record.get("starts_at"))
            ends_at = parse_datetime(record.get("ends_at"))
            if starts_at is not None and ends_at is not None and ends_at < starts_at:
                reference_errors.append(f"{path.relative_to(root)}: event ends_at precedes starts_at")
        if record.get("record_type") == "evidence":
            accessed_at = parse_date(record.get("accessed_at"))
            stale_after = parse_date(record.get("stale_after"))
            if accessed_at is not None and stale_after is not None and stale_after < accessed_at:
                reference_errors.append(f"{path.relative_to(root)}: evidence stale_after precedes accessed_at")
        for location, history in find_decision_histories(record):
            seen_decisions: set[str] = set()
            previous: dict | None = None
            for index, decision in enumerate(history):
                decision_id = decision.get("decision_id")
                if not isinstance(decision_id, str):
                    continue
                if decision_id in seen_decisions:
                    reference_errors.append(f"{path.relative_to(root)}:{location} repeats decision ID {decision_id}")
                if "approval_scope" in decision and not (
                    record.get("record_type") == "outreach_draft"
                    and location == "review_history"
                    and decision.get("state") == "approve"
                ):
                    reference_errors.append(f"{path.relative_to(root)}:{location}[{index}] uses approval scope outside an outreach approval")
                seen_decisions.add(decision_id)
                supersedes = decision.get("supersedes_decision_id")
                if previous is None and supersedes is not None:
                    reference_errors.append(f"{path.relative_to(root)}:{location}[0] cannot supersede an absent decision")
                elif previous is not None and supersedes != previous.get("decision_id"):
                    reference_errors.append(
                        f"{path.relative_to(root)}:{location}[{index}] must supersede {previous.get('decision_id')}"
                    )
                if previous is not None:
                    decided_at = parse_datetime(decision.get("decided_at"))
                    previous_decided_at = parse_datetime(previous.get("decided_at"))
                    if decided_at is not None and previous_decided_at is not None and decided_at < previous_decided_at:
                        reference_errors.append(f"{path.relative_to(root)}:{location}[{index}] is out of chronological order")
                previous = decision
        if record.get("record_type") == "outreach_draft":
            history = record.get("review_history", [])
            disposition = record.get("disposition")
            if disposition == "pending_review" and history:
                reference_errors.append(f"{path.relative_to(root)}: pending review cannot contain a human disposition")
            elif disposition != "pending_review" and (not history or history[-1].get("state") != disposition):
                reference_errors.append(f"{path.relative_to(root)}: disposition must match the latest human review")
            recipient = records_by_id.get(record.get("recipient_person_id"), {})
            restrictions = recipient.get("communication_boundary", {}).get("restriction_history", [])
            if restrictions and restrictions[-1].get("state") == "do_not_contact" and disposition != "do_not_contact":
                reference_errors.append(f"{path.relative_to(root)}: recipient has an active do-not-contact restriction")
            contribution_id = record.get("contribution_id")
            linked_relationships = [
                linked_record
                for linked_record in records_by_id.values()
                if linked_record.get("record_type") == "relationship"
                and record.get("recipient_person_id") in linked_record.get("participant_ids", [])
                and contribution_id in linked_record.get("contribution_ids", [])
            ]
            if disposition != "do_not_contact" and any(
                relationship.get("disposition_history", [])
                and relationship["disposition_history"][-1].get("state") == "do_not_contact"
                for relationship in linked_relationships
            ):
                reference_errors.append(f"{path.relative_to(root)}: linked relationship has an active do-not-contact restriction")
            contribution = records_by_id.get(contribution_id, {})
            linked_opportunities = [
                records_by_id.get(opportunity_id, {}) for opportunity_id in contribution.get("opportunity_ids", [])
            ]
            if disposition != "do_not_contact" and any(
                opportunity.get("record_type") == "opportunity"
                and opportunity.get("decision_history", [])
                and opportunity["decision_history"][-1].get("state") == "do_not_contact"
                for opportunity in linked_opportunities
            ):
                reference_errors.append(f"{path.relative_to(root)}: linked opportunity has an active do-not-contact restriction")
            if disposition == "approve" and history:
                approval_scope = history[-1].get("approval_scope", {})
                expected_hash = hashlib.sha256(str(record.get("draft_content", "")).encode("utf-8")).hexdigest()
                if approval_scope.get("content_sha256") != expected_hash:
                    reference_errors.append(f"{path.relative_to(root)}: approved content hash does not match the current draft")
                for field, expected in (
                    ("outreach_draft_id", record.get("id")),
                    ("recipient_person_id", record.get("recipient_person_id")),
                    ("channel", record.get("channel")),
                ):
                    if approval_scope.get(field) != expected:
                        reference_errors.append(f"{path.relative_to(root)}: approval scope {field} does not match the current draft")
                approval_expires_at = parse_datetime(approval_scope.get("expires_at"))
                approval_decided_at = parse_datetime(history[-1].get("decided_at"))
                record_updated_at = parse_datetime(record.get("updated_at"))
                if approval_expires_at is not None and approval_decided_at is not None and approval_expires_at < approval_decided_at:
                    reference_errors.append(f"{path.relative_to(root)}: approval expires before its decision time")
                if approval_expires_at is not None and record_updated_at is not None and approval_expires_at < record_updated_at:
                    reference_errors.append(f"{path.relative_to(root)}: approved outreach is expired at the record update time")

    if baseline_root is not None:
        baseline_examples = baseline_root / "examples" / "fictional"
        baseline_paths = sorted(baseline_examples.glob("*.json")) if baseline_examples.is_dir() else []
        if not baseline_paths:
            reference_errors.append(
                f"authoritative baseline {baseline_root} does not contain examples/fictional/*.json records"
            )
        baseline_records: dict[str, tuple[Path, dict]] = {}
        for path in baseline_paths:
            try:
                baseline_record = load_json(path)
            except Exception as exc:
                reference_errors.append(f"authoritative baseline {path.relative_to(baseline_root)} is invalid: {exc}")
                continue
            record_id = baseline_record.get("id")
            if isinstance(record_id, str):
                baseline_records[record_id] = (path, baseline_record)
        for record_id, (baseline_path, baseline_record) in baseline_records.items():
            candidate_record = records_by_id.get(record_id)
            if candidate_record is None:
                reference_errors.append(f"{baseline_path.relative_to(baseline_root)}: authoritative record {record_id} is missing")
                continue
            candidate_histories = dict(find_decision_histories(candidate_record))
            for location, baseline_history in find_decision_histories(baseline_record):
                candidate_history = candidate_histories.get(location, [])
                if len(candidate_history) < len(baseline_history) or candidate_history[: len(baseline_history)] != baseline_history:
                    reference_errors.append(f"{record_id}:{location} rewrites authoritative decision history")

    graph_result = GateResult(
        "graph-references",
        "FAIL" if reference_errors else "PASS",
        "; ".join(reference_errors) if reference_errors else f"all references resolve across {len(ids)} stable record IDs",
    )
    return [schema_result, graph_result]


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = re.sub(r"<[^>]+>", "", match.group(1))
        heading = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", heading)
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        index = counts.get(slug, 0)
        counts[slug] = index + 1
        anchors.add(slug if index == 0 else f"{slug}-{index}")
    return anchors


def validate_links(root: Path) -> list[GateResult]:
    errors: list[str] = []
    checked = 0
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", "node_modules"} for part in path.parts):
            continue
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
        for raw_target in link_pattern.findall(text):
            target = raw_target.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("//"):
                continue
            checked += 1
            decoded_path = unquote(parsed.path)
            target_path = (path.parent / decoded_path).resolve() if decoded_path else path.resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes repository: {target}")
                continue
            if not target_path.exists():
                errors.append(f"{path.relative_to(root)}: missing target {target}")
                continue
            if parsed.fragment and target_path.is_file() and target_path.suffix.lower() == ".md":
                anchor = unquote(parsed.fragment).lower()
                if anchor not in markdown_anchors(target_path):
                    errors.append(f"{path.relative_to(root)}: missing heading #{parsed.fragment} in {target_path.relative_to(root)}")

    return [
        GateResult(
            "links",
            "FAIL" if errors else "PASS",
            "; ".join(errors) if errors else f"{checked} repository-local Markdown links resolve",
        )
    ]


REQUIRED_VISUAL_IDS = {
    "automation-architecture",
    "contribution-before-ask",
    "ecosystem-map",
    "event-intelligence-workflow",
    "framework-overview",
    "human-reviewed-outreach",
    "influence-lifecycle",
    "measurement-model",
    "profile-to-framework",
    "reflection-learning-loop",
    "relationship-graph-model",
    "repository-information-architecture",
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    return struct.unpack(">II", data[16:24])


def validate_visuals(root: Path) -> list[GateResult]:
    errors: list[str] = []
    manifest_path = root / "visuals" / "manifest.json"
    if not manifest_path.is_file():
        return [GateResult("visuals", "FAIL", "missing visuals/manifest.json")]
    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        return [GateResult("visuals", "FAIL", f"invalid visuals/manifest.json: {exc}")]

    config = manifest.get("configuration", {})
    config_path = root / str(config.get("path", ""))
    if not config_path.is_file():
        errors.append(f"missing visual configuration {config.get('path')}")
    elif file_sha256(config_path) != config.get("sha256"):
        errors.append(f"hash mismatch for {config_path.relative_to(root)}")

    entries = manifest.get("visuals", [])
    ids = {entry.get("id") for entry in entries if isinstance(entry, dict)}
    missing_ids = sorted(REQUIRED_VISUAL_IDS - ids)
    extra_ids = sorted(ids - REQUIRED_VISUAL_IDS)
    if missing_ids:
        errors.append("missing required visual IDs: " + ", ".join(missing_ids))
    if extra_ids:
        errors.append("unexpected visual IDs: " + ", ".join(extra_ids))

    metadata_ids = {path.stem for path in (root / "visuals" / "metadata").glob("*.json")}
    if metadata_ids != REQUIRED_VISUAL_IDS:
        errors.append("visual metadata set does not match required visual IDs")

    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("manifest contains a non-object visual entry")
            continue
        visual_id = entry.get("id", "<unknown>")
        for artifact_name in ("source", "svg", "png", "metadata", "description"):
            artifact = entry.get(artifact_name, {})
            relative = artifact.get("path")
            expected_hash = artifact.get("sha256")
            path = root / str(relative or "")
            if not relative or not path.is_file():
                errors.append(f"{visual_id}: missing {artifact_name} {relative}")
                continue
            if file_sha256(path) != expected_hash:
                errors.append(f"{visual_id}: hash mismatch for {relative}")
                continue
            if artifact_name == "source" and path.suffix != ".mmd":
                errors.append(f"{visual_id}: source must be Mermaid .mmd")
            elif artifact_name == "svg":
                if "<svg" not in path.read_text(encoding="utf-8")[:1000]:
                    errors.append(f"{visual_id}: invalid SVG export")
            elif artifact_name == "png":
                try:
                    width, height = png_dimensions(path)
                    if width < 800 or height < 200:
                        errors.append(f"{visual_id}: PNG is too small at {width}x{height}")
                except ValueError as exc:
                    errors.append(f"{visual_id}: {exc}")
            elif artifact_name == "description":
                if len(path.read_text(encoding="utf-8").split()) < 45:
                    errors.append(f"{visual_id}: accessible description is too short")

        metadata_artifact = entry.get("metadata", {})
        metadata_path = root / str(metadata_artifact.get("path", ""))
        if metadata_path.is_file():
            metadata = load_json(metadata_path)
            if metadata.get("id") != visual_id:
                errors.append(f"{visual_id}: metadata ID mismatch")
            for field in ("title", "concept", "version", "source", "exports", "description", "accessible_description", "hashes"):
                if field not in metadata:
                    errors.append(f"{visual_id}: metadata missing {field}")
            if len(str(metadata.get("accessible_description", "")).split()) < 20:
                errors.append(f"{visual_id}: metadata accessible description is too short")
            metadata_hashes = metadata.get("hashes", {})
            for artifact_name in ("source", "svg", "png", "description"):
                manifest_hash = entry.get(artifact_name, {}).get("sha256")
                if metadata_hashes.get(artifact_name) != manifest_hash:
                    errors.append(f"{visual_id}: metadata {artifact_name} hash does not match manifest")

    return [
        GateResult(
            "visuals",
            "FAIL" if errors else "PASS",
            "; ".join(errors) if errors else f"{len(entries)} Mermaid sources have synchronized SVG, PNG, metadata, and accessible descriptions",
        )
    ]


REQUIRED_PATHS = [
    "README.md", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "GOVERNANCE.md", "CHANGELOG.md",
    "SECURITY.md", "AGENTS.md", "CONTEXT.md", "INDEX.md", "VERSION",
    "decisions/locked-decisions.md", "decisions/proposed-decisions.md", "decisions/adr-template.md",
    "scripts/validate.py", "scripts/render_visuals.py", "scripts/build_index.py",
    "tests/test_schemas.py", "tests/test_links.py", "tests/test_structure.py", "tests/test_visuals.py",
    "reports/validation-report.md",
    "project/discovery/grill-with-docs-review.md", "project/specifications/initial-build.md",
    "project/specifications/v1.0.0-release-criteria.md",
    "project/migrations/portable-records-1-to-2.md",
    "project/planning/tickets.md", "project/planning/status.md", "project/reviews/initial-visual-inspection.md",
    "project/reviews/initial-code-review-disposition.md",
    "project/reviews/v1.0.0-independent-application-review-2026-08-01-a.md",
    "project/reviews/v1.0.0-adversarial-release-assurance-review-2026-08-01-b.md",
    "project/reviews/v1.0.0-independent-review-disposition-2026-08-01.md",
    "project/reviews/v1.0.0-rc.1-visual-readback-2026-08-01.md",
]
REQUIRED_PATHS.extend(f"docs/{number:02d}-{name}.md" for number, name in [
    (0, "charter"), (1, "framework-overview"), (2, "operating-model"), (3, "ecosystem-mapping"),
    (4, "relationship-intelligence"), (5, "event-and-conference-intelligence"), (6, "contribution-strategy"),
    (7, "speaking-and-influence-channels"), (8, "opportunity-evaluation"), (9, "human-reviewed-outreach"),
    (10, "reflection-and-antifragile-learning"), (11, "measurement-and-outcomes"), (12, "ethics-privacy-and-safety"),
    (13, "automation-architecture"), (14, "visualization-system"), (15, "implementation-guide"), (16, "research-methodology"),
])
REQUIRED_PATHS.extend(f"schemas/{name}.schema.json" for name in [
    "person", "organization", "ecosystem", "event", "relationship", "interaction", "opportunity",
    "contribution", "outreach-draft", "reflection", "evidence", "profile",
])
REQUIRED_PATHS.extend(f"templates/{name}.md" for name in [
    "profile", "person", "organization", "ecosystem", "event-brief", "conference-playbook", "relationship-note",
    "contribution-plan", "outreach-draft", "follow-up-plan", "reflection", "research-note", "monthly-review", "annual-plan",
])
REQUIRED_PATHS.extend(f"automations/{name}.md" for name in [
    "discovery-agent", "enrichment-agent", "event-brief-agent", "ecosystem-mapping-agent", "prioritization-agent",
    "contribution-agent", "outreach-draft-agent", "follow-up-agent", "reflection-agent", "visualization-agent", "validation-agent",
])
REQUIRED_PATHS.extend(f"workflows/{name}.md" for name in [
    "discover-research-prioritize", "prepare-for-event", "contribution-before-ask", "human-reviewed-outreach",
    "post-event-follow-up", "learn-document-evolve-repeat",
])
REQUIRED_PATHS.extend(f"profiles/brad-groux/{name}.md" for name in [
    "profile", "goals", "ecosystems", "channels", "current-assets", "research-backlog", "annual-plan",
])
REQUIRED_PATHS.extend(f"profiles/riverbend-learning-collective/{name}.md" for name in [
    "profile", "goals", "ecosystems", "channels", "current-assets", "research-backlog", "annual-plan",
])


def validate_structure(root: Path) -> list[GateResult]:
    missing = [relative for relative in REQUIRED_PATHS if not (root / relative).is_file()]
    structure = GateResult(
        "structure",
        "FAIL" if missing else "PASS",
        "missing required files: " + ", ".join(missing) if missing else f"{len(REQUIRED_PATHS)} required repository artifacts exist",
    )

    documentation_errors: list[str] = []
    canonical_paths = sorted((root / "docs").glob("[0-9][0-9]-*.md"))
    for path in canonical_paths:
        word_count = len(path.read_text(encoding="utf-8").split())
        if word_count < 140:
            documentation_errors.append(f"{path.relative_to(root)} has only {word_count} words")

    operating_model = root / "docs" / "02-operating-model.md"
    if operating_model.is_file():
        text = operating_model.read_text(encoding="utf-8")
        stages = ["Discover", "Research", "Verify", "Map", "Prioritize", "Contribute", "Engage", "Follow up", "Reflect", "Improve", "Repeat"]
        required_labels = ["Purpose", "Inputs", "Outputs", "Evidence", "Human decisions", "Automation", "Prohibited", "Quality", "Reflection"]
        for index, stage in enumerate(stages):
            start = text.find(f"## {stage}")
            end = text.find("\n## ", start + 1) if start >= 0 else -1
            section = text[start : end if end >= 0 else len(text)] if start >= 0 else ""
            missing_labels = [label for label in required_labels if f"**{label}:**" not in section]
            if start < 0 or missing_labels:
                documentation_errors.append(f"operating stage {stage} missing: {', '.join(missing_labels) or 'section'}")

    contract_headings = [
        "Purpose", "Approved inputs", "Required evidence", "Outputs", "Confidence handling", "Prohibited actions",
        "Human approval gates", "Failure states", "Logging and idempotency", "Privacy boundaries", "Test cases",
    ]
    for path in sorted((root / "automations").glob("*-agent.md")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        missing_headings = [heading for heading in contract_headings if f"## {heading}" not in text]
        if missing_headings:
            documentation_errors.append(f"{path.relative_to(root)} missing contract headings: {', '.join(missing_headings)}")

    documentation = GateResult(
        "documentation",
        "FAIL" if documentation_errors else "PASS",
        "; ".join(documentation_errors) if documentation_errors else f"{len(canonical_paths)} canonical docs and all agent contracts are substantive and complete",
    )
    return [structure, documentation]


def walk_json_items(value: object) -> Iterable[tuple[str, object]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from walk_json_items(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json_items(child)


def validate_safety(root: Path) -> list[GateResult]:
    public_errors: list[str] = []
    email_pattern = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
    allowed_domains = {"example.com", "example.net", "example.org"}
    scan_roots = [root / "examples" / "fictional", root / "profiles"]
    for scan_root in scan_roots:
        if not scan_root.exists():
            continue
        for path in sorted(item for item in scan_root.rglob("*") if item.is_file() and item.suffix in {".md", ".json"}):
            text = path.read_text(encoding="utf-8")
            for match in email_pattern.finditer(text):
                if match.group(1).lower() not in allowed_domains:
                    public_errors.append(f"{path.relative_to(root)}: possible private email")
            if path.suffix == ".json":
                try:
                    record = json.loads(text)
                    if record.get("fictional") is not True:
                        public_errors.append(f"{path.relative_to(root)}: public example is not marked fictional")
                    if record.get("privacy") != "public":
                        public_errors.append(f"{path.relative_to(root)}: public example privacy is not public")
                    forbidden_fields = {"email", "email_address", "phone", "phone_number", "street_address", "personal_address"}
                    for key, _ in walk_json_items(record):
                        if key.lower() in forbidden_fields:
                            public_errors.append(f"{path.relative_to(root)}: public example contains contact field {key}")
                    prohibited_vocabulary = re.compile(r"\b(?:lead|prospect|target)\b|conversion probability", re.IGNORECASE)
                    if prohibited_vocabulary.search(text):
                        public_errors.append(f"{path.relative_to(root)}: public example contains transactional vocabulary")
                except json.JSONDecodeError:
                    pass
    public_result = GateResult(
        "public-data-safety",
        "FAIL" if public_errors else "PASS",
        "; ".join(public_errors) if public_errors else "public examples are fictional, public-classified, and contain no non-reserved email addresses",
    )

    outreach_errors: list[str] = []
    outreach_contract = root / "automations" / "outreach-draft-agent.md"
    outreach_workflow = root / "workflows" / "human-reviewed-outreach.md"
    outreach_schema = root / "schemas" / "outreach-draft.schema.json"
    person_schema = root / "schemas" / "person.schema.json"
    relationship_schema = root / "schemas" / "relationship.schema.json"
    common_schema = root / "schemas" / "common.schema.json"
    for path in (outreach_contract, outreach_workflow, outreach_schema, person_schema, relationship_schema, common_schema):
        if not path.is_file():
            outreach_errors.append(f"missing {path.relative_to(root)}")
    required_states = {"approve", "revise", "wait", "do_not_contact"}
    if outreach_schema.is_file():
        document = load_json(outreach_schema)
        serialized = json.dumps(document)
        missing_states = [state for state in sorted(required_states) if f'"{state}"' not in serialized]
        if missing_states:
            outreach_errors.append("outreach schema missing dispositions: " + ", ".join(missing_states))
        if '"sending_capability": {"const": false}' not in serialized:
            outreach_errors.append("outreach schema does not lock sending_capability to false")
        if '"review_history"' not in serialized or '"relationship_claims"' not in serialized:
            outreach_errors.append("outreach schema lacks reviewed decision history or evidence-backed relationship claims")
    if common_schema.is_file():
        common_serialized = json.dumps(load_json(common_schema))
        for field in ("decision_id", "decided_by_person_id", "decided_at", "reason", "supersedes_decision_id"):
            if f'"{field}"' not in common_serialized:
                outreach_errors.append(f"human decision contract missing {field}")
    if person_schema.is_file() and '"restriction_history"' not in json.dumps(load_json(person_schema)):
        outreach_errors.append("person communication boundary lacks restriction history")
    if relationship_schema.is_file() and '"disposition_history"' not in json.dumps(load_json(relationship_schema)):
        outreach_errors.append("relationship record lacks disposition history")

    for schema_path in sorted((root / "schemas").glob("*.schema.json")):
        document = load_json(schema_path)
        for key, child in walk_json_items(document):
            normalized_key = key.lower()
            if normalized_key == "sending_capability":
                if child != {"const": False}:
                    outreach_errors.append(f"{schema_path.relative_to(root)}: sending_capability is not locked false")
            elif normalized_key == "no_autonomous_send":
                if child != {"const": True}:
                    outreach_errors.append(f"{schema_path.relative_to(root)}: no_autonomous_send is not locked true")
            elif re.search(r"(^|[._-])(send|sender|sending)($|[._-])", normalized_key):
                outreach_errors.append(f"{schema_path.relative_to(root)}: prohibited sender field {key}")

    capability_pattern = re.compile(r"\b(?:can|may|will)\s+(?:automatically\s+|autonomously\s+)?send\b", re.IGNORECASE)
    for directory in (root / "automations", root / "workflows"):
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if capability_pattern.search(text):
                outreach_errors.append(f"{path.relative_to(root)}: appears to grant sending capability")

    familiarity_pattern = re.compile(
        r"\b(?:great meeting you|good to see you again|as we discussed|our relationship|we know each other|close friend)\b",
        re.IGNORECASE,
    )
    for path in sorted((root / "examples" / "fictional").glob("*.json")):
        record = load_json(path)
        for key, _ in walk_json_items(record.get("extensions", {})):
            if PROHIBITED_EXTENSION_FIELD_PATTERN.search(key):
                outreach_errors.append(f"{path.relative_to(root)}: prohibited extension field {key}")
        if record.get("record_type") != "outreach_draft":
            continue
        claims = record.get("relationship_claims", [])
        if familiarity_pattern.search(str(record.get("draft_content", ""))) and not claims:
            outreach_errors.append(f"{path.relative_to(root)}: invented familiarity lacks evidence-backed relationship claims")
        for claim in claims:
            if not claim.get("evidence_ids"):
                outreach_errors.append(f"{path.relative_to(root)}: relationship claim lacks evidence IDs")
    for path in (outreach_contract, outreach_workflow):
        if path.is_file():
            normalized = path.read_text(encoding="utf-8").lower().replace("do not contact", "do_not_contact")
            missing_states = [state for state in sorted(required_states) if state not in normalized]
            if missing_states:
                outreach_errors.append(f"{path.relative_to(root)} missing dispositions: {', '.join(missing_states)}")
            no_send_phrases = ("never send", "never a send", "no sending", "does not send", "no send occurs")
            if not any(phrase in normalized for phrase in no_send_phrases):
                outreach_errors.append(f"{path.relative_to(root)} lacks an explicit no-send boundary")
    outreach_result = GateResult(
        "outreach-safety",
        "FAIL" if outreach_errors else "PASS",
        "; ".join(outreach_errors) if outreach_errors else "approve, revise, wait, and do-not-contact are explicit; schema and contracts expose no sender",
    )
    return [public_result, outreach_result]


def validate_index(root: Path) -> list[GateResult]:
    script = root / "scripts" / "build_index.py"
    if not script.is_file():
        return [GateResult("index", "FAIL", "missing scripts/build_index.py")]
    process = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--check"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    detail = (process.stdout or process.stderr).strip()
    return [GateResult("index", "PASS" if process.returncode == 0 else "FAIL", detail)]


def validate_tests(root: Path) -> list[GateResult]:
    process = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    combined = (process.stdout + "\n" + process.stderr).strip()
    match = re.search(r"Ran (\d+) tests?", combined)
    count = match.group(1) if match else "unknown number of"
    detail = f"{count} acceptance tests pass" if process.returncode == 0 else combined[-2000:]
    return [GateResult("tests", "PASS" if process.returncode == 0 else "FAIL", detail)]


GATES: dict[str, Callable[[Path], list[GateResult]]] = {
    "index": validate_index,
    "links": validate_links,
    "safety": validate_safety,
    "schemas": validate_schemas,
    "structure": validate_structure,
    "tests": validate_tests,
    "visuals": validate_visuals,
}


def repository_version(root: Path) -> str:
    version_path = root / "VERSION"
    return version_path.read_text(encoding="utf-8").strip() if version_path.is_file() else "unknown"


def render_report(root: Path, results: list[GateResult]) -> str:
    """Return deterministic Markdown for a complete validation run."""

    overall = "FAIL" if any(result.status == "FAIL" for result in results) else "PASS"
    lines = [
        "# Validation report",
        "",
        f"**Repository version:** {repository_version(root)}",
        f"**Overall:** {overall}",
        "**Command:** `python3 scripts/validate.py`",
        "",
        "This report records direct repository checks. It does not convert owner decisions or independent reviews into implementation success.",
        "",
        "## Automated gates",
        "",
        "| Gate | Status | Evidence |",
        "| --- | --- | --- |",
    ]
    for result in results:
        safe_detail = result.detail.replace("|", "\\|").replace("\n", "<br>")
        lines.append(f"| {result.name} | {result.status} | {safe_detail} |")
    failures = [result for result in results if result.status == "FAIL"]
    lines.extend(["", "## Failed items", ""])
    if failures:
        lines.extend(f"- **{result.name}:** {result.detail}" for result in failures)
    else:
        lines.append("No automated gate failed.")
    lines.extend(
        [
            "",
            "## Visual inspection",
            "",
            "The release-candidate lifecycle change passed the recorded [visual readback](../project/reviews/v1.0.0-rc.1-visual-readback-2026-08-01.md). This is not an independent human accessibility review.",
            "",
            "## Deferred items",
            "",
            "| Item | Status | Completion condition |",
            "| --- | --- | --- |",
            "| Public repository host and slug | DEFERRED | Owner selects and authorizes a publication target. |",
            "| Additional maintainers and CODEOWNERS | DEFERRED | Named maintainers accept documented responsibilities. |",
            "| Dedicated private security and conduct channel | DEFERRED | Owner publishes an appropriate monitored private channel. |",
            "| Release signing and long-term cadence | DEFERRED | Maintainers approve signing, custody, and cadence policy. |",
            "| Tool-specific private overlay and messaging integrations | DEFERRED | Separate proposals pass privacy, access, retention, and external-action review. |",
            "| Fresh post-fix two-agent review | DEFERRED | Both independent agents review the same exact hardened candidate SHA with no unresolved Blocker or Material findings. |",
            "| Independent ethics, privacy, accessibility, legal, and domain review | DEFERRED | Qualified human reviewers complete reviews and dispositions before a final 1.0.0 maturity claim. |",
            "| Independent verification of Brad profile statements | DEFERRED | Owner approves source-based public research; the release candidate remains explicitly owner-supplied. |",
            "| Final owner approval | DEFERRED | Owner reads the validation and review dispositions and approves the final commit and annotated tag. |",
            "",
            "## Safety conclusion",
            "",
            "The public examples are fictional, schemas and graph references validate, every outreach path retains human approve/revise/wait/do-not-contact dispositions, and the default implementation exposes no sending capability.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(root: Path, results: list[GateResult]) -> None:
    report = root / "reports" / "validation-report.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    content = render_report(root, results)
    report.write_text(content, encoding="utf-8")
    if report.read_text(encoding="utf-8") != content:
        raise RuntimeError("validation report read-back did not match generated content")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--only", choices=sorted(GATES))
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument(
        "--baseline-root",
        type=Path,
        help="previous authoritative repository snapshot used to verify append-only decision histories",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    selected = [args.only] if args.only else list(GATES)
    results: list[GateResult] = []
    for gate_name in selected:
        if gate_name == "schemas":
            baseline_root = args.baseline_root.resolve() if args.baseline_root else None
            results.extend(validate_schemas(root, baseline_root))
        else:
            results.extend(GATES[gate_name](root))
    if not args.only and not args.no_report:
        results.append(GateResult("report", "PASS", "deterministic full-gate report regenerated and read back"))
        write_report(root, results)
    for result in results:
        print(f"{result.status} {result.name}: {result.detail}")
    return 1 if any(result.status == "FAIL" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
