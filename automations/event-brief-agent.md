# Event briefing agent contract

## Purpose

Assemble a verified event brief focused on contribution, learning, accessibility, relationships, and stop conditions.

## Approved inputs

Event ID, profile ID, ecosystem IDs, approved evidence, existing relationship IDs, capacity and travel boundaries.

## Required evidence

Current organizer source for dates, format, location summary, accessibility, deadlines, participation rules, and public roles used in the brief.

## Outputs

An event brief with verified logistics, fit narrative, contribution options, known versus merely public participants, questions, risks, and human decisions.

## Confidence handling

Mark each volatile detail with freshness and confidence. Stale logistics block travel or submission recommendations.

## Prohibited actions

No registration, travel purchase, proposal submission, calendar change, contact, or inference that co-attendance creates a relationship.

## Human approval gates

A human decides attend, submit, contribute, wait, decline, no action, and every outreach disposition.

## Failure states

Stop on conflicting dates, missing primary logistics, inaccessible requirements, capacity conflict, safety concern, or privacy ambiguity.

## Logging and idempotency

Log event and evidence IDs, freshness checks, output version, human decisions, and failures. Same evidence snapshot updates the existing brief.

## Privacy boundaries

Include only public event data and authorized relationship context; never export private notes into a public brief.

## Test cases

- Conflicting dates block a travel recommendation.
- A public speaker list does not create person relationships.
- Missing accessibility information becomes an open question.
- Rerun updates one brief rather than duplicating it.
