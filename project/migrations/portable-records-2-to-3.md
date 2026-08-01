# Portable record migration: schema 2.0.0 to 3.0.0

**Status:** Required for schema 2.0.0 release-candidate records
**Framework release target:** v1.0.0-rc.2
**Migration type:** Breaking, human-reviewed

## Why the major version changes

The first post-fix review of `1.0.0-rc.1` found that schema 2.0.0 could not preserve framework-version provenance, profile capacity and cadence, or profile-bound outreach authority. It also allowed contradictory completion states. These are required-field and semantic changes, so they are schema 3.0.0 rather than a silent rewrite of 2.0.0.

## Field mapping

| Record | Schema 2.0.0 | Schema 3.0.0 action |
| --- | --- | --- |
| All records | `schema_version` only | Add the framework release that produced the record as `framework_version`; set `schema_version` to `3.0.0` only after all other migration steps pass. |
| Profile | Free-text `accountable_human`; no capacity, cadence, or approver list | Replace with stable `accountable_human_id`; add `authorized_outreach_approver_ids`, capacity, and review cadence from accountable human input or an allowed structured unknown. |
| Person | Mutable consent status without decision history | Add `consent_history`; the first decision must preserve the authoritative 2.0.0 status with source and reason, then later changes append decisions and current status matches the latest one. |
| Outreach draft | No governing profile link | Add `profile_id`. Re-review approval under that profile; the deciding person must be in its authorized approver list. |
| Contribution | Completion fields could contradict `status: completed` | A completed contribution needs completion evidence, a completed/not-applicable due state, and passed/not-required accessibility status. Lower unsupported status rather than inventing evidence. |
| Interaction commitment | Status and due state could conflict | Align open, completed, and cancelled status with the corresponding due state; preserve completion evidence. |
| Known volatile text | Placeholder strings such as `TBD` could impersonate known values | Replace placeholders with the structured unknown object and a truthful reason. |

## Decision, restriction, and reference preservation

Retain the authoritative 2.0.0 export unchanged. Preserve every existing decision history as an exact prefix, and preserve the old mutable consent status as the first schema 3 consent decision before appending any later change. Do not remove relationship edges to avoid wait or do-not-contact precedence. Schema 3 validation also enforces typed person, profile, contribution, opportunity, relationship, interaction, organizer, beneficiary, organization, ecosystem, outreach, and evidence references, using explicit unions where canonical participants may be people or organizations.

Verify the candidate against the retained snapshot:

```bash
python3 scripts/validate.py \
  --baseline-root /path/to/authoritative-2.0.0-export
```

The resulting report must show `history-baseline: PASS`, the authoritative baseline source digest, the candidate source digest, and no failed automated gate.

## Validation differences

Approval now fails closed on active opt-out, a channel outside recipient preferences, active person or relationship wait, linked opportunity wait/decline/no-action, any applicable do-not-contact, a wrong-type recipient, or an approver not authorized by the governing profile. Unknown consent remains a bounded contextual human judgment, never general permission. Completed contributions and commitments must have coherent states. Known text rejects common unknown placeholders.

## Privacy impact

The new profile fields identify stable person records and authority, not private contact details. Keep delegated-authority evidence, sensitive capacity detail, and private schedules in the governed private overlay when public disclosure is not necessary. A public profile may use a bounded public-safe capacity statement or a structured unknown with a non-sensitive reason.

## Deprecation window

Schema 2.0.0 was a release-candidate format. Its deprecation window begins on the framework v1.0.0 release date and lasts 90 calendar days. During that period, maintainers retain this mapping and accept migration questions through the documented support path. The current validator accepts 3.0.0 only and does not claim dual-version validation.

## Rollback

Keep the 2.0.0 export read-only until schema 3 validation, baseline comparison, and accountable human acceptance pass. Rollback restores that exact export and invalidates schema 3 approvals; never down-convert by discarding authority, consent, restriction, completion, capacity, cadence, or framework-version meaning.

## Completion evidence

- all records identify schema 3.0.0 and their producing framework version;
- every typed reference resolves to the expected record type;
- profile authority, capacity, and cadence are explicit;
- outreach approvals are re-reviewed under the linked profile;
- contribution and commitment completion states are coherent and evidenced;
- placeholder unknowns are replaced with structured unknowns;
- authoritative-baseline comparison and all repository gates pass;
- the accountable human records migration acceptance and rollback readiness.
