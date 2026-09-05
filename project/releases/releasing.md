# Release runbook

This procedure maintains this documentation repository. It is not a required
implementation of the framework. Use Bash, Git, Python 3, Node/npm with npx,
a usable Chromium browser, authenticated gh and Gitleaks for publication work.
The gate uses Mermaid CLI 11.16.0 transiently through npx; its transitive tree
is unlocked. Review renderer advisories before release and report that limit.
CI pins action commits, runs with read-only permissions and a bounded timeout.
Its disposable Linux renderer disables the browser process sandbox; never use
that setting to browse sensitive or unrelated content.

## Prepare and review

1. Read Governance and the exact adopted Commons revision. Resolve substantive
   content findings first; record source evidence, adverse cases, compatibility,
   dissent and missing field evidence. Do not substitute link checks for this work.
2. Use the actual UTC publication date for VERSION. Further same-day editions
   use .1, .2 in numeric order. If the day changes before publication, update
   metadata and review the resulting candidate before tagging.
3. Update current README status, charter status, Governance edition, changelog,
   quoted CFF product version/date, and the edition release record. Preserve
   all historical records, tags and bodies. CFF format version stays 1.2.0.
4. Stage only intended files; run the commands below. Inspect changed diagrams
   when their meaning or layout changes. No diagram change needs to be invented.
5. Obtain independent content/application/adversarial and repository standards
   review of the exact candidate; resolve findings and retain its commit through
   a merge commit. Merge only after required PR checks pass, then verify the
   clean merged tree matches the reviewed tree and main's checks pass.

```bash
git status --short
git diff --check
bash -n scripts/validate-repository.sh scripts/validate-release.sh scripts/validate-mermaid.sh
bash scripts/validate-repository.sh
gitleaks git . --no-banner --redact --log-level error
```

The regression suite covers calendar dates, correction suffixes, stale/duplicate
citation metadata, active status fields, and candidate-only history. CI also
checks depth-1 contributor success with explicit partial-history reporting and
depth-1 release rejection. Release validation requires a clean tree and complete
history; use `git fetch --unshallow` when necessary. Gitleaks errors are not a
clean scan. Review dependencies separately; a secret scan is not a dependency audit.

## Publish the clean merged target

Confirm the normal signing configuration uses the authorized release identity.
Never print, rotate or export private signing material. If signing is unavailable,
stop at a reviewable candidate. No unsigned fallback is permitted.

Before writes, verify the account, main protection, tag update/deletion ruleset
and future release immutability through gh. Tag protection must have no bypass
actors; main must require Documentation and publication safety. Preserve these
protections, and never bypass an executed failed check.

The following sequence uses no force operation. Run it from clean merged main
only after the content, PR and merged-main checks above pass:

```bash
gh auth status --hostname github.com
test "$(gh api --hostname github.com user --jq .login)" = BradGroux
git fetch origin --tags
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
bash scripts/validate-release.sh
edition="$(cat VERSION)"
release_tag="v$edition"
release_date="$(date -u +%Y-%m-%d)"
test "${edition:0:10}" = "$(date -u +%Y.%m.%d)"
notes="project/releases/$release_tag-release-$release_date.md"
test -f "$notes"
git tag -s "$release_tag" -m "Influence Operating Framework $release_tag"
bash scripts/validate-release.sh "$release_tag"
git push origin "refs/tags/$release_tag"
```

Wait for the tag workflow to pass, then publish the prepared immutable release:

```bash
gh release create "$release_tag" --repo BradGroux/influence-operating-framework --verify-tag --title "Influence Operating Framework $release_tag" --notes-file "$notes"
python3 scripts/verify-public-release.py "$release_tag"
```

No assets are required. The read-only verifier checks the exact repository,
local/remote annotated object and peeled commit, tracked-key signature, GitHub
signature status, release author, final immutable state, UTC date, title, body
and empty asset list. It normalizes only CRLF and trailing newlines in the body.
A publication-day mismatch is a failure, not permission to move the tag.

## Historical assurance and recovery

Preserve v1.0.0, v1.0.1 and v1.0.2 exactly, including their original date metadata
and republish records. Their effective dates are not retroactively converted
to UTC publication dates. To check v1.0.2, use a separate clean checkout at that
tag and run its own `bash scripts/validate-release.sh v1.0.2`; compare the
remote tag object and peeled commit separately. The new public verifier is for
calendar editions only. v1.0.0/v1.0.1 predate signed-release enforcement and
cannot truthfully pass the new signature requirement. Their existing historical
review checks remain available at their original revisions.

Snapshot existing remote tag objects and release bodies before publishing and
compare them afterwards. Never move a tag, delete/recreate a release, or add a
dated alias. Correct a published error in a new edition with explicit scope.
If a command fails after creating a tag, inspect local and remote identity and
publication state before retrying. Reuse only the exact reviewed tag; if the
UTC date has passed, prepare a new dated candidate and preserve the old tag.
