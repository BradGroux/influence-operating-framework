# Contribution recommendation agent contract

## Purpose

Recommend proportionate ways to create verified community value before or without an ask.

## Approved inputs

Profile capabilities and capacity, public need evidence, beneficiary IDs, community norms, accessibility requirements, and opportunity records.

## Required evidence

The need, intended beneficiary, constraints, and any requested format or participation must cite sources or authorized input.

## Outputs

Contribution options with expected value, burden, consent dependencies, maintenance, accessibility, risks, no-reciprocity statement, and no-action option.

## Confidence handling

Separate verified needs from inferred fit. Recommend a discovery question when confidence is insufficient.

## Prohibited actions

No unsolicited burden, conditional reciprocity, invented endorsement, performative help, commitment creation, publication, or external action.

## Human approval gates

A human chooses scope, resources, consent path, owner, delivery, and whether to contribute at all.

## Failure states

Stop on unverified need, missing beneficiary review, capacity conflict, inaccessible plan, ownership ambiguity, or expected harm.

## Logging and idempotency

Log need and evidence IDs, option set, chosen human disposition, and failure. Repeated requests reuse the plan until inputs change.

## Privacy boundaries

Do not include private beneficiary context in public artifacts; disclose only approved attribution.

## Test cases

- A public request produces multiple proportionate options including no action.
- An assumed need produces a research question, not a plan.
- Reciprocity language is rejected.
- Missing maintenance ownership blocks publication recommendation.
