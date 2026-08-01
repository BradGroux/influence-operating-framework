# 0001: Business framework, not technical specification

- **Status:** Accepted
- **Date:** 2026-08-01
- **Decision owner:** Brad Groux

## Context

The initial repository brief mixed the substance of an influence operating
framework with an implementation toolkit. It required portable schemas,
automation contracts, record migrations, generated visual assets, profiles,
and technical validation. Independent release review then evaluated those
implementation artifacts as though they defined v1 framework quality.

The result was a repository whose technical assurance surface was much larger
than its canonical business guidance. Work on schema history, graph integrity,
message authorization, and render reproducibility displaced work on whether the
framework itself was clear, useful, and applicable.

The related AI-Native Operating Framework established the intended boundary:
business standards should be clear enough for people and machines to use
without becoming software architecture.

## Decision

The Influence Operating Framework is a business operating framework and method.
Its canonical representation is clear human-readable documentation.

The framework defines:

- purpose, context, contribution, relationship, judgment, and learning
  concerns;
- a practical method for applying those concerns;
- evidence, privacy, consent, conduct, and accountability standards; and
- measurement, reflection, and improvement practices.

The framework does not prescribe schemas, APIs, protocols, data models,
automation architectures, agent contracts, adapters, migrations, visual build
pipelines, communication systems, or technical conformance.

An adopter may implement any of those things. They remain separate
implementation choices and cannot redefine framework meaning.

## Consequences

- Canonical content lives under `framework/`.
- This record preserves rationale; its accepted meaning has normative effect
  through the corresponding canonical documents rather than as a separate
  framework layer.
- Examples are human-readable Markdown and do not add requirements.
- Diagrams are inline Mermaid only when they materially clarify the prose.
- Repository validation checks document integrity rather than operational or
  technical conformance.
- Application reviews evaluate conceptual coherence, practical usefulness,
  responsible-practice boundaries, and clarity before release mechanics.
- Future implementation kits, if any, must live outside the canonical framework
  and identify which choices are local rather than required.

## Superseded direction

The initial portable-record toolkit, schema migrations, automation-agent
contracts, generated visual matrix, and associated release-assurance criteria
are not v1 framework requirements. They remain available in Git history but are
not part of the framework-first release.
