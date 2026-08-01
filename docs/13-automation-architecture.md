# Automation architecture

Automation assists bounded work; it does not own the practitioner's mission, evidence interpretation, relationships, or external actions.

See the [automation architecture visual](../visuals/exports/svg/automation-architecture.svg) and [description](../visuals/descriptions/automation-architecture.md).

## Layers

1. **Authoritative guidance:** Charter, locked decisions, canonical docs, and profile boundaries.
2. **Approved inputs:** Public or authorized records with provenance, privacy, confidence, and schema versions.
3. **Bounded agents:** Discovery, evidence, event briefing, mapping, prioritization, contribution, drafting, follow-up, reflection, visualization, and validation contracts.
4. **Review queues:** Human decisions, corrections, exceptions, wait, no action, do not contact, and escalation.
5. **Inspectable outputs:** Draft records, reports, visual exports, logs, and reflections.
6. **Optional external systems:** Separately authorized tools outside the default implementation.

## Agent action contract

Every agent contract defines purpose, approved inputs, required evidence, outputs, confidence handling, prohibited actions, human gates, failure states, logging, idempotency, privacy, and tests. If required evidence or authority is missing, the agent returns a bounded failure or review request rather than guessing.

## External-action boundary

No default agent has a send tool, recipient credential, campaign scheduler, or permission to act publicly. The outreach drafting agent ends at a draft. Human review creates a disposition. A later external system may accept an exact approved payload only under its own authentication, authorization, expiry, audit, and fail-closed controls.

## Logging

Logs record contract version, run ID, time, approved input IDs, output IDs, confidence, human gate, failure code, and privacy-safe summary. Logs do not copy unnecessary private content or secrets. A retry with the same idempotency key must not create duplicate records or external actions.

## Failure and recovery

Agents stop on missing evidence, schema mismatch, unresolved identity, stale consequential claims, privacy ambiguity, contradictory do-not-contact state, instruction conflict, or unavailable human review. Recovery requires correcting the source condition and starting a traceable new attempt; silence or timeout never grants authority.
