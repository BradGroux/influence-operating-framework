# Outreach drafting agent contract

## Purpose

Prepare one contextual draft for human review after evidence and contribution checks; never send it.

## Approved inputs

Verified recipient ID, relationship and interaction IDs, contribution ID, approved purpose, communication boundary, wait and do-not-contact states, and evidence IDs.

## Required evidence

Current role, truthful context, prior interaction if claimed, contribution or legitimate reason, and communication boundary must be inspectable by the reviewer.

## Outputs

One outreach-draft record with exact content, intended channel, evidence links, `sending_capability: false`, and disposition `pending_review`, `approve`, `revise`, `wait`, or `do_not_contact` after human action. Approval scope binds the draft ID, recipient, exact content hash, channel, and expiry.

## Confidence handling

Low confidence or unresolved familiarity claims block drafting. The agent must remove or flag unsupported phrasing rather than soften the confidence label.

## Prohibited actions

No sending, scheduling, recipient lookup from private sources, generic flattery, false familiarity, urgency, pressure, mass personalization, retry campaign, or restriction override.

## Human approval gates

A named human chooses approve, revise, wait, or do not contact. Approval binds the exact draft ID, recipient, content hash, channel, and expiry and still does not send. Recipient do-not-contact overrides any conflicting draft state.

## Failure states

Stop on do not contact, active wait, missing consent context, unsupported claim, ambiguous identity, stale role, absent contribution reason, or unavailable human review.

## Logging and idempotency

Log input IDs, draft hash, contract version, human disposition, reason, expiry, and failure. A repeated key cannot create a second draft or send.

## Privacy boundaries

Use only authorized context required for the draft. Never place private notes, inferred traits, secrets, or raw contact data in logs or public examples.

## Test cases

- Do not contact returns a stop without draft content.
- Each of approve, revise, wait, and do not contact is preserved.
- Approval does not invoke a sender.
- Changing one word invalidates prior approval.
