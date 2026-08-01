# Repository instructions

## Purpose

This repository contains the Influence Operating Framework: an open business
operating framework for building useful, trusted influence through
contribution, relationships, sound judgment, and learning.

## Authority

Apply the public authority chain in `GOVERNANCE.md`. A direct current owner
instruction controls the immediate repository task, but any change to framework
meaning must be incorporated into the appropriate canonical document.

Examples illustrate the framework. They do not create requirements.

## Framework boundary

- Treat this as a business operating framework and method, not a software,
  data, automation, or interoperability specification.
- Clear Markdown is the canonical representation for people and machines.
- Do not add required schemas, APIs, protocols, record formats, adapters,
  automation architectures, agent contracts, migrations, or technical
  conformance layers.
- An implementation may use those technologies, but they remain outside the
  framework and cannot redefine it.
- Keep the framework independent of vendors, platforms, models, databases, and
  communication systems.

## Practice boundaries

- Treat people as people, never leads, prospects, targets, or conversions.
- Put contribution and community value ahead of reach, growth, and
  monetization.
- Preserve accountable human judgment for external engagement.
- Never introduce autonomous sending, mass outreach, fabricated relationships,
  or unsupported research claims.
- Make waiting, declining, no action, and do not contact normal outcomes.
- Use fictional public examples unless a real example is explicitly authorized
  and safely sourced.
- Keep private notes, contact details, and sensitive context outside the public
  repository.

## Documentation

- Use the vocabulary in `framework/glossary.md`.
- Prefer direct, practical language over technical or promotional language.
- Explain what a practitioner must understand and decide without prescribing a
  database or workflow engine.
- Add an inline Mermaid diagram only when it materially clarifies a relationship
  or sequence. Do not commit generated image exports or diagram metadata.
- Keep examples subordinate to the canonical framework.
- Follow the filename conventions in `CONTRIBUTING.md` and the review-record
  conventions in `project/reviews/README.md`.

## Verification

Before reporting completion, run:

```bash
bash scripts/validate-repository.sh
```

The gate checks its enumerated required files, local Markdown links and anchors,
release and citation metadata, review-record conventions and source targets,
publication-safety patterns, public-history attribution, fixed
superseded-framework paths, Mermaid fence integrity, and rendering of inline
Mermaid source. It does not fetch external links, infer semantic coherence, or
claim that document checks can prove the quality or ethics of real practice.
