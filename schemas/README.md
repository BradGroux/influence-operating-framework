# Portable record schemas

Canonical documents define framework meaning. These JSON Schema Draft 2020-12 contracts validate portable records and never supersede the [charter](../docs/00-charter.md), [locked decisions](../decisions/locked-decisions.md), or canonical guidance.

## Conventions

- Stable IDs are lowercase, dash-separated, and type-prefixed.
- Every record declares its schema URI, record type, schema version, timestamps, status, confidence, privacy, evidence references, human notes, extensions, and fictional marker.
- Relationships use stable IDs rather than embedding duplicate records.
- Human restrictions and dispositions use append-only decision histories. Each decision records a stable decision ID, accountable person ID, time, reason, and the exact prior decision it supersedes.
- A current snapshot proves only its internal decision chain. Cross-revision append-only verification compares the candidate with the last authoritative snapshot by running `python3 scripts/validate.py --only schemas --baseline-root <authoritative-root> --no-report`.
- Public examples set `fictional` to `true` and use reserved domains when URLs are needed.
- Required but unresolved identity, summary, schedule, location, format, or accessibility values use the structured `{ "state": "unknown", "reason": "..." }` form; fabricated placeholders are invalid practice.
- Non-evidence records marked `verified` or `high` confidence cite at least one evidence record. Evidence links still require human claim-level adequacy review; an existing ID is not proof that the source supports every claim.
- `extensions` uses namespaced keys and passive values. Sender, delivery, retry, campaign, webhook, credential, secret, token, password, or key fields are prohibited recursively. Extensions with external effects require a separately governed schema and never travel inside a portable framework record.
- An approved outreach decision binds the draft ID, recipient, exact UTF-8 content SHA-256, channel, and expiry. A content, recipient, channel, or timing change requires a new review; approval is never a send.

## Versioning and migration

Schema versions use semantic versioning. Additive optional fields are minor changes. Changed meaning, required fields, removed enum values, or incompatible ID rules are major changes. A breaking release must document old-to-new field mapping, default behavior, privacy impact, validation differences, rollback, and a deprecation window.

The current portable record version is **2.0.0**. Records from the initial 1.0.0 draft require the [schema 1-to-2 migration](../project/migrations/portable-records-1-to-2.md); changing only the version string is prohibited.

Migrations must preserve original evidence, timestamps, uncertainty, contradictions, complete human decision histories, and do-not-contact restrictions. A migration may not synthesize a missing value merely to satisfy a new required field; it must stop for review or use an explicitly allowed unknown state. Verify append-only histories against the last authoritative export rather than trusting the new snapshot to attest to its own completeness.
