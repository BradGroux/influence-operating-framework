# Governance

## Stewardship

Brad Groux is the founding steward. Future maintainers or successors require an
explicit public record.

Stewardship protects the charter, preserves the framework's business boundary,
distinguishes requirements from examples, and reports uncertainty and review
limits honestly. Teaching, applying, commercializing, or implementing the
framework does not independently grant authority to redefine it.

## Authority

Framework authority descends in this order:

1. [Charter](framework/charter.md)
2. Remaining canonical documents under [`framework/`](framework/README.md)
3. Governance and contribution guidance
4. Examples and project records

Lower-authority material cannot silently change higher-authority meaning.
Accepted [decision records](decisions/README.md) preserve rationale and
authorize corresponding edits, but they do not form a separate normative
layer. A decision changes the framework only when its accepted meaning appears
in the canonical documents.

## Change paths

- **Correction:** Fix a demonstrable error without changing framework meaning.
- **Clarification:** Improve language or examples while preserving meaning.
- **Canonical change:** Change the operating framework, practice method,
  responsible-practice standard, measurement model, or glossary.
- **Charter amendment:** Change the definition, mission, commitments, scope, or
  accountability boundary.
- **Illustration:** Add or improve an example without creating a requirement.

Material choices with reasonable alternatives belong in a decision record.
Routine wording and maintenance do not.

## Review standard

A proposal should state:

- the problem and evidence;
- the affected framework concern or community;
- alternatives and trade-offs;
- privacy, consent, accessibility, or safety implications;
- whether the change is framework meaning or only an illustration; and
- dissent, uncertainty, and follow-up that remain.

Charter amendments require written approval from the founding steward or a
documented successor. Canonical changes require maintainer review and evidence
that they improve real practice without contradicting the charter. Examples
require clarity, truthful provenance, publication safety, and framework
alignment.

Decisions may be accepted, revised, deferred, or rejected. Material dissent
remains visible in the record.

## Framework and implementations

The framework does not govern the internal architecture of tools that apply it.
An implementation may use databases, schemas, APIs, AI, automation, or other
technical controls. It must identify those as local choices and must not present
them as framework requirements.

An implementation claiming alignment should explain how its business practice
addresses the six concerns and responsible-practice standard. This repository
does not certify implementations.

## Releases

The project uses semantic versioning for published framework releases. A
release must:

- identify the exact canonical change;
- pass repository document validation;
- disclose open limitations and dissent; and
- avoid claims of legal, ethical, accessibility, or professional certification
  that the review did not establish.

A release with a material canonical change must receive a practical
application review and an adversarial framework review. Editorial corrections,
repository-only maintenance, and other changes that preserve framework meaning
receive review proportionate to their risk plus the repository document checks.

No version number or automated check overrides an unresolved material framework
finding.
