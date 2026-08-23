#!/usr/bin/env python3
"""Validate repository documentation, release metadata, and public hygiene."""

from __future__ import annotations

import html
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/appeal.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/framework-contribution.yml",
    ".github/ISSUE_TEMPLATE/private-conduct-contact.yml",
    ".github/ISSUE_TEMPLATE/private-sensitive-disclosure-contact.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/signing-keys/allowed-signers",
    ".github/workflows/validate-release.yml",
    "AGENTS.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE.md",
    "README.md",
    "SECURITY.md",
    "VERSION",
    "decisions/README.md",
    "decisions/TEMPLATE.md",
    "decisions/0001-business-framework-not-technical-specification.md",
    "examples/README.md",
    "framework/README.md",
    "framework/charter.md",
    "framework/glossary.md",
    "framework/measurement-and-learning.md",
    "framework/operating-framework.md",
    "framework/practice-method.md",
    "framework/responsible-practice-standard.md",
    "project/README.md",
    "project/reviews/README.md",
    "scripts/puppeteer-ci-config.json",
    "scripts/validate-mermaid.sh",
    "scripts/validate-release.sh",
    "scripts/validate-repository.py",
    "scripts/validate-repository.sh",
)

REMOVED_TECHNICAL_PATHS = (
    "automations",
    "profiles",
    "schemas",
    "templates",
    "tests",
    "visuals",
    "workflows",
    "package.json",
    "package-lock.json",
    "requirements-dev.txt",
)

IGNORED_DIRECTORIES = {".git", ".venv", "__pycache__", "node_modules"}
PUBLIC_DOCUMENT_SUFFIXES = {".cff", ".md", ".yaml", ".yml"}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\n]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
MERMAID_START = re.compile(
    r"^(?:flowchart|graph|sequenceDiagram|classDiagram|stateDiagram(?:-v2)?|"
    r"erDiagram|journey|gantt|pie|mindmap|timeline|quadrantChart)\b"
)
REVIEW_RECORD_FILENAME = re.compile(
    r"^[a-z0-9]+(?:[.-][a-z0-9]+)*-"
    r"(?:review|disposition)-\d{4}-\d{2}-\d{2}\.md$"
)
REVIEW_STATUS = re.compile(r"^- \*\*Status:\*\* .+$", flags=re.MULTILINE)
REVIEW_DATE = re.compile(
    r"^- \*\*(?:Review|Decision|Record) date:\*\* \d{4}-\d{2}-\d{2}$",
    flags=re.MULTILINE,
)
REVIEW_ROLE = re.compile(r"^- \*\*Reviewer role:\*\* .+$", flags=re.MULTILINE)
REVIEW_COMMIT = re.compile(
    r"^- \*\*Reviewed commit:\*\* `[0-9a-f]{40}`$", flags=re.MULTILINE
)
REVIEW_FINDINGS = re.compile(r"^- \*\*Findings:\*\* (.+)$", flags=re.MULTILINE)
FINDING_HEADING = re.compile(
    r"^#### [BMNS]-\d+: .+$", flags=re.MULTILINE
)
REPOSITORY_EVIDENCE = re.compile(
    r"`([A-Za-z0-9_.\-/]+):(\d+(?:-\d+)?(?:,\d+(?:-\d+)?)*)`"
)
HISTORICAL_ATTRIBUTION = re.compile(
    r"Reviewer [A-Z]([^A-Za-z]|$)|Tester [A-Z]([^A-Za-z]|$)|"
    r"^[- ]*\*\*(Reviewer|Tester|Reviewer type|Tester type|Author):\*\*|"
    r"[A-Z]+-(HANDOFF|PROMPT)\.md",
    flags=re.IGNORECASE | re.MULTILINE,
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", flags=re.IGNORECASE
)
LOCAL_DETAIL_PATTERNS = (
    re.compile(r"/Users/"),
    re.compile(r"/private/tmp/"),
    re.compile(r"[A-Za-z]:\\Users\\"),
    re.compile(r"\bfile://", flags=re.IGNORECASE),
    re.compile(r"\blocalhost(?::\d+)?\b", flags=re.IGNORECASE),
    re.compile(r"(?:^|/)\.(?:buzz|codex)(?:/|$)"),
)
FORBIDDEN_ATTRIBUTION_PATTERNS = (
    re.compile(
        r"^\s*(?:- )?\*\*(?:Reviewer|Tester|Reviewer type|Tester type|Author):\*\*",
        flags=re.MULTILINE | re.IGNORECASE,
    ),
    re.compile(
        r"^#{1,6}\s+(?:Reviewer|Tester) Identity(?:\s+and\s+Limits)?$",
        flags=re.MULTILINE | re.IGNORECASE,
    ),
    re.compile(r"\b(?:reviewed|tested|authored)\s+by\b", flags=re.IGNORECASE),
    re.compile(
        r"\b(?:reviewer|tester)\s+(?:name|identity|called|named|is|was)\b",
        flags=re.IGNORECASE,
    ),
)
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for candidate in ROOT.rglob("*.md"):
        if any(part in IGNORED_DIRECTORIES for part in candidate.parts):
            continue
        files.append(candidate)
    return sorted(files)


