# Repository instructions

## Purpose

This repository contains the Influence Operating Framework: an open, tool-agnostic operating model for ethical influence through contribution, relationships, reflection, and continuous improvement.

## Authority

Apply this order:

1. Direct current owner instruction.
2. `docs/00-charter.md`.
3. `decisions/locked-decisions.md` and accepted ADRs.
4. Canonical documents under `docs/` and the vocabulary in `CONTEXT.md`.
5. Governance and contribution guidance.
6. Schemas and automation contracts.
7. Templates, profiles, workflows, and examples.
8. Project records and history.

Lower-authority material may implement or illustrate the framework but must not silently redefine higher-authority material.

## Content boundaries

- Treat people as people, never leads, prospects, targets, or conversions.
- Keep contribution and community value ahead of reach, growth, and monetization.
- Preserve human judgment for every external engagement decision.
- Never add an autonomous sender, mass-outreach path, fabricated relationship, or unsupported research claim.
- Make `wait`, `do not contact`, and `no action needed` normal outcomes.
- Keep public examples fictional and free of real personal contact data.
- Keep the canonical framework independent of vendors, models, databases, and automation platforms.
- Use schemas to validate portable records, not to redefine canonical prose.
- Keep private overlays outside the public repository.

## Documentation

- Use the canonical vocabulary in `CONTEXT.md`.
- Use clear Markdown, relative links, and kebab-case filenames.
- State status, ownership, provenance, confidence, privacy, and review limits honestly.
- Examples illustrate and never create requirements.
- Add a diagram only when sequence, hierarchy, or relationships are materially clearer visually.
- Every required visual needs Mermaid source, SVG, PNG, metadata, an accessible description, and a synchronized manifest entry.

## Verification

Before reporting completion, run:

```bash
python3 scripts/validate.py
```

The command must validate schemas and examples, record links, Markdown links, structure, vocabulary and safety checks, visual synchronization, and the generated index. Read back `reports/validation-report.md` and report every failed or deferred item.
