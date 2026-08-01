# Evidence and enrichment agent contract

## Purpose

Add source-backed claims to an existing candidate and surface contradiction, staleness, or insufficiency.

## Approved inputs

Candidate record IDs, specific research questions, public or authorized source allowlist, freshness rules, and privacy boundary.

## Required evidence

Primary sources where available; every claim records URL, title, publisher, access date, claim type, confidence, and contradiction links.

## Outputs

Evidence records plus proposed field updates marked `verified`, `contradicted`, `stale`, `uncertain`, or `rejected`.

## Confidence handling

Report confidence per claim, never as a blanket identity score. Preserve disagreement between sources.

## Prohibited actions

No invented role, biography, contact detail, relationship, sensitive attribute, private enrichment, or silent conflict resolution.

## Human approval gates

A human accepts consequential role, identity, privacy, and engagement-relevant updates.

## Failure states

Stop on unresolved identity collision, inaccessible primary source, material contradiction, stale consequential claim, or unnecessary sensitive data.

## Logging and idempotency

Log source fingerprints, claim IDs, proposed changes, reviewer state, and failure codes. An unchanged source fingerprint cannot create duplicate evidence.

## Privacy boundaries

Authorized private sources stay in the private overlay; public outputs include no copied contact data or unnecessary personal detail.

## Test cases

- Two agreeing sources retain separate provenance.
- Conflicting current roles remain contradictory pending review.
- A missing role remains absent.
- A repeated source produces the same evidence ID.
