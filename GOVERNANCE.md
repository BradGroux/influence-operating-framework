# Governance

**Status:** Approved initial repository governance<br>
**Founding steward:** Brad Groux<br>
**Last reviewed:** 2026-09-05

## Stewardship

Brad Groux is the founding steward. Future maintainers or successors require an
explicit public record.

Stewardship protects the charter, preserves the framework's business boundary,
distinguishes requirements from examples, and reports uncertainty and review
limits honestly. Teaching, applying, commercializing, or implementing the
framework does not independently grant authority to redefine it.

The framework is developed through
[Digital Meld](https://digitalmeld.io)'s research arm. This affiliation does
not grant Digital Meld decision authority outside this governance process.

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

## Open Framework Commons adoption

Influence adopts [Open Framework Commons](https://github.com/BradGroux/open-framework-commons)
as shared documentation at annotated tag
[`v2026.09.05`](https://github.com/BradGroux/open-framework-commons/releases/tag/v2026.09.05),
release commit
[`8868a248457dd7b663563beb243c5ebcbb8ac360`](https://github.com/BradGroux/open-framework-commons/commit/8868a248457dd7b663563beb243c5ebcbb8ac360).

Commons is a referenced shared foundation, not a parent authority, and does not
enter the Influence authority chain above. Influence retains authority over
its concerns, method, terminology, examples, research, governance, roadmap,
implementation choices, and releases.

All Commons v2026.09.05 shared principles and boundaries are adopted with no
deviation. The updated help-seeking, disengagement and privacy boundaries are
expressed in local canonical guidance. Commons review and release tooling
remain Commons-local; this repository independently adopts the proportionate
evidence distinction and calendar-edition policy below. This includes recognizing
Focus Operating Framework as the fifth
equal, independent product in Commons scope and evaluating future shared
proposals across all five products. Product-local Mission Control,
community-extension topics, and guidance owned by other ecosystem products
remain deferred unless separately accepted through this governance.
Influence's more specific human-judgment, consent, and external-action
requirements remain local and controlling for Influence practice.

If Commons and Influence appear to conflict, pause the disputed action or
representation while unrelated safe work continues. Identify the exact adopted
tag and commit, the statements in tension, affected people and uncertainty.
Use a safe summary when evidence is private; silence is not permission.
The founding steward or a documented successor resolves it through
the applicable Influence change path, recording the rationale, dissent, scope
of any resumed action and, for a deferral, an owner and concrete revisit trigger.
Influence decides its local guidance; a shared amendment needs a separate
Commons decision. A later Commons release has no effect
until Influence records a separate adoption, deferral, or deviation decision.
See [decision 0005](decisions/0005-calendar-editions-and-commons-adoption.md).

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
documented successor. Canonical changes require maintainer review and a
proportionate rationale
without contradicting the charter. Distinguish a chosen commitment, an
interpretation, and a claim about an effect. Record supporting evidence and
context, the strongest adverse case, affected decisions, dissent, and the
reason to accept, revise, defer or reject. Chosen values need accountable
reasons; effect claims need evidence appropriate to the claimed effect.
Fictional scenarios and document review can test interpretation but cannot
establish improved real practice. Keep missing practitioner or specialist
evidence explicit and identify what observation would justify reconsideration.
A wording correction does not require a research dossier. Examples
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

New documentation editions use `YYYY.MM.DD` and signed annotated tags
`vYYYY.MM.DD`, based on the actual UTC publication date. Further publications
on that day use `.1`, then `.2`, in numeric order. Order calendar editions by
date and then correction number; historical v1.0.2 precedes the first calendar
edition. The identifier says nothing about compatibility or effectiveness.
Never replace a published tag or add dated aliases to historical editions.
Preserve old release bodies, citations, decisions, reviews and adoption pins.
If publication crosses a UTC date, update candidate metadata before tagging.

Release notes assess changes to reader decisions, permissions, responsibilities,
scope and authority separately from the date. A clarification that narrows a
previous interpretation is substantive and potentially incompatible, even when
it matches prior intent. Name what adopters should reconsider; no downstream
product adopts automatically. The product edition and Commons pin are separate.
See the [release runbook](project/releases/releasing.md). A release must:

- identify the exact canonical change;
- pass release validation from a clean checkout with complete Git history;
- use a cryptographically signed annotated tag verified against the tracked
  public signing key and resolving exactly to the released commit;
- disclose open limitations and dissent; and
- avoid claims of legal, ethical, accessibility, or professional certification
  that the review did not establish.

A release with a material canonical change must receive a practical
application review and an adversarial framework review. Editorial corrections,
repository-only maintenance, and other changes that preserve framework meaning
receive review proportionate to their risk plus the repository document checks.

No version number or automated check overrides an unresolved material framework
finding.

Repository content and accepted contributions are licensed under the
[MIT License](LICENSE.md).

### Edition 2026.09.05

- **UTC publication date:** 2026-09-05
- **Predecessor:** v1.0.2, preserved unchanged
- **Compatibility and limitations:** [release record](project/releases/v2026.09.05-release-2026-09-05.md)
- **Authority and rationale:** [decision 0005](decisions/0005-calendar-editions-and-commons-adoption.md)

### Version 1.0.0 Release Baseline

- **Version:** 1.0.0
- **Effective date:** 2026-08-01
- **Repository version:** annotated tag `v1.0.0`
- **Republished:** 2026-08-03 after adopting Open Framework Commons v1.0.0 and
  adding focused visualizations before documented use; prior published tag
  targets were `7d4727a8cf889d621e45854c874a5e0a15a94a56` and
  `f91851a1b42b28b01928e5db7aaac4c20b946417`, and the immediately prior
  product tag target was
  `cbe41ccd84f2027f58ae7938df09131b5fbde3ca`
- **Material changes:** recorded in the [changelog](CHANGELOG.md)
- **Known limitations:** examples are fictional, illustrative, and not
  domain-validated; independent reports are source-bounded AI-assisted review
  evidence rather than human, organizational, professional, or domain
  validation; real-world use has not been certified
- **Superseded public version:** none
- **Responsible steward:** Brad Groux
- **Publication destination:**
  [`github.com/BradGroux/influence-operating-framework`](https://github.com/BradGroux/influence-operating-framework)

### Version 1.0.1 Release Baseline

- **Version:** 1.0.1
- **Effective date:** 2026-08-22
- **Repository version:** annotated tag `v1.0.1`
- **Material changes:** recorded in the [changelog](CHANGELOG.md)
- **Framework effect:** no canonical meaning change; adopts Open Framework
  Commons v1.1.0 and improves shallow-clone validation reporting
- **Known limitations:** shallow clones cannot verify unavailable historical
  review evidence or complete public history; full release assurance requires
  complete Git history
- **Superseded public version:** 1.0.0 remains available as historical release
- **Responsible steward:** Brad Groux
- **Publication destination:**
  [`github.com/BradGroux/influence-operating-framework`](https://github.com/BradGroux/influence-operating-framework)

### Version 1.0.2 Release Baseline

- **Version:** 1.0.2
- **Effective date:** 2026-08-22
- **Repository version:** signed annotated tag `v1.0.2`
- **Material changes:** recorded in the [changelog](CHANGELOG.md)
- **Framework effect:** no canonical meaning change; adds cryptographic release
  identity and makes complete Git history a mandatory release gate
- **Known limitations:** signature verification establishes control of the
  registered release key, not real-world framework effectiveness
- **Superseded public version:** 1.0.1 remains available as historical release
- **Responsible steward:** Brad Groux
- **Publication destination:**
  [`github.com/BradGroux/influence-operating-framework`](https://github.com/BradGroux/influence-operating-framework)

## Conflicts and Appeals

Conflicting interpretations are recorded and escalated to the founding steward
or a future governing body. Material dissent remains visible with the decision.

An appeal identifies the disputed contribution or decision, grounds, evidence,
and requested resolution. Appeals of maintainer decisions go to the founding
steward or future governing body. When the founding steward made the disputed
decision and no broader governing body exists, the steward conducts a
documented reconsideration with an uninvolved reviewer when practical and
records that governance limitation.

## Governance Review

Review this document when participation materially expands, maintainers or
decision authorities change, repeated contribution or appeal problems occur, a
release exposes unclear authority, licensing changes, or the founding steward
proposes a broader governing body.
