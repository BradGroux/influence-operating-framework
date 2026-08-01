# Visualization renderer contract

## Purpose

Render approved Mermaid sources into synchronized SVG and PNG artifacts with metadata and accessible descriptions.

## Approved inputs

Approved `.mmd` sources, visual configuration, metadata, descriptions, manifest, and renderer version.

## Required evidence

Source concept links to canonical prose; metadata names the source, exports, description, and version.

## Outputs

Deterministic SVG and PNG exports plus refreshed SHA-256 manifest entries and a render summary.

## Confidence handling

Rendering is deterministic; semantic confidence is not inferred. Ambiguous or contradictory diagrams require human review.

## Prohibited actions

No semantic rewrite, remote content inclusion, hidden network dependency at render time, publication, or replacement of accessible prose.

## Human approval gates

A human approves source meaning and visually inspects representative exports for readability and accessibility.

## Failure states

Stop on Mermaid parse error, missing description, missing metadata, export failure, non-deterministic path, or hash mismatch.

## Logging and idempotency

Log renderer version, source and export hashes, duration, and failures. Unchanged sources and configuration must produce current manifest state without duplicate artifacts.

## Privacy boundaries

Only public-safe labels and metadata enter public visuals. Do not render private graph content into public exports.

## Test cases

- Valid source creates SVG, PNG, and current hashes.
- Missing description fails.
- A source edit makes validation fail until rerendered.
- A visually misleading semantic change requires human review even if rendering succeeds.
