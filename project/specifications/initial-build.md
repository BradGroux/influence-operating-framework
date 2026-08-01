# Initial build specification

**Status:** Approved for implementation from the owner build brief
**Version target:** 0.1.0
**Date:** 2026-08-01
**Source review:** [Grill-with-docs review](../discovery/grill-with-docs-review.md)

## Problem Statement

Practitioners who want to grow meaningful influence have disconnected notes, event lists, relationship context, contribution ideas, outreach drafts, and outcome data. Common tools push this work toward follower metrics, transactional lead funnels, unsupported research, and premature outreach. They do not provide an ethical, portable operating model that a person and bounded agents can understand together while leaving external judgment with a human.

Brad Groux needs an initial profile for expanding speaking, workshop, community, media, open-source, and thought-leadership reach. The repository must serve that concrete use case without making Brad, commercial growth, public speaking, or any software platform the framework's center.

## Solution

Create an inspectable, forkable repository that defines ethical influence as a repeatable practice of discovery, evidence-based research, mapping, prioritization, contribution, human-governed engagement, follow-up, reflection, and improvement. Canonical prose defines the meaning; JSON Schemas provide portable record contracts; fictional examples demonstrate a linked graph; profiles adapt the framework to distinct missions; bounded agent contracts identify safe automation; and source-controlled visuals make important relationships easier to understand.

The default implementation never sends external communication. It supports research and drafting through an explicit human disposition of approve, revise, wait, or do not contact. An approval may be handed to a separately controlled external system, but sending remains outside this repository.

## User Stories

1. As a practitioner, I want to state my mission and boundaries so that recommendations serve my purpose rather than generic growth.
2. As a practitioner, I want to map ecosystems as linked people, organizations, events, communities, channels, projects, and evidence so that I can understand relationships rather than maintain flat lists.
3. As a practitioner, I want to connect evidence to every material claim so that I can distinguish what is known from what is assumed.
4. As a practitioner, I want facts, inferences, and hypotheses labeled separately so that uncertainty is visible.
5. As a practitioner, I want contradictory evidence retained so that the system does not silently manufacture certainty.
6. As a practitioner, I want stale information flagged so that I can verify current roles before acting.
7. As a practitioner, I want privacy classifications on records so that public and private material do not mix accidentally.
8. As a practitioner, I want stable IDs and explicit links so that I can move records between tools without losing graph relationships.
9. As a practitioner, I want relationship notes framed as continuity and mutual context so that people are never treated as prospects.
10. As a practitioner, I want no action needed, wait, and do not contact to be normal outcomes so that research never implies outreach.
11. As a practitioner, I want consent and communication preferences to take precedence so that engagement respects boundaries.
12. As a practitioner, I want to evaluate opportunities across mission, community value, learning, effort, accessibility, risk, and downstream outcomes so that revenue and reach do not dominate.
13. As a practitioner, I want every rating explained with evidence and narrative so that a number is never presented as objective truth.
14. As a practitioner, I want contribution ideas before asks so that value is created without requiring reciprocity.
15. As a practitioner, I want to prepare an event brief from verified records so that preparation is relevant and defensible.
16. As a practitioner, I want a conference playbook that includes contribution, accessibility, energy, consent, and no-action paths so that attendance is not reduced to networking volume.
17. As a practitioner, I want outreach drafts to cite their context so that messages do not invent familiarity.
18. As a human reviewer, I want to approve, revise, wait, or mark do not contact so that I retain accountable control.
19. As a human reviewer, I want approval separated from sending so that no automation silently crosses an external-action boundary.
20. As a recipient, I want outreach to be concise, contextual, respectful, and easy to decline so that the framework does not create pressure or spam.
21. As a practitioner, I want to log only interactions that actually occurred so that relationship history remains truthful.
22. As a practitioner, I want to record promises and follow-through so that continuity is based on accountability.
23. As a practitioner, I want to reflect on rejection and failure as rigorously as success so that the framework learns from reality.
24. As a practitioner, I want reflections to identify challenged assumptions and reusable artifacts so that learning compounds.
25. As a practitioner, I want contribution, relationships, learning, reach, and commercial outcomes measured separately so that no single vanity metric defines influence.
26. As a practitioner, I want qualitative measures and context beside counts so that measurement remains human-readable.
27. As Brad, I want an initial profile grounded only in supplied facts so that the repository is immediately usable without invented research.
28. As a nonprofit practitioner, I want the same framework to support a fictional community mission so that generality is demonstrated.
29. As a maintainer, I want locked and proposed decisions separated so that experimentation cannot silently amend principles.
30. As a maintainer, I want principle amendments to require transparent rationale, review, and owner approval so that the ethical center remains durable.
31. As a maintainer, I want schemas versioned and migrations documented so that machine-readable records can evolve safely.
32. As a maintainer, I want examples to be fictional and non-normative so that public artifacts are safe and do not create hidden requirements.
33. As an agent author, I want approved inputs, evidence requirements, outputs, confidence handling, prohibited actions, approval gates, failures, logs, idempotency, privacy, and tests defined so that automation stays bounded.
34. As an agent, I want one canonical documentation body so that I do not infer rules from duplicated machine-only instructions.
35. As a validator, I want one top-level command to check structure, schemas, links, graph references, privacy, outreach safety, visuals, and the index so that completion is reproducible.
36. As a reader using assistive technology, I want a text description for every major visual so that diagrams are not the only way to understand the framework.
37. As a maintainer, I want diagram sources and exports synchronized by hashes so that stale renders are detected.
38. As a new adopter, I want templates and an implementation guide so that I can start with a small evidence-backed practice.
39. As an adopter with private context, I want a documented private-overlay boundary so that I can use local tools without placing sensitive data in the public repository.
40. As a public contributor, I want governance, contribution, conduct, security, and release guidance so that participation is clear and accountable.