def publication_text_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    files: list[Path] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        candidate = ROOT / raw_path.decode("utf-8")
        if not candidate.is_file():
            continue
        try:
            candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        files.append(candidate)
    return sorted(files)


def github_slug(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = "".join(
        character
        for character in text
        if character.isalnum() or character in {" ", "-", "_"}
    )
    return re.sub(r"\s", "-", text)


def heading_anchors(text: str) -> set[str]:
    anchors: set[str] = set()
    occurrences: defaultdict[str, int] = defaultdict(int)
    in_fence = False

    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if not match:
            continue
        base = github_slug(match.group(2))
        suffix = occurrences[base]
        occurrences[base] += 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")

    return anchors


def split_link(raw_target: str) -> tuple[str, str]:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    target = target.split(maxsplit=1)[0]
    path, separator, fragment = target.partition("#")
    return unquote(path), unquote(fragment) if separator else ""


def validate_structure(errors: list[str]) -> None:
    for required in REQUIRED_FILES:
        if not (ROOT / required).is_file():
            errors.append(f"missing required file: {required}")

    for removed in REMOVED_TECHNICAL_PATHS:
        if (ROOT / removed).exists():
            errors.append(f"superseded technical path remains: {removed}")

    for directory in ("decisions", "examples", "framework", "project", "scripts"):
        for candidate in (ROOT / directory).rglob("*"):
            if not candidate.is_file():
                continue
            if any(part in IGNORED_DIRECTORIES for part in candidate.parts):
                continue
            if candidate.name == ".DS_Store":
                continue
            if candidate.name in {"README.md", "TEMPLATE.md"}:
                continue
            if "_" in candidate.name:
                errors.append(f"filename is not kebab-case: {relative(candidate)}")


def validate_release_metadata(errors: list[str]) -> None:
    version_path = ROOT / "VERSION"
    if not version_path.is_file():
        return

    version = version_path.read_text(encoding="utf-8").strip()
    if not VERSION_PATTERN.fullmatch(version):
        errors.append(f"invalid VERSION value: {version!r}")
        return

    release_documents = (
        "README.md",
        "CHANGELOG.md",
        "CITATION.cff",
        "GOVERNANCE.md",
        "framework/charter.md",
    )
    for document_name in release_documents:
        document = ROOT / document_name
        if document.is_file() and version not in document.read_text(encoding="utf-8"):
            errors.append(
                f"release-facing document does not name VERSION {version}: {document_name}"
            )

    citation = ROOT / "CITATION.cff"
    if citation.is_file():
        text = citation.read_text(encoding="utf-8")
        expected = (
            "cff-version: 1.2.0",
            f"version: {version}",
            "date-released: 2026-08-22",
            "license: MIT",
            "repository-code: \"https://github.com/BradGroux/influence-operating-framework\"",
        )
        for value in expected:
            if value not in text:
                errors.append(f"CITATION.cff missing expected metadata: {value}")


def validate_markdown(
    files: list[Path], errors: list[str]
) -> tuple[int, int, int]:
    anchor_cache: dict[Path, set[str]] = {}
    local_link_count = 0
    external_link_count = 0
    mermaid_count = 0

    for markdown_path in files:
        name = relative(markdown_path)
        text = markdown_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        h1_exceptions = {".github/PULL_REQUEST_TEMPLATE.md", "LICENSE.md"}
        if name not in h1_exceptions:
            h1_count = sum(1 for line in lines if line.startswith("# "))
            if not lines or not lines[0].startswith("# ") or h1_count != 1:
                errors.append(f"Markdown file must begin with exactly one H1: {name}")

        in_fence = False
        fence_language = ""
        mermaid_has_body = False
        for line_number, line in enumerate(lines, start=1):
            if line.startswith("```"):
                if not in_fence:
                    in_fence = True
                    fence_language = line[3:].strip()
                    mermaid_has_body = False
                    if fence_language == "mermaid":
                        mermaid_count += 1
                else:
                    if fence_language == "mermaid" and not mermaid_has_body:
                        errors.append(
                            "Mermaid block has no recognized diagram declaration: "
                            f"{name}:{line_number}"
                        )
                    in_fence = False
                    fence_language = ""
                continue
            if in_fence and fence_language == "mermaid" and line.strip():
                if MERMAID_START.match(line.strip()):
                    mermaid_has_body = True

        if in_fence:
            errors.append(f"unclosed code fence: {name}")

        for match in MARKDOWN_LINK.finditer(text):
            target_path, fragment = split_link(match.group(1))
            if target_path.startswith(("http://", "https://", "mailto:")):
                external_link_count += 1
                continue

            local_link_count += 1
            resolved = (
                markdown_path
                if not target_path
                else (markdown_path.parent / target_path).resolve()
            )
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"link escapes repository: {name} -> {match.group(1)}")
                continue

            if not resolved.exists():
                errors.append(f"broken local link: {name} -> {match.group(1)}")
                continue

            if fragment and resolved.suffix.lower() == ".md":
                if resolved not in anchor_cache:
                    anchor_cache[resolved] = heading_anchors(
                        resolved.read_text(encoding="utf-8")
                    )
                if fragment.lower() not in anchor_cache[resolved]:
                    errors.append(
                        f"missing Markdown anchor: {name} -> {match.group(1)}"
                    )

    return local_link_count, external_link_count, mermaid_count


