# Follow-up recommendation agent contract

## Purpose

Recommend whether and how to honor a real commitment or maintain appropriate continuity after an actual interaction.

## Approved inputs

Relationship and interaction IDs, explicit commitments, actual outcome, communication boundary, timing, capacity, and evidence.

## Required evidence

The interaction occurred, the commitment or reason is real, the owner is known, and current wait or do-not-contact state is checked.

## Outputs

Fulfill commitment, draft follow-up, wait, no action needed, or do not contact recommendation with rationale and optional draft-review request.

## Confidence handling

Unknown outcome or ambiguous promise lowers confidence and routes to human clarification rather than outreach.

## Prohibited actions

No cadence generation, repeated contact after silence, send, calendar mutation, invented promise, or automatic inference that follow-up is expected.

## Human approval gates

A human decides timing, channel, relevance, exact draft, and every external action.

## Failure states

Stop on missing interaction evidence, unclear owner, completed or cancelled promise, do not contact, active wait, or excessive recipient burden.

## Logging and idempotency

Log commitment ID, state, recommendation, human disposition, and failure. One commitment cannot generate duplicate open follow-up records.

## Privacy boundaries

Private interaction context stays in the private overlay and is summarized only to the minimum needed for review.

## Test cases

- An open promise recommends fulfillment before any ask.
- Silence does not create a retry schedule.
- Completed commitment produces no action needed.
- Do not contact blocks a draft.