## Implementation Decisions

- The repository has one domain context and uses the canonical vocabulary recorded during the grill review.
- Authority flows from direct owner instruction to the charter and locked decisions, then canonical docs, then implementation contracts and illustrative artifacts.
- Canonical prose is authoritative. Schemas validate interchange records but do not independently define the framework's meaning.
- The operating lifecycle is an adaptable loop. A stage may repeat, pause, skip, or end in no action; it is not a prospect funnel and does not obligate contact.
- The data model is a graph of stable record IDs. Each record includes schema version, timestamps, status, confidence, privacy classification, evidence references, notes, and extensions where relevant.
- JSON Schema Draft 2020-12 is the portable validation dialect. Examples declare a schema and use only fictional entities, reserved domains, and synthetic facts.
- Research claims identify fact, inference, or hypothesis, preserve contradictory evidence, record access dates, and expose staleness.
- Opportunities may use optional ordinal ratings, but ratings require narrative reasoning, evidence, uncertainty, and a human decision. Aggregation is advisory and never objective truth.
- Relationship health is qualitative and evidence-backed. Frequency, audience size, or platform interaction never proves trust or intimacy.
- Do not contact is a durable restriction and takes precedence over agent recommendations. Only an accountable human can change it, with a documented reason.
- Outreach automation ends at a reviewed draft and human disposition. The repository contains no sender, credential contract, or autonomous communication path.
- Public and private records are separated operationally. Public validation covers only the public tree; private overlays are documented but ignored by version control.
- Profiles are adapters to the same framework. Brad's profile uses only owner-supplied statements, and a fictional nonprofit/community profile demonstrates generality.
- Twelve named major concepts receive Mermaid source, SVG and PNG renders, metadata, accessible descriptions, and synchronized hashes.
- Mermaid CLI is a pinned development dependency used only to render repository artifacts. Mermaid is not part of the framework semantics, and adopters do not need it to use the framework.
- The single acceptance seam is a top-level Python validation command. Focused unit tests may exercise individual checks, but completion is judged at the repository boundary.
- MIT is the initial license. Version 0.1.0 is an inspectable baseline, not a claim of independent ethics, privacy, accessibility, or domain review.

## Testing Decisions

- Good tests observe repository behavior: whether a clean checkout can validate the complete public framework, not how helper functions are internally structured.
- The primary seam is the top-level validator. It reports each gate, exits nonzero on failure, and writes the validation report with passed, failed, and deferred items.
- Schema tests validate every JSON example and resolve every record ID reference in the fictional dataset.
- Link tests resolve repository-local Markdown paths and heading anchors while ignoring external URLs.
- Structure tests assert required authoritative docs, contracts, templates, profiles, visual artifacts, and project records.
- Safety tests assert all four human dispositions, prohibit sending capabilities in agent contracts, and scan public examples for likely real contact data or transactional vocabulary.
- Visual tests assert all twelve concepts have Mermaid source, SVG, PNG, metadata, accessible descriptions, and current source/export hashes.
- Index tests rebuild the repository index deterministically and fail when the checked-in index is stale.
- Documentation quality tests detect empty placeholders and confirm lifecycle-stage guidance covers purpose, inputs, outputs, evidence, human decisions, automation, prohibited actions, quality checks, and reflection.
- The final review inspects representative SVG and PNG renders, because file existence and hash checks cannot establish readability.

## Out of Scope

- Sending messages, email, posts, comments, invitations, or follow-ups.
- Private-data scraping, platform-control bypass, contact-list purchasing, or mass cold outreach.
- A hosted application, SaaS product, CRM integration, proprietary database, or vendor-specific automation.
- A large researched directory of real people, organizations, roles, events, or contact details.
- Guarantees of influence, invitations, speaking opportunities, community recognition, or revenue.
- Independent verification of the Brad profile beyond the owner-supplied build brief.
- Final public hosting, repository publication, release signing, or a 1.0.0 maturity claim.
- Certification, legal advice, privacy compliance advice, or replacement of professional judgment.

## Further Notes

- The implementation must be truthful about deferred reviews and publication decisions.
- The public repository may teach a private-overlay pattern but must not contain private overlay data.
- Examples illustrate possible usage and may not amend canonical concepts or locked principles.
- External tools may later consume approved records, but integrations must remain modular and separately authorized.
