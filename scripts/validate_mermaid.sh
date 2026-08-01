#!/usr/bin/env bash

set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validation_temp="$(mktemp -d "${TMPDIR:-/tmp}/influence-framework-mermaid.XXXXXX")"

cleanup() {
  find "$validation_temp" -depth -delete
}
trap cleanup EXIT

if [[ $# -ne 0 ]]; then
  echo "Usage: scripts/validate_mermaid.sh" >&2
  exit 2
fi

for required_command in find npx rg; do
  if ! command -v "$required_command" >/dev/null 2>&1; then
    echo "Required Mermaid validation command is unavailable: $required_command" >&2
    exit 1
  fi
done

cd "$repository_root"

document_count=0
diagram_count=0

while IFS= read -r markdown_file; do
  document_count=$((document_count + 1))
  expected="$(rg --count '^```mermaid$' "$markdown_file")"
  document_key="$(printf '%s' "$markdown_file" | tr '/.' '__')"
  document_temp="$validation_temp/$document_key"
  assets_temp="$document_temp/assets"

  mkdir -p "$assets_temp"
  npx --yes @mermaid-js/mermaid-cli@11.16.0 \
    --input "$markdown_file" \
    --output "$document_temp/rendered.md" \
    --artefacts "$assets_temp" \
    --quiet

  rendered="$(find "$assets_temp" -type f -name '*.svg' | wc -l | tr -d ' ')"
  if [[ "$rendered" != "$expected" ]]; then
    echo "Mermaid render mismatch in $markdown_file: expected $expected, rendered $rendered" >&2
    exit 1
  fi
  diagram_count=$((diagram_count + rendered))
done < <(rg --files -g '*.md' | while IFS= read -r file; do
  if rg --quiet '^```mermaid$' "$file"; then
    printf '%s\n' "$file"
  fi
done)

if [[ "$document_count" -eq 0 ]]; then
  echo "No Mermaid diagrams found" >&2
  exit 1
fi

echo "PASS: Mermaid rendering: $diagram_count diagrams in $document_count documents"
