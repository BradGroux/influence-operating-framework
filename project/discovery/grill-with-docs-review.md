# Grill-with-docs review

**Status:** Complete
**Date:** 2026-08-01
**Owner:** Brad Groux
**Scope:** `owner build brief`, the owner build prompt, and structural comparison with the AI-Native Operating Framework

## Authority used

1. Direct current owner instruction and the build prompt.
2. The supplied `owner build brief` build brief.
3. Locked principles and decisions recorded by this repository.
4. Canonical framework documents.
5. Schemas, automation contracts, templates, workflows, profiles, and examples.
6. Project records and validation reports.

Lower-authority artifacts may implement or illustrate the framework but may not silently redefine it.

## Confirmed requirements

- Build a reusable, open-source operating framework for ethical influence through contribution, relationships, reflection, and continuous improvement.
- Preserve all twelve locked principles verbatim and treat amendments as owner-governed changes.
- Keep the framework broader than public speaking and explicitly prevent it from becoming a sales CRM, lead funnel, or engagement-farming system.
- Use one canonical body of clear documentation for human and agent readers, with machine-readable JSON Schema records linked by stable IDs.
- Cover ecosystem, person, organization, event, relationship, interaction, opportunity, contribution, outreach, reflection, evidence, and practitioner-profile concepts.
- Distinguish fact, inference, and hypothesis; retain provenance, access dates, confidence, staleness, and contradictory evidence.
- Make external communication impossible by default. Agents may research, recommend, and draft, but a human must choose approve, revise, wait, or do not contact. Approval is not itself a send.
- Keep public examples fictional and free of real private contact data. Keep sensitive overlays outside the public repository.
- Include the Brad Groux profile using only supplied context, plus a second fictional profile demonstrating reuse beyond a commercial mission.
- Supply substantive operating documents, templates, bounded agent contracts, workflows, schemas, fictional examples, twelve minimum visualizations, render automation, tests, an index, and a truthful validation report.

## Structural conventions reused

The AI-Native Operating Framework provides applicable discipline without donating its domain content:

- an explicit authority hierarchy;
- charter and accepted decisions above examples and project history;
- canonical prose as the source of meaning for people and machines;
- accepted versus proposed decisions with evidence and dissent preserved;
- examples that illustrate rather than create requirements;
- accountable human ownership and explicit approval, exception, stop, and recovery conditions;
- vendor independence and clear separation between framework meaning and technical implementation;
- source-controlled evidence, status, handoffs, review limits, and validation gates;
- repository-portable relative links and inspectable release records.

The source framework's prohibition on a universal business lifecycle and core schemas is domain-specific, not controlling here. The Influence Operating Framework handoff explicitly requires a reusable influence lifecycle and portable schemas. To preserve the useful underlying convention, the lifecycle is an adaptable practice loop rather than a funnel, and prose remains authoritative over schemas.

## Conservative assumptions and proposed resolutions

| Gap | Resolution for the initial release | Reason |
| --- | --- | --- |
| Open-source license not named | Use MIT, matching the inspected source framework. | Permissive, forkable, and easy to replace before publication. |
| Schema dialect not named | Use JSON Schema Draft 2020-12 with repository-relative identifiers and semantic schema versions. | Current portable standard with explicit versioning. |
| Lifecycle rigidity | Permit stages to pause, repeat, skip, or end in no action. Never infer contact from research or prioritization. | Prevents a funnel interpretation and respects human judgment. |
| Meaning versus implementation | Canonical docs define semantics; schemas validate record interchange; templates and examples are illustrative. | Keeps the framework tool-agnostic while meeting machine-readable requirements. |
| Privacy overlays | Document a local/private overlay contract, but do not include or validate private records in the public tree. | Avoids accidental publication and platform lock-in. |
| Brad profile evidence | Use only facts explicitly supplied in the handoff and label the profile as owner-supplied, not independently researched. | Prevents fabrication and keeps initial scope bounded. |
| Diagram set | Treat the twelve visualizations enumerated in the handoff as the initial definition of “major concepts.” | Creates a testable acceptance boundary. |
| Diagram implementation | Use source-controlled Mermaid, deterministic SVG/PNG exports, accessible descriptions, and a hash manifest. | The required visuals are primarily flows and conceptual relationships; Mermaid source is easy to review in Markdown and keeps the framework semantics independent of the renderer. |
| Opportunity scoring | Use optional explainable dimension ratings plus mandatory narrative, evidence, uncertainty, and human decision fields. | Numbers must not masquerade as objective truth. |
| Relationship health | Use qualitative, evidence-backed states; do not infer intimacy from frequency, reach, or platform activity. | Avoids manipulative or fabricated relationship claims. |
| Outreach approval | Record approval as permission for a separately controlled system to send; this repository never performs the send. | Keeps the external-action boundary explicit. |
| Initial release | Use version `0.1.0` and mark unfinished owner, domain, and publication reviews as deferred rather than passed. | Truthful baseline for a new repository. |

