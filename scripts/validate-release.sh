#!/usr/bin/env bash

set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repository_root"

release_tag="${1:-}"
if [[ $# -gt 1 ]]; then
  echo "Usage: scripts/validate-release.sh [v<version>]" >&2
  exit 2
fi

if [[ "$(git rev-parse --is-shallow-repository)" != "false" ]]; then
  echo "Release validation requires complete Git history." >&2
  echo "Run git fetch --unshallow, then rerun this command." >&2
  exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Release validation requires a clean worktree." >&2
  exit 1
fi

bash scripts/validate-repository.sh

echo "PASS: release validation uses complete Git history"
echo "PASS: release worktree is clean"

if [[ -z "$release_tag" ]]; then
  echo "Release candidate checks passed."
  exit 0
fi

version="$(tr -d '[:space:]' < VERSION)"
expected_tag="v${version}"
if [[ "$release_tag" != "$expected_tag" ]]; then
  echo "Release tag does not match VERSION: $release_tag != $expected_tag" >&2
  exit 1
fi

if [[ "$(git cat-file -t "$release_tag" 2>/dev/null || true)" != "tag" ]]; then
  echo "Release tag must be an annotated tag: $release_tag" >&2
  exit 1
fi

allowed_signers="$repository_root/.github/signing-keys/allowed-signers"
git -c gpg.ssh.allowedSignersFile="$allowed_signers" verify-tag "$release_tag"

tag_commit="$(git rev-parse "${release_tag}^{commit}")"
head_commit="$(git rev-parse HEAD^{commit})"
if [[ "$tag_commit" != "$head_commit" ]]; then
  echo "Release tag does not resolve to HEAD: $tag_commit != $head_commit" >&2
  exit 1
fi

echo "PASS: signed annotated release tag: $release_tag"
echo "PASS: release tag resolves exactly to HEAD: $head_commit"
echo "All release checks passed."
