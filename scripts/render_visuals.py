#!/usr/bin/env python3
"""Render every declared Mermaid visual and update the synchronization manifest."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VISUALS = ROOT / "visuals"
MMDC = ROOT / "node_modules" / ".bin" / "mmdc"
CONFIG = VISUALS / "mermaid-config.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_metadata() -> list[tuple[Path, dict]]:
    records: list[tuple[Path, dict]] = []
    for path in sorted((VISUALS / "metadata").glob("*.json")):
        records.append((path, json.loads(path.read_text(encoding="utf-8"))))
    if not records:
        raise RuntimeError("No visual metadata records found")
    return records


def accessible_summary(path: Path) -> str:
    paragraphs = [paragraph.replace("\n", " ").strip() for paragraph in path.read_text(encoding="utf-8").split("\n\n")]
    for paragraph in paragraphs:
        if paragraph and not paragraph.startswith("#"):
            return paragraph
    raise RuntimeError(f"Accessible description has no prose: {path.relative_to(ROOT)}")


def render(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(MMDC),
        "--quiet",
        "--input",
        str(source),
        "--output",
        str(output),
        "--configFile",
        str(CONFIG),
        "--backgroundColor",
        "#0b1020",
    ]
    if output.suffix == ".png":
        command.extend(["--width", "1600", "--scale", "2"])
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    if not MMDC.exists():
        print("Mermaid CLI is missing. Run: npm install", file=sys.stderr)
        return 2

    entries: list[dict] = []
    for metadata_path, metadata in load_metadata():
        source = ROOT / metadata["source"]
        svg = ROOT / metadata["exports"]["svg"]
        png = ROOT / metadata["exports"]["png"]
        description = ROOT / metadata["description"]
        for required in (source, description):
            if not required.is_file():
                raise RuntimeError(f"Missing required visual artifact: {required.relative_to(ROOT)}")
        render(source, svg)
        render(source, png)
        metadata["accessible_description"] = accessible_summary(description)
        metadata["hashes"] = {
            "source": sha256(source),
            "svg": sha256(svg),
            "png": sha256(png),
            "description": sha256(description),
        }
        metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        entries.append(
            {
                "id": metadata["id"],
                "source": {"path": metadata["source"], "sha256": metadata["hashes"]["source"]},
                "svg": {"path": metadata["exports"]["svg"], "sha256": metadata["hashes"]["svg"]},
                "png": {"path": metadata["exports"]["png"], "sha256": metadata["hashes"]["png"]},
                "metadata": {"path": str(metadata_path.relative_to(ROOT)), "sha256": sha256(metadata_path)},
                "description": {"path": metadata["description"], "sha256": metadata["hashes"]["description"]},
            }
        )
        print(f"rendered {metadata['id']}")

    manifest = {
        "manifest_version": "1.0.0",
        "renderer": "@mermaid-js/mermaid-cli@11.16.0",
        "configuration": {
            "path": str(CONFIG.relative_to(ROOT)),
            "sha256": sha256(CONFIG),
        },
        "visuals": sorted(entries, key=lambda entry: entry["id"]),
    }
    (VISUALS / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"updated visuals/manifest.json ({len(entries)} visuals)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
