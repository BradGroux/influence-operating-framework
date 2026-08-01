# Human-reviewed outreach

Outreach is a controlled drafting workflow. The framework never sends.

```text
Research complete
→ Contribution opportunity identified
→ Draft generated
→ Human review
   ├── Approve
   ├── Revise
   ├── Wait
   └── Do not contact
→ Separately authorized external-system handoff, if any
→ Log actual outcome
→ Reflect
```

See the [outreach flow](../visuals/exports/svg/human-reviewed-outreach.svg) and [accessible description](../visuals/descriptions/human-reviewed-outreach.md).

## Entry conditions

A draft may be prepared only when:

- the intended recipient and current role are verified from public or authorized evidence;
- the context for communication is truthful and relevant;
- a contribution or legitimate reason is explicit;
- consent, communication preference, wait state, and do-not-contact state have been checked;
- the practitioner has capacity to honor any implied or explicit commitment;
- no lower-burden public contribution is clearly preferable.

If a condition is missing, the output is research, revise, wait, no action, or do not contact—not a speculative draft.

## Draft requirements

A draft is contextual, concise, respectful, and easy to decline. It states a truthful reason for writing, avoids false familiarity, makes no unsupported claim, identifies any request plainly, and does not manufacture urgency. Generic flattery, engagement manipulation, emotional pressure, fake personalization, and concealed mass templating are prohibited.

## Human dispositions

- **Approve:** The named human accepts the exact draft and optional external-system handoff. Approval expires if material facts, content, recipient, channel, or timing change. Approval is not a send.
- **Revise:** The human identifies required changes; the draft returns to review and cannot inherit approval.
- **Wait:** The human records why communication is inappropriate now and may set a review date. Silence is not automatic permission to retry.
- **Do not contact:** The human records a durable prohibition. Agents and downstream tools must stop and may not weaken it. Any later change appends a named human decision with time, reason, and the exact decision it supersedes; history is never overwritten.

## External-system boundary

Any later messaging tool is a separate controlled implementation. It must authenticate the human disposition, bind it to the exact content and recipient, enforce expiry and do-not-contact, log the human-triggered action, and fail closed. This repository provides no sender, credential field, delivery API, background campaign, or retry queue.

The portable approval scope records the draft ID, recipient ID, content SHA-256, channel, and expiry. Validation recomputes the content hash, compares the current recipient and channel, rejects expiry at the record update time, and gives an active recipient do-not-contact restriction precedence over a conflicting draft. Runtime handoff systems must recheck the current time and authoritative restriction state immediately before any separately authorized human-triggered action.

## Outcome logging

Record only what actually happened: handed off, sent by an authorized human-controlled system, declined, failed, no response, or unknown. Do not infer that delivery created a relationship. Follow-up requires a new contextual judgment.
