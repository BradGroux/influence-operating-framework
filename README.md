# Influence Operating Framework

The Influence Operating Framework is an open business operating framework for
building meaningful influence through useful contribution, trusted
relationships, accountable judgment, and continuous learning.

It is for practitioners and mission-led groups working across communities,
education, open source, media, speaking, philanthropy, technology, public
service, and commercial settings. It helps them decide where to participate,
what value to create, when engagement is appropriate, what commitments to
honor, and what outcomes should change future practice.

Influence here means the earned capacity to help ideas, people, and communities
move. It is not follower count, access, status, or the ability to manufacture
attention.

## Research and Stewardship

The framework is developed as part of
[Digital Meld](https://digitalmeld.io)'s research arm. This relationship
provides research, application, and learning context; it does not grant Digital
Meld authority to redefine the framework outside its documented governance and
contribution processes.

Brad Groux is the creator and founding steward. Changes follow
[Governance](GOVERNANCE.md) and the [contribution guide](CONTRIBUTING.md).

## Open Framework Commons

Influence adopts [Open Framework Commons](https://github.com/BradGroux/open-framework-commons)
as shared documentation at annotated tag
[`v1.1.0`](https://github.com/BradGroux/open-framework-commons/releases/tag/v1.1.0),
release commit
[`f25a2b89b4aed95984fd235e2e229efe52c125d8`](https://github.com/BradGroux/open-framework-commons/commit/f25a2b89b4aed95984fd235e2e229efe52c125d8).

The adoption disposition is:

- **Adopted:** all nine shared principles and the shared boundaries for
  people-first, tool-independent, contribution-led, openly documented, and
  honestly reviewed work, including recognition of Focus Operating Framework
  as the fifth equal, independent product in Commons scope;
- **Deferred as product-local:** Mission Control, community-extension topics,
  and guidance owned by other ecosystem products; and
- **Deviations:** none. Influence's stronger human-judgment, consent, and
  external-action boundaries remain compatible local guidance.

Influence remains independent. It owns its concerns, method, terminology,
examples, research, governance, roadmap, implementation choices, and releases.
Commons is not a parent framework and cannot amend Influence automatically.
The [current adoption decision](decisions/0004-adopt-open-framework-commons-v1.1.0.md)
and [Governance](GOVERNANCE.md#open-framework-commons-adoption) record the
authority boundary.

## The Framework

Every responsible influence practice makes six concerns clear:

1. **Purpose** — Why are we participating, and who should benefit?
2. **Context** — What do we know, how do we know it, and what remains unknown?
3. **Contribution** — What useful value can we create without requiring
   reciprocity?
4. **Relationship** — What shared history, commitments, consent, and boundaries
   matter?
5. **Judgment** — What should a person decide now, including waiting or taking
   no action?
6. **Learning** — What happened, what changed, and how should the practice
   improve?

These concerns apply to existing work. The framework does not require a
particular tool, database, data model, automation system, or communication
platform.

## Start Here

Read the canonical framework in this order:

1. [Charter](framework/charter.md)
2. [Operating framework](framework/operating-framework.md)
3. [Practice method](framework/practice-method.md)
4. [Responsible practice standard](framework/responsible-practice-standard.md)
5. [Measurement and learning](framework/measurement-and-learning.md)
6. [Glossary](framework/glossary.md)

Then use:

- [Examples](examples/README.md) to see the framework applied in three
  fictional contexts;
- [Decision records](decisions/README.md) to understand material choices and
  their rationale;
- [Governance](GOVERNANCE.md) to understand authority, review, and releases;
- [Contributing](CONTRIBUTING.md) to propose or prepare a change;
- [Code of Conduct](CODE_OF_CONDUCT.md) for participation expectations; and
- [Security and privacy](SECURITY.md) before reporting sensitive information.

## Quick Application

For any activity, write one honest answer for each of the six concerns. If
purpose is unclear, evidence is weak, the contribution is speculative, a
boundary is unresolved, or the practitioner cannot honor the resulting
commitment, stop or narrow the activity. Waiting, declining, and doing nothing
are successful outcomes when they protect people or purpose.

## Repository Structure

| Path | Purpose | Authority |
|---|---|---|
| `framework/` | Charter, operating framework, method, practice standard, measurement guidance, and glossary | Canonical framework |
| `examples/` | Fictional application examples | Explanatory; cannot amend the framework |
| `decisions/` | Accepted decisions and reusable decision template | Rationale for canonical changes |
| `project/` | Development and review records | Historical evidence; not framework content |
| `CONTRIBUTING.md` | Contribution and review process | Repository process |
| `GOVERNANCE.md` | Stewardship, authority, amendment, and release rules | Repository governance |
| `CODE_OF_CONDUCT.md` | Participation and enforcement expectations | Community standard |
| `SECURITY.md` | Private reporting and sensitive-disclosure guidance | Repository safeguard |
| `CITATION.cff` | Citation metadata | Release metadata |
| `scripts/validate-repository.sh` | Complete local validation entry point | Repository verification |

## What This Is Not

This is not a CRM, lead funnel, engagement-farming playbook, public-speaking
checklist, messaging system, or technical specification. It does not prescribe
schemas, APIs, agent contracts, record formats, visual build pipelines, or
autonomous outreach.

People and tools may assist with research, drafting, organization, and
reflection. The practitioner remains accountable for evidence, privacy,
contribution, commitments, and every external action.

## Current Status

Version 1.0.2 is the current owner-approved release, dated 2026-08-22. It adds
cryptographically verified release tags and a complete-history release gate
without changing canonical framework meaning. Version 1.0.1 adopted Open
Framework Commons v1.1.0 and corrected shallow-clone contributor validation.
Version 1.0.0 remains the initial release, dated 2026-08-01 and republished on
2026-08-03 to include the original Commons adoption and focused framework
visualizations before documented use. Its final canonical framework reviews
found no Blocker, Material, Minor, or Suggestion findings:

- [Canonical coherence review](project/reviews/v1.0.0-final-canonical-coherence-review-2026-08-01.md)
- [Practical application review](project/reviews/v1.0.0-final-practical-application-review-2026-08-01.md)
- [Adversarial misuse review](project/reviews/v1.0.0-final-adversarial-misuse-review-2026-08-01.md)

The Commons adoption and v1.0.0 republish received separate exact-candidate
[practical application](project/reviews/open-framework-commons-v1.0.0-adoption-practical-application-review-2026-08-03.md)
and
[adversarial scope](project/reviews/open-framework-commons-v1.0.0-adoption-adversarial-scope-review-2026-08-03.md)
reviews. Both returned GO with no findings after two first-pass Minor
consistency findings were resolved. The
[maintainer disposition](project/reviews/open-framework-commons-v1.0.0-adoption-review-disposition-2026-08-03.md)
records the republish decision and limits.

The focused visualizations received separate exact-candidate
[practical application](project/reviews/v1.0.0-visualization-practical-application-review-2026-08-03.md)
and
[adversarial scope](project/reviews/v1.0.0-visualization-adversarial-scope-review-2026-08-03.md)
reviews. Both returned GO with no findings after the candidate resolved four
iterative Minor clarity findings and one layout suggestion. The
[maintainer disposition](project/reviews/v1.0.0-visualization-review-disposition-2026-08-03.md)
records the visualization and republish decision.

The [release-integrity review](project/reviews/v1.0.0-final-release-integrity-review-2026-08-01.md)
returned GO with three repository-maintenance findings. This publication pass
resolves them by documenting the transient Mermaid renderer accurately,
aligning validation claims with implemented checks, and restoring concise
source evidence to historical reports.

The examples are fictional, illustrative, and not domain-validated. The
independent reports are source-bounded AI-assisted review evidence; they are
not human, organizational, legal, ethical, professional, or domain validation.

Run the complete repository gate before submitting or releasing a change:

```bash
bash scripts/validate-repository.sh
```

The gate checks required files, local Markdown links and anchors, version and
citation metadata, review-record conventions and historical evidence targets,
publication-safety patterns, sanitized public history, framework-boundary
paths, and Mermaid rendering. It does not certify a real-world implementation
or prove legal compliance, ethics, accessibility, or community acceptance.
Mermaid rendering uses a transient, pinned command-line renderer through `npx`;
no package manifest, lockfile, generated diagram, or committed dependency tree
is required. On GitHub-hosted Linux runners, a narrowly scoped Puppeteer
configuration disables Chromium's unavailable process sandbox while rendering
repository-owned Markdown in the disposable CI environment.

In a shallow clone, the gate keeps current-tree checks active and reports
historical review evidence and public-history coverage as partial. Run
`git fetch --unshallow` before a release or whenever complete historical
assurance is required.

Release maintainers use `bash scripts/validate-release.sh` from a clean checkout
with complete history. Version tags must be signed annotated tags that verify
against the tracked public signing key and resolve exactly to the released
commit.

## Contributing and Support

Use [GitHub Issues](https://github.com/BradGroux/influence-operating-framework/issues)
for proposals, questions, and appeals. Use
[pull requests](https://github.com/BradGroux/influence-operating-framework/pulls)
for prepared changes. Do not put credentials, personal information, private
evidence, or sensitive conduct reports in a public issue or pull request.

## License and Citation

The framework is available under the [MIT License](LICENSE.md). Its designated
public home is
[github.com/BradGroux/influence-operating-framework](https://github.com/BradGroux/influence-operating-framework).
Formal citation metadata is provided in [`CITATION.cff`](CITATION.cff).

## Development Records

Planning and review artifacts are preserved under [`project/`](project/README.md)
so contributors can inspect how decisions were reached without confusing those
records with the framework itself.
