# Initial code review disposition

**Review date:** 2026-08-01
**Baseline:** 0.1.0 initial repository build
**Axes:** specification and acceptance; maintainability and repository standards

## Outcome

No blocking finding remains after disposition. The review identified safety, durability, test-depth, visual-semantics, metadata, template, and status gaps. Each material finding was fixed and covered by the repository validation seam.

## Findings resolved

| Finding | Disposition | Evidence |
| --- | --- | --- |
| Do-not-contact and other human decisions were mutable snapshots without accountable history. | Fixed. Shared human decisions now require an actor, timestamp, reason, stable decision ID, and an exact supersession chain. Person restrictions, relationship dispositions, opportunity decisions, and outreach reviews use append-only histories. | `schemas/common.schema.json`, domain schemas, schema tests, fictional records |
| Safety checks proved expected words existed but did not reject meaningful negative cases. | Fixed. Tests now reject invalid do-not-contact reopening, empty review reasons, sender capabilities, invented familiarity without evidence, and transactional person labels. | `tests/test_schemas.py`, `tests/test_structure.py`, `scripts/validate.py` |
| The lifecycle visual made a durable do-not-contact decision appear restartable. | Fixed. Temporary wait/no-action and durable human stop are separate terminal semantics; only the safe pause can re-enter discovery after changed evidence or capacity. | `visuals/source/influence-lifecycle.mmd` and synchronized exports |
| Visual metadata did not carry accessible prose or per-artifact hashes. | Fixed. Rendering injects an accessible summary and source, SVG, PNG, and description hashes into every metadata record; validation cross-checks them with the manifest. | `scripts/render_visuals.py`, `scripts/validate.py`, `visuals/metadata/`, `visuals/manifest.json` |
| The research workflow lacked a reusable research-note template. | Fixed. | `templates/research-note.md` |
| Required-structure coverage omitted implementation records and the fictional practitioner profile. | Fixed. | `scripts/validate.py`, structure acceptance tests |
| Partial validation could overwrite the full validation report, and completion status was stale. | Fixed. Only a complete run writes the deterministic report, which is read back; the status and ticket record are closed with explicit deferrals. | `scripts/validate.py`, `tests/test_structure.py`, `project/planning/status.md` |

## Judgment retained

One reviewer flagged the size of `scripts/validate.py` as a possible divergent-change risk. No split was made for 0.1.0: the build prompt explicitly asks for one validation seam, there is only one implementation, and speculative modules would add navigation without reducing current duplication. The file keeps named gate functions behind one command. Revisit extraction if a second validator consumer or repeated implementation emerges.

## Release boundary

This disposition supports the local 0.1.0 baseline only. It is not an independent ethics, privacy, accessibility, legal, or domain review, and it does not authorize public publication or external integrations.
