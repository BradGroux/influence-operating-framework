# Contributing

Contributions should leave the framework and its communities better than they
were found.

## Contribution License

By submitting material for inclusion, a contributor agrees to license that
contribution under the repository's [MIT License](LICENSE.md) and confirms that
they have the right to do so. No separate contributor license agreement is
required.

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Do not
include credentials, personal information, private evidence, confidential
material, or security-sensitive details in an issue, pull request, review, or
appeal. Follow the [security and privacy policy](SECURITY.md) for sensitive
disclosures.

## Before Proposing a Change

1. Read the [charter](framework/charter.md),
   [operating framework](framework/operating-framework.md), and
   [business-framework decision](decisions/0001-business-framework-not-technical-specification.md).
2. Decide whether the proposal is a correction, clarification, canonical
   change, charter amendment, illustration, or project record.
3. Bring public, community-owned, or authorized evidence for factual claims.
4. Remove private contact details, unsupported relationship claims,
   confidential material, and unnecessary personal information.
5. Explain which concern, practice move, responsible-practice boundary, or
   repository safeguard the proposal improves.
6. Identify meaningful alternatives, trade-offs, limitations, dissent, and
   downstream documents that may be affected.

Use a
[framework contribution issue](https://github.com/BradGroux/influence-operating-framework/issues/new?template=framework-contribution.yml)
for a proposal or question. Use a pull request when the change is prepared for
review.

## Content Standard

- Write for practitioners, not for a particular tool or platform.
- Keep requirements in canonical framework documents and scenario-specific
  choices in examples.
- Separate observed facts, interpretation, and open questions.
- Preserve waiting, declining, no action, and do not contact as valid outcomes.
- Do not introduce schemas, protocols, automation architectures, agent
  contracts, migrations, or technical conformance as framework requirements.
- Use an inline Mermaid diagram only when it materially clarifies a relationship
  or sequence.
- State material human and AI assistance honestly, but use generic role-based
  attribution in public review records unless a specific identity is necessary
  to establish approved professional authority.

Real-person or real-organization examples require explicit maintainer approval,
safe sourcing, appropriate permission, and a clear reason fiction would not
serve the same explanatory purpose.

## Naming Standard

- Use uppercase names for repository-wide policy and metadata files, such as
  `README.md`, `GOVERNANCE.md`, `SECURITY.md`, and `TEMPLATE.md`.
- Use lowercase kebab-case for framework, example, decision, project, workflow,
  and script filenames.
- Prefix ordered examples and decisions with zero-padded numbers, such as
  `01-...` and `0001-...`.
- Name dated project records `<subject>-<record-type>-YYYY-MM-DD.md`.
- Keep reviewer or tester sequence letters, names, model names, tool names, and
  internal platform names out of public review filenames.
- Rename an accepted file only when the consistency benefit outweighs link and
  history disruption; update every repository reference in the same change.

## Decision and Review Path

Use the [decision template](decisions/TEMPLATE.md) for a material framework
choice with reasonable alternatives. Routine editing, formatting, link repair,
and project administration do not require a decision record.

Material canonical changes require the practical application and adversarial
reviews defined in [Governance](GOVERNANCE.md). Lower-risk editorial and
repository-only changes receive review proportionate to their consequence plus
the repository validation gate. A reviewer provides evidence and a
recommendation; the accountable maintainer records the decision.

An appeal must identify the disputed contribution or decision, the grounds,
supporting evidence, and requested resolution. Use the
[appeal issue form](https://github.com/BradGroux/influence-operating-framework/issues/new?template=appeal.yml)
without including sensitive material.

## Verification

Run:

```bash
bash scripts/validate-repository.sh
```

In the contribution description, report what changed, how it was checked, and
any remaining risk or disagreement. Passing validation establishes repository
integrity only; it does not certify real-world practice.
