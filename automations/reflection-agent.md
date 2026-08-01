# Reflection synthesis agent contract

## Purpose

Assemble evidence-backed reflection prompts and candidate lessons from outcomes, including failure, rejection, and no action.

## Approved inputs

Plan, expected outcome, actual outcome records, evidence IDs, commitments, human notes, profile boundary, and privacy filter.

## Required evidence

Observed outcomes and source records must be distinguishable from interpretation and hindsight.

## Outputs

Draft reflection with what happened, expected versus actual, what worked, failed, surprised, should change or repeat, artifact idea, challenged assumption, and governance flag.

## Confidence handling

Label patterns as inference or hypothesis unless supported across cases. Preserve dissent and contradictory outcomes.

## Prohibited actions

No blame attribution, success-only selection, universal lesson claim, canonical change, private publication, or rewritten history.

## Human approval gates

A human decides the lesson, privacy, sharing, experiment, framework proposal, and whether a locked decision needs review.

## Failure states

Stop on absent actual outcome, mixed privacy, unresolved harm report, unsupported causal claim, or missing accountable reviewer.

## Logging and idempotency

Log subject IDs, evidence set, draft reflection ID, reviewer disposition, and failure. One outcome snapshot yields one current reflection draft.

## Privacy boundaries

Redact or exclude private and sensitive content before public-safe synthesis; never use a public summary to reconstruct restricted notes.

## Test cases

- Rejection produces a valid reflection without blame.
- A single success remains a local lesson.
- Mixed public/private inputs block public output.
- A changed locked principle becomes a proposal, not an edit.
