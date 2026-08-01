# Portable record schemas

Canonical documents define framework meaning. These JSON Schema Draft 2020-12 contracts validate portable records and never supersede the [charter](../docs/00-charter.md), [locked decisions](../decisions/locked-decisions.md), or canonical guidance.

## Conventions

- Stable IDs are lowercase, dash-separated, and type-prefixed.
- Every record declares its schema URI, record type, schema version, timestamps, status, confidence, privacy, evidence references, human notes, extensions, and fictional marker.
- Relationships use stable IDs rather than embedding duplicate records.
- Human restrictions and dispositions use append-only decision histories. Each decision records a stable decision ID, accountable person ID, time, reason, and the exact prior decision it supersedes.
- Public examples set `fictional` to `true` and use reserved domains when URLs are needed.
- Missing or uncertain facts remain absent or receive `unknown` confidence; they are never fabricated.
- `extensions` permits tool-specific data while canonical fields remain portable.

## Versioning and migration

Schema versions use semantic versioning. Additive optional fields are minor changes. Changed meaning, required fields, removed enum values, or incompatible ID rules are major changes. A breaking release must document old-to-new field mapping, default behavior, privacy impact, validation differences, rollback, and a deprecation window.

Migrations must preserve original evidence, timestamps, uncertainty, contradictions, complete human decision histories, and do-not-contact restrictions. A migration may not synthesize a missing value merely to satisfy a new required field; it must stop for review or use an explicitly allowed unknown state.
