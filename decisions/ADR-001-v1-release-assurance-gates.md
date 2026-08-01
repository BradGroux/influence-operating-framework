# ADR-001 — v1 release assurance gates

- **Status:** accepted
- **Date:** 2026-08-01
- **Owner:** Brad Groux

## Question

What evidence and accountable review must exist before this repository may claim a final v1.0.0 release?

## Context and evidence

Version 1.0.0 is a maturity claim for a framework that governs research, relationship context, contribution, outreach drafting, privacy, and human decisions. Automated repository checks can prove structural properties, but they cannot supply accountable ethics, privacy, accessibility, legal, domain, operational, or owner judgment. The initial two-agent review also showed that a single implementation-and-review pass can miss material safety gaps.

## Alternatives considered

1. Treat passing repository automation as sufficient for v1.0.0. This is fast but overstates what machine checks establish.
2. Require only owner approval. This preserves authority but concentrates review and leaves specialist risks underexamined.
3. Require repository gates, two independent AI review roles on one exact commit, qualified human discipline reviews, operational reporting readiness, and explicit owner approval. This creates more work but keeps each evidence type within its competence.

## Recommendation

Use the layered gate in option 3. Permit clearly labeled release-candidate commits so review can target immutable content, but prohibit the final version, tag, or publication claim until every required gate closes.

## Decision

The owner accepts the [v1.0.0 release criteria](../project/specifications/v1.0.0-release-criteria.md) as the governing release gate. Both independent AI reports must cover the same exact candidate commit and have no unresolved Blocker or Material finding. Qualified human review, a tested private reporting route, an authorized publication target, and final owner approval remain separate requirements.

## Consequences, dissent, and migration

The repository may remain at a release candidate after its technical checks pass. This delays the final tag but prevents technical evidence from impersonating ethical, legal, accessibility, domain, operational, or owner approval. If reviewer disciplines or evidence requirements change, amend this ADR and the release criteria together; do not silently weaken one document.
