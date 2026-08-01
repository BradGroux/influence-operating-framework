# Human-reviewed outreach

## Trigger and purpose

A truthful, evidence-backed reason for one external communication remains after contribution-first review.

## Inputs and evidence

Governing profile and authorized approver IDs, verified recipient ID and role, relationship and interaction context, contribution ID, current consent state, preferred channels, communication boundary, current wait and do-not-contact state, approved purpose, and supporting evidence.

## Flow

1. Check entry conditions and lower-burden alternatives.
2. Draft one concise, contextual, respectful message that is easy to decline.
3. Bind evidence, intended channel, and `sending_capability: false`.
4. Human chooses:
   - **Approve** — an approver authorized by the governing profile binds draft ID, recipient, exact content hash, channel, and expiry; the exact draft is eligible for a separate authorized handoff, but no send occurs here.
   - **Revise** — invalidate approval and return to review.
   - **Wait** — record reason and optional review date.
   - **Do not contact** — stop and preserve the durable restriction.
5. If separately authorized, hand off the exact approved payload to an external human-controlled system.
6. Log only the actual outcome and reflect.

## Stops and recovery

Stop on unsupported familiarity, stale role, ambiguity, active opt-out, a channel outside declared preferences, active person/relationship/opportunity wait, do not contact, privacy conflict, scope mismatch, expiry, wrong record type, unauthorized reviewer, or unavailable reviewer. Unknown consent requires an explicit contextual human judgment and never becomes general permission. An applicable do-not-contact restriction overrides a conflicting draft even when an optional relationship-to-contribution edge is missing. Only corrected evidence or a new documented human decision can reopen review.

## Outputs and reflection

Produce a reviewed draft and disposition, never a send. See the [outreach visual](../visuals/exports/svg/human-reviewed-outreach.svg).
