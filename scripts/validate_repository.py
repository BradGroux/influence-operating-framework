#!/usr/bin/env python3
"""Validate the documentation integrity of the framework repository."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "README.md",
    "LICENSE",
    "GOVERNANCE.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "VERSION",
    "framework/README.md",
    "framework/charter.md",
    "framework/operating-framework.md",
    "framework/practice-method.md",
    "framework/responsible-practice-standard.md",
    "framework/measurement-and-learning.md",
    "framework/glossary.md",
    "decisions/README.md",
    "decisions/0001-business-framework-not-technical-specification.md",
    "examples/README.md",
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

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
}

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
VERSION = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
MERMAID_START = re.compile(
    r"^(?:flowchart|graph|sequenceDiagram|classDiagram|stateDiagram(?:-v2)?|"
    r"erDiagram|journey|gantt|pie|mindmap|timeline|quadrantChart)\b"
)


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def github_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return re.sub(r"[ ]+", "-", text)


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
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(maxsplit=1)[0]
    path, separator, fragment = target.partition("#")
    return unquote(path), unquote(fragment) if separator else ""


def validate_structure(errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for relative in REMOVED_TECHNICAL_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"superseded technical path remains: {relative}")

    version_path = ROOT / "VERSION"
    if version_path.is_file():
        value = version_path.read_text(encoding="utf-8").strip()
        if not VERSION.fullmatch(value):
            errors.append(f"invalid VERSION value: {value!r}")
        else:
            for relative in ("README.md", "CHANGELOG.md", "framework/charter.md"):
                document = ROOT / relative
                if document.is_file() and value not in document.read_text(encoding="utf-8"):
                    errors.append(
                        f"release-facing document does not name VERSION {value}: {relative}"
                    )


def validate_markdown(files: list[Path], errors: list[str]) -> tuple[int, int]:
    anchor_cache: dict[Path, set[str]] = {}
    link_count = 0
    mermaid_count = 0

    for path in files:
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        if not lines or not lines[0].startswith("# "):
            errors.append(f"Markdown file must begin with one H1: {relative}")

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
                            f"Mermaid block has no recognized diagram declaration: "
                            f"{relative}:{line_number}"
                        )
                    in_fence = False
                    fence_language = ""
                continue

            if in_fence and fence_language == "mermaid" and line.strip():
                if MERMAID_START.match(line.strip()):
                    mermaid_has_body = True

        if in_fence:
            errors.append(f"unclosed code fence: {relative}")

        for match in MARKDOWN_LINK.finditer(text):
            link_count += 1
            target_path, fragment = split_link(match.group(1))

            if target_path.startswith(("http://", "https://", "mailto:")):
                continue

            resolved = path if not target_path else (path.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"link escapes repository: {relative} -> {match.group(1)}")
                continue

            if not resolved.exists():
                errors.append(f"broken local link: {relative} -> {match.group(1)}")
                continue

            if fragment and resolved.suffix.lower() == ".md":
                if resolved not in anchor_cache:
                    anchor_cache[resolved] = heading_anchors(
                        resolved.read_text(encoding="utf-8")
                    )
                if fragment.lower() not in anchor_cache[resolved]:
                    errors.append(
                        f"missing Markdown anchor: {relative} -> {match.group(1)}"
                    )

    return link_count, mermaid_count


def main() -> int:
    errors: list[str] = []
    files = markdown_files()

    validate_structure(errors)
    link_count, mermaid_count = validate_markdown(files, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"PASS: required structure: {len(REQUIRED_FILES)} files")
    print(f"PASS: Markdown documents: {len(files)}")
    print(f"PASS: local and external Markdown links inspected: {link_count}")
    print(f"PASS: inline Mermaid blocks: {mermaid_count}")
    print("PASS: superseded technical framework paths are absent")
    print("All repository document checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
