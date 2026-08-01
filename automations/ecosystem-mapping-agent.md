# Ecosystem mapping agent contract

## Purpose

Create a bounded graph view from verified records that answers an approved ecosystem question.

## Approved inputs

Map question, profile ID, approved node and relationship IDs, privacy filter, evidence threshold, and graph-size limit.

## Required evidence

Every asserted edge cites evidence or is explicitly labeled inference or hypothesis.

## Outputs

Ecosystem record, unresolved-node queue, typed edges, gaps, excluded private fields, and a render request.

## Confidence handling

Carry claim-level confidence into edges; never infer strength from proximity, follows, employer, or event co-presence.

## Prohibited actions

No hidden expansion, universal importance score, sensitive-attribute clustering, speculative personal relationship, or automatic contact prioritization.

## Human approval gates

A human approves map scope, privacy, uncertain edges, and publication.

## Failure states

Stop on unresolved duplicate IDs, missing edge evidence, boundary overflow, private/public mixing, or graph size beyond reviewability.

## Logging and idempotency

Log map question, input IDs, exclusions, output hash, reviewer state, and failures. Same inputs and version yield the same map.

## Privacy boundaries

Apply the requested privacy view before rendering and report excluded counts without leaking content.

## Test cases

- Co-attendance does not become collaboration.
- A hypothesis edge is visibly labeled.
- Private nodes are excluded from a public view.
- Reordered inputs produce the same semantic graph.
