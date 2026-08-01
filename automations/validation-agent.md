# Validation agent contract

## Purpose

Run the repository acceptance gates and produce a truthful report of passed, failed, and deferred checks.

## Approved inputs

Repository working tree, validation policy, schema registry, required structure, visual manifest, and declared deferrals.

## Required evidence

Command output, file hashes, schema errors, link targets, graph-reference results, safety checks, index comparison, and explicit review records.

## Outputs

Machine exit code, concise console summary, and validation report listing every gate and deferral.

## Confidence handling

A check is passed only from direct evidence. Unavailable dependencies or skipped review become failed or deferred according to policy, never passed.

## Prohibited actions

No auto-correction of semantic content, deletion, suppressed failure, fabricated review, remote publication, or conversion of deferral to success.

## Human approval gates

A human reviews failures, representative visual renders, privacy-sensitive changes, and release deferrals before release claims.

## Failure states

Dependency missing, invalid schema or example, unresolved ID, broken link, absent artifact, stale hash or index, private-data pattern, unsafe automation language, or internal validator error.

## Logging and idempotency

Log policy version, repository state, gate details, report hash, and exit code. An unchanged tree yields the same gate outcomes apart from declared run time.

## Privacy boundaries

Report paths and safe summaries, not matched private values. Scan only public artifacts by default.

## Test cases

- A bad example fails schema validation.
- A broken relative link fails.
- A missing PNG or stale hash fails.
- A declared independent review remains deferred.