def repository_is_shallow() -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def validate_review_records(
    errors: list[str], shallow_repository: bool
) -> tuple[int, int, int, int]:
    records = sorted((ROOT / "project/reviews").glob("*.md"))
    checked = 0
    evidence_checked = 0
    unavailable_commit_records = 0
    unavailable_citations = 0

    for record in records:
        if record.name == "README.md":
            continue
        checked += 1
        text = record.read_text(encoding="utf-8")
        name = relative(record)

        if not REVIEW_RECORD_FILENAME.fullmatch(record.name):
            errors.append(f"nonstandard review-record filename: {name}")
        if not REVIEW_STATUS.search(text):
            errors.append(f"review record missing Status metadata: {name}")
        if not REVIEW_DATE.search(text):
            errors.append(f"review record missing ISO date metadata: {name}")

        if "-disposition-" not in record.name:
            if not REVIEW_ROLE.search(text):
                errors.append(f"review report missing generic reviewer role: {name}")
            if not REVIEW_COMMIT.search(text):
                errors.append(f"review report missing exact reviewed commit: {name}")

            reviewed_commit = REVIEW_COMMIT.search(text)
            commit = ""
            commit_available = False
            if reviewed_commit:
                commit = re.search(r"[0-9a-f]{40}", reviewed_commit.group(0)).group(0)
                commit_check = subprocess.run(
                    ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
                    cwd=ROOT,
                    capture_output=True,
                )
                if commit_check.returncode != 0:
                    if shallow_repository:
                        unavailable_commit_records += 1
                    else:
                        errors.append(
                            f"reviewed commit is not available: {name} ({commit})"
                        )
                else:
                    commit_available = True

            findings = REVIEW_FINDINGS.search(text)
            if findings:
                counts = [
                    int(value)
                    for value in re.findall(
                        r"(\d+)\s+(?:Blocker|Material|Minor|Suggestions?)",
                        findings.group(1),
                    )
                ]
                finding_headings = list(FINDING_HEADING.finditer(text))
                if any(counts) and not finding_headings:
                    errors.append(f"review report has counts but no finding sections: {name}")
                for index, heading in enumerate(finding_headings):
                    section_end = (
                        finding_headings[index + 1].start()
                        if index + 1 < len(finding_headings)
                        else len(text)
                    )
                    section = text[heading.end() : section_end]
                    if "**Evidence:**" not in section or not REPOSITORY_EVIDENCE.search(
                        section
                    ):
                        errors.append(
                            "review finding lacks repository path:line evidence: "
                            f"{name} ({heading.group(0)})"
                        )

            evidence = list(REPOSITORY_EVIDENCE.finditer(text))
            if commit and commit_available:
                source_line_counts: dict[str, int] = {}
                for citation in evidence:
                    source = citation.group(1)
                    if source not in source_line_counts:
                        source_result = subprocess.run(
                            ["git", "show", f"{commit}:{source}"],
                            cwd=ROOT,
                            check=False,
                            capture_output=True,
                            text=True,
                        )
                        if source_result.returncode != 0:
                            errors.append(
                                f"review evidence path is unavailable at commit: "
                                f"{name} ({source})"
                            )
                            source_line_counts[source] = 0
                            continue
                        source_line_counts[source] = len(
                            source_result.stdout.splitlines()
                        )
                    maximum_line = max(
                        int(value) for value in re.findall(r"\d+", citation.group(2))
                    )
                    if maximum_line > source_line_counts[source]:
                        errors.append(
                            f"review evidence exceeds source length: {name} "
                            f"({source}:{citation.group(2)})"
                        )
                    evidence_checked += 1
            elif commit and shallow_repository:
                unavailable_citations += len(evidence)

    return (
        checked,
        evidence_checked,
        unavailable_commit_records,
        unavailable_citations,
    )


