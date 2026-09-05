#!/usr/bin/env bash

set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repository_root"

python3 scripts/test-validation.py
python3 scripts/validate-repository.py
bash scripts/validate-mermaid.sh
