# Portable record migration: schema 1.0.0 to 2.0.0

**Status:** Historical first step; followed by schema 2-to-3
**Framework release target:** v1.0.0 release candidate
**Migration type:** Breaking, human-reviewed

## Why the major version changes

Schema 2.0.0 aligns the portable record layer with canonical accountability, evidence, uncertainty, outreach, and learning requirements found incomplete during independent review. The change adds required meaning and tightens previously permissive extension and evidence behavior; a 1.x record is not upgraded safely by changing its version string.

## Field mapping

| Record | Schema 1.x | Schema 2.0.0 action |
| --- | --- | --- |
| All non-evidence records | `verified` or `high` could have no evidence | Cite at least one supporting evidence record or lower the unsupported status/confidence after human review. |
| All records | Arbitrary `extensions` object | Move only passive, non-sensitive values under a namespaced key. Remove sender, delivery, retry, campaign, webhook, credential, secret, token, password, and key material. External-effect integrations need a separate governed schema. |
| Person, organization, event | Required strings encouraged placeholders when facts were unresolved | Use the structured unknown object with `state: unknown` and a truthful reason where the 2.0.0 field permits it. Never invent a value. |
| Interaction commitment | Owner, description, and status only | Add `due_state` and `completion_evidence_ids`; add `due_at` only when supported. A completed commitment needs actual completion evidence. |
| Contribution | Core intent fields only | Add owner, scope, due-window state, accessibility-check state/evidence/notes, maintenance or handoff, risks, and stop conditions. |
| Reflection | Outcome and narrative fields only | Add observed evidence, interpretation, beneficiaries, burdens, lesson scope, artifact review targets, and authorized-reader scope. |
| Outreach draft | No channel; approval was only a state | Add the intended channel. Reset every existing approval to pending review unless a named human reviews the current payload and creates an approval scope binding exact draft ID, recipient, UTF-8 content SHA-256, channel, and expiry. |

## Deprecation window

Schema 1.x was a pre-release draft, but adopters still need an explicit transition boundary. Its deprecation window begins on the framework v1.0.0 release date and lasts 90 calendar days. During that window, maintainers will retain this migration guide, answer migration questions through the documented support path, and treat the last authoritative 1.x export as the rollback source. The 2.0.0 release-candidate validator accepted 2.0.0 records only; the current validator requires the subsequent [schema 2-to-3 migration](portable-records-2-to-3.md). After the window, 1.x artifacts remain historical evidence but receive no compatibility changes.

## Decision-history preservation

Retain the last authoritative 1.x export unchanged. Append new decisions; never truncate, reorder, replace, or silently rewrite prior restriction, relationship, opportunity, or outreach history. Verify the migrated candidate with:

```bash
python3 scripts/validate.py \
  --only schemas \
  --baseline-root /path/to/authoritative-1.x-export \
  --no-report
```

A new snapshot cannot prove by itself that a prior decision was not deleted. The authoritative baseline, its access controls, and its retention are part of the migration evidence.

## Temporal and approval checks

Schema 2.0.0 validation rejects record updates before creation, event end before start, evidence staleness before access, approval-scope mismatches, approval expiry at the record update time, and outreach that conflicts with the recipient's active do-not-contact restriction. A runtime handoff must also recheck current time and the authoritative restriction immediately before any separately authorized human-triggered external action.

## Privacy impact

Migration must not copy private contact details, consent records, sensitive notes, secrets, or credentials into public records or extensions. Structured unknown reasons describe the evidence gap without exposing private context. Apply the private-overlay access, retention, correction, deletion, incident, and recovery rules before migrating non-public data.

## Rollback

Keep the authoritative 1.x export read-only until the migrated 2.0.0 set validates and an accountable human accepts the result. Rollback means returning to that unchanged export; do not down-convert 2.0.0 records if doing so would discard do-not-contact history, approval scope, completion evidence, accessibility review, burden analysis, or other required meaning.

## Completion evidence

- schema validation passes for the migrated set;
- graph references resolve;
- authoritative-baseline history comparison passes;
- every required new field has source-backed or explicitly unknown meaning;
- approved outreach was re-reviewed rather than mechanically grandfathered;
- public-data and extension safety gates pass;
- the accountable human records migration acceptance, exceptions, and rollback readiness.