def validate_public_history(errors: list[str]) -> int:
    history_ref = ""
    for candidate_ref in ("refs/heads/main", "refs/remotes/origin/main", "HEAD"):
        ref_result = subprocess.run(
            ["git", "rev-parse", "--verify", f"{candidate_ref}^{{commit}}"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        if ref_result.returncode == 0:
            history_ref = candidate_ref
            break
    if not history_ref:
        errors.append("unable to resolve public history for inspection")
        return 0

    commit_result = subprocess.run(
        ["git", "rev-list", history_ref],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if commit_result.returncode != 0:
        errors.append("unable to inspect public main history")
        return 0

    commits = [value for value in commit_result.stdout.splitlines() if value]
    metadata_result = subprocess.run(
        ["git", "log", history_ref, "--format=%an%x00%ae%x00%cn%x00%ce"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    for row in metadata_result.stdout.splitlines():
        author_name, author_email, committer_name, committer_email = row.split("\0")
        for identity_name, identity_email in (
            (author_name, author_email),
            (committer_name, committer_email),
        ):
            if identity_name == "Brad Groux" and not identity_email.endswith(
                "@users.noreply.github.com"
            ):
                errors.append(
                    "public main history exposes non-no-reply steward email metadata"
                )
                break

    for commit in commits:
        grep_result = subprocess.run(
            [
                "git",
                "grep",
                "-n",
                "-I",
                "-i",
                "-E",
                HISTORICAL_ATTRIBUTION.pattern,
                commit,
                "--",
                "*.md",
                "*.yml",
                "*.yaml",
                "*.cff",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if grep_result.returncode == 0:
            first_match = grep_result.stdout.splitlines()[0]
            errors.append(f"public main history contains legacy attribution: {first_match}")
            break
        if grep_result.returncode not in {0, 1}:
            errors.append(f"unable to scan public history commit: {commit}")
            break

    return len(commits)


def validate_publication_safety(files: list[Path], errors: list[str]) -> int:
    checked = 0
    for candidate in files:
        text = candidate.read_text(encoding="utf-8")
        name = relative(candidate)
        checked += 1

        if EMAIL_PATTERN.search(text):
            errors.append(f"public text contains an email address: {name}")
        if name != "scripts/validate-repository.py":
            for pattern in LOCAL_DETAIL_PATTERNS:
                if pattern.search(text):
                    errors.append(f"public text contains local-machine detail: {name}")
                    break
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"public text resembles a credential or private key: {name}")
                break

        if candidate.suffix.lower() in PUBLIC_DOCUMENT_SUFFIXES:
            for pattern in FORBIDDEN_ATTRIBUTION_PATTERNS:
                if pattern.search(text):
                    errors.append(
                        f"public record contains identity-based review attribution: {name}"
                    )
                    break

    return checked


def main() -> int:
    errors: list[str] = []
    documents = markdown_files()
    public_files = publication_text_files()
    shallow_repository = repository_is_shallow()

    validate_structure(errors)
    validate_release_metadata(errors)
    local_links, external_links, mermaid_blocks = validate_markdown(
        documents, errors
    )
    (
        review_records,
        review_evidence,
        unavailable_review_commits,
        unavailable_review_citations,
    ) = validate_review_records(errors, shallow_repository)
    publication_files = validate_publication_safety(public_files, errors)
    history_commits = validate_public_history(errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"PASS: required release structure: {len(REQUIRED_FILES)} files")
    print(f"PASS: Markdown documents: {len(documents)}")
    print(f"PASS: local Markdown link targets and anchors: {local_links}")
    print(f"INFO: external Markdown links not fetched: {external_links}")
    print(f"PASS: inline Mermaid source blocks: {mermaid_blocks}")
    print(f"PASS: standardized review records: {review_records}")
    if shallow_repository:
        print(
            "WARNING: shallow repository: historical review evidence is unavailable "
            f"for {unavailable_review_commits} records and "
            f"{unavailable_review_citations} "
            "citations. Run git fetch --unshallow for full history validation."
        )
        print(f"PASS: available historical review citations: {review_evidence}")
    else:
        print(f"PASS: historical review citations: {review_evidence}")
    print(f"PASS: publication-safety scan: {publication_files} text files")
    if shallow_repository:
        print(f"PASS: sanitized reachable public main history: {history_commits} commits")
    else:
        print(f"PASS: sanitized public main history: {history_commits} commits")
    print("PASS: release version and citation metadata")
    print("PASS: superseded technical framework paths are absent")
    if shallow_repository:
        print("All current-tree and reachable-history checks passed.")
    else:
        print("All repository document and publication checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
