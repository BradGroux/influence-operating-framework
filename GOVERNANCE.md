# Governance

## Stewardship

Brad Groux is the founding steward. Additional maintainers and CODEOWNERS assignments are deferred until accepted explicitly.

Stewardship preserves the charter, records material decisions, distinguishes requirements from examples, and reports review limits honestly. Teaching, applying, commercializing, or automating the framework does not independently grant authority to redefine it.

## Decision levels

- **Locked principles** require an explicit amendment proposal, evidence, impact analysis, a public review period, recorded dissent, and written approval from the founding steward or a future documented successor.
- **Accepted ADRs** record difficult-to-reverse choices with real alternatives. They may be superseded only by another accepted ADR.
- **Canonical guidance** can evolve through reviewed contributions that remain consistent with higher authority.
- **Implementation contracts and schemas** may version independently but cannot silently change canonical meaning.
- **Examples and profiles** are illustrative and never normative.

## Proposal and disagreement process

A proposal states the problem, evidence, affected communities, privacy and safety implications, alternatives, recommendation, migration impact, and unresolved dissent. Maintainers publish a disposition: accept, revise, defer, or reject. Disagreement remains in the record; it is not erased merely because a decision was made.

## Releases and compatibility

The project uses semantic versions. Schema documents have their own `schema_version`. Breaking record changes require a migration note and a major schema version. Deprecated fields remain documented for at least one compatible release unless retaining them creates a safety risk.

Release signing, cadence, and public hosting remain deferred. The [v1.0.0 release criteria](project/specifications/v1.0.0-release-criteria.md) define the accepted maturity gate. Every release must run validation and include a truthful status report; no version string or automated PASS can override an open required gate.

## Lessons into changes

Reflections may propose improvements but do not amend the framework automatically. A lesson becomes guidance only after evidence review, affected-community consideration, compatibility review, and the appropriate decision path.

## Security and privacy

Use [SECURITY.md](SECURITY.md). Sensitive disclosures never belong in public issues. Maintainers minimize retained personal data and preserve the reporter's requested confidentiality within legal and operational limits.