## Unresolved questions

No unresolved question blocks the initial architecture, ethics model, public data model, or external-action safety boundary.

The following owner choices are intentionally deferred because the initial implementation can preserve them without guessing:

- final public hosting location and repository slug;
- additional maintainers and CODEOWNERS assignments;
- security and private-reporting contact channel;
- release signing and long-term release cadence;
- which private storage or workflow tools, if any, Digital Meld will connect later;
- independent ethics, privacy, accessibility, and domain review before a `1.0.0` claim.

## Implementation risks and controls

| Risk | Required control |
| --- | --- |
| The framework drifts into a CRM or funnel. | Vocabulary checks, prohibited terms in canonical records, contribution-first workflows, and valid no-action outcomes. |
| Research claims become stale or fabricated. | Evidence references, access dates, confidence, claim type, contradiction support, and validation of required provenance fields. |
| Approval is mistaken for autonomous sending. | Agent outputs stop at a human disposition and an explicit external-system handoff; no sender implementation or credentials. |
| Public examples expose personal data. | Fictional markers, reserved example domains, privacy classification, and content scans for contact-like data. |
| Scores overstate objectivity. | Mandatory narrative and evidence beside any optional rating; human override and abstention supported. |
| Schemas silently become the framework. | Documentation authority statement, schema-to-doc links, and governance review for semantic changes. |
| Brad's profile makes the core person-specific. | Profiles remain adapters; canonical concepts and fictional examples demonstrate noncommercial use. |
| Visuals drift from sources or become decorative. | Named visual grammar, accessible descriptions, generated hashes, render checks, and direct links from relevant docs. |
| “Public by default” overrides consent or safety. | Privacy classification, minimum-necessary collection, do-not-contact precedence, and private-overlay guidance. |

## Acceptance criteria

The initial build is acceptable only when:

1. This review, canonical vocabulary, locked decisions, assumptions, and deferred decisions are source-controlled.
2. Required documents contain operational guidance rather than headings or placeholders.
3. Every JSON example declares its schema and passes Draft 2020-12 validation.
4. All stable record links resolve in the example dataset and all repository-local Markdown links resolve.
5. The required structure exists and the repository index is current.
6. Each of the twelve required visual concepts has source, SVG, PNG, metadata, accessible description, and synchronized hashes.
7. Every outreach-related workflow and agent contract exposes approve, revise, wait, and do-not-contact, and no default path sends.
8. Public fictional examples contain no real private contact data and the Brad profile contains only the owner-supplied facts named above.
9. A Brad profile and a noncommercial fictional profile both map to the same core model.
10. The validation report lists every check as passed, failed, or deferred and does not call deferred owner or independent review complete.

## Grill conclusion

The supplied handoff resolves the decisions that could materially change architecture, ethics, the public data model, or external-action safety. The owner explicitly authorized conservative resolution of non-blocking gaps in the build prompt. Shared understanding for implementation is therefore represented by the locked source requirements plus the assumptions above; no additional owner interruption is required before the initial build.
