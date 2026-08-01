# Human-reviewed outreach

## Trigger and purpose

A truthful, evidence-backed reason for one external communication remains after contribution-first review.

## Inputs and evidence

Verified recipient ID and role, relationship and interaction context, contribution ID, communication boundary, current wait and do-not-contact state, approved purpose, and supporting evidence.

## Flow

1. Check entry conditions and lower-burden alternatives.
2. Draft one concise, contextual, respectful message that is easy to decline.
3. Bind evidence, intended channel, and `sending_capability: false`.
4. Human chooses:
   - **Approve** — bind draft ID, recipient, exact content hash, channel, and expiry; the exact draft is eligible for a separate authorized handoff, but no send occurs here.
   - **Revise** — invalidate approval and return to review.
   - **Wait** — record reason and optional review date.
   - **Do not contact** — stop and preserve the durable restriction.
5. If separately authorized, hand off the exact approved payload to an external human-controlled system.
6. Log only the actual outcome and reflect.

## Stops and recovery

Stop on unsupported familiarity, stale role, ambiguity, missing consent context, active wait, do not contact, privacy conflict, scope mismatch, expiry, or unavailable reviewer. An active recipient do-not-contact restriction overrides a conflicting draft. Only corrected evidence or a new documented human decision can reopen review.

## Outputs and reflection

Produce a reviewed draft and disposition, never a send. See the [outreach visual](../visuals/exports/svg/human-reviewed-outreach.svg).
