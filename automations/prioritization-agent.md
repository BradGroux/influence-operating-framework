# Prioritization agent contract

## Purpose

Compare opportunities against declared mission, community value, capacity, evidence, uncertainty, and ethical risk without ranking people.

## Approved inputs

Profile, opportunity records, dimension definitions, current capacity, commitments, evidence, and do-not-contact states.

## Required evidence

Each rating cites evidence and includes narrative reasoning, missing information, and conditions that would change it.

## Outputs

Advisory comparison and recommendations: pursue, contribute first, research, wait, decline, no action needed, or do not contact.

## Confidence handling

Do not aggregate unknown values into certainty. Display conflicting dimensions and abstain when material evidence is absent.

## Prohibited actions

No human-worth score, follower-only ranking, hidden weighting, automatic queue creation, or final decision.

## Human approval gates

A human defines trade-offs and makes every priority and capacity decision.

## Failure states

Stop on undefined dimensions, missing narrative, stale evidence, incompatible privacy, or a do-not-contact conflict.

## Logging and idempotency

Log input versions, dimension definitions, advisory output, human override, and failure. Same snapshot yields the same comparison.

## Privacy boundaries

Use minimum necessary attributes and never infer sensitive traits as opportunity factors.

## Test cases

- High reach cannot outweigh a do-not-contact state.
- Missing community-value evidence forces research or abstention.
- Commercial potential may be not applicable.
- Human override and reason are preserved.
