# Discovery agent contract

## Purpose

Surface bounded public research questions and candidate ecosystem records aligned with an approved profile; do not create a contact queue.

## Approved inputs

Profile ID, goals, named ecosystems, source allowlist, time and data budget, prior evidence IDs, and explicit stop condition.

## Required evidence

Every candidate includes discovery URL, publisher, access date, reason for relevance, and a fact/inference/hypothesis label.

## Outputs

Deduplicated candidate records with `research`, `wait`, `no_action_needed`, or `reject` recommendations and missing-evidence notes.

## Confidence handling

Default new candidates to low or unknown. Confidence rises only through the verification workflow.

## Prohibited actions

No private scraping, access-control bypass, purchased lists, sensitive-trait inference, ranking by reach alone, profile creation as fact, or outreach drafting.

## Human approval gates

A human approves the research question, source boundary, and any candidate entering research.

## Failure states

Stop on unavailable source, ambiguous identity, unbounded query, privacy concern, source-policy conflict, or exhausted budget.

## Logging and idempotency

Log contract version, run ID, query, approved source domains, candidate IDs, evidence IDs, disposition, and failures. The same query and source snapshot must not create duplicate IDs.

## Privacy boundaries

Use public sources only and collect the minimum fields required to decide whether further research is justified.

## Test cases

- A public event page produces a candidate with low confidence and evidence.
- A private profile page is rejected.
- A high-follower person without mission relevance receives no action.
- A repeated run reuses the existing candidate ID.
