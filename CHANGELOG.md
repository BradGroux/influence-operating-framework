# Changelog

All notable changes to the Influence Operating Framework are documented here.

## 1.0.2 — 2026-08-22

This patch release removes the remaining release-integrity caveats from v1.0.1
without changing canonical framework meaning or rewriting prior release history.

### Changed

- Added a dedicated, GitHub-registered Ed25519 release-signing identity and a
  tracked public allowed-signers record. No private key enters the repository.
- Required signed annotated version tags that verify against the tracked public
  key and resolve exactly to the released commit.
- Added a release-only validation entry point that requires a clean worktree and
  complete Git history before running the full repository and Mermaid gates.
- Kept ordinary contributor validation useful in shallow clones with explicit
  partial-history reporting; shallow release validation now fails closed with
  actionable restoration guidance.
- Updated CI to use the full-history release gate for pull requests, `main`, and
  tags, with cryptographic tag verification on version-tag workflows.

### Audit and release status

- Version 1.0.1 remains unchanged and publicly available as historical release.
- The change affects release stewardship and repository assurance only. It does
  not change the six concerns, seven practice moves, responsible-practice
  standard, measurement guidance, glossary, examples, or Commons disposition.
- Signature verification establishes control of the registered signing key. It
  does not establish real-world, organizational, legal, ethical, accessibility,
  professional, or domain validation.

## 1.0.1 — 2026-08-22

This patch release adopts Open Framework Commons v1.1.0 and makes repository
validation useful and honest in shallow clones. It does not change canonical
framework meaning.

### Changed

- Adopted Open Framework Commons v1.1.0 at annotated tag object
  `79e5f06dab46f262cad1d1daf7840e683ffc3880`, peeling to release commit
  `f25a2b89b4aed95984fd235e2e229efe52c125d8`.
- Recognized Focus Operating Framework as the fifth equal, independent product
  in Commons scope and included it in future shared-applicability review.
- Preserved all nine shared principles, Influence's independent authority, and
  its stronger human-judgment, consent, and external-action boundaries.
- Made shallow-clone validation distinguish unavailable historical objects from
  invalid review evidence, preventing 194 false cascading errors while keeping
  current-tree checks active.
- Labeled shallow public-history coverage as reachable-only and documented
  `git fetch --unshallow` as the release/full-history requirement.
- Added a CI regression check for shallow-clone reporting while retaining the
  full-history primary release gate.

### Audit and release status

- Historical review citations to underscored script filenames remain unchanged
  because they correctly resolve at their exact reviewed commits; current
  hyphenated filenames did not exist at those commits.
- Commons v1.1.0 changes no shared principle or research guidance. Its relevant
  boundary change is the explicit five-product scope.
- The release remains documentation-only and does not claim real-world,
  organizational, legal, ethical, accessibility, professional, or domain
  validation.

## 1.0.0 — 2026-08-01 (republished 2026-08-03)

The first public release establishes a concise, human-first business operating
framework for responsible influence practice.

### Added

- A charter defining the framework's purpose, commitments, scope,
  accountability, and stewardship.
- Six canonical concerns: Purpose, Context, Contribution, Relationship,
  Judgment, and Learning.
- A seven-move practice method: Orient, Understand, Choose, Contribute, Engage,
  Sustain, and Learn.
- A responsible-practice standard covering evidence, proportional research,
  truthful relationships, consent, communication boundaries, accountable human
  judgment, contribution, power, conflicts, corrections, and prohibited
  practice.
- Measurement and learning guidance that keeps contribution, relationship,
  learning, relevant reach, sustainability, and commercial outcomes visible
  without reducing influence to one score.
- An approved glossary and three fictional application examples spanning event
  contribution, community sponsorship, and assisted open-source work.
- Governance, contribution guidance, a Code of Conduct, security and sensitive
  disclosure guidance, decision records, project-history boundaries, and an
  MIT license.
- Citation metadata in `CITATION.cff` and a release version in `VERSION`.
- GitHub issue forms for contribution, appeal, conduct, and sensitive
  disclosure, plus a pull-request template and explicit code ownership.
- A pinned GitHub Actions workflow for automated repository validation.
- A repeatable validation gate covering required structure, local Markdown
  links and anchors, release metadata, review-record conventions and source
  targets, publication-safety patterns, sanitized public history,
  framework-boundary paths, and Mermaid rendering.
- Preserved, sanitized review evidence from application, adversarial,
  coherence, simplicity, misuse, and release-integrity passes.
- Adopted Open Framework Commons v1.0.0 as shared documentation, pinned to
  release commit `a0f0d384e9010a65d1a21a324b4c912433d5e031`, with a public
  discovery reference and an explicit local authority boundary.
- Recorded adoption of all shared principles and boundaries, deferral of
  product-local topics, and no deviations from Commons v1.0.0.
- Five focused Mermaid diagrams covering separate outcome dimensions, the
  assisted-work accountability boundary, and the decision structure of each
  fictional example.

### Changed

- Refreshed the Open Framework Commons v1.0.0 pin from
  `27870fb1d57d951b9ef5a3a86f33ef068ee557da` to
  `a0f0d384e9010a65d1a21a324b4c912433d5e031` after its coordinated
  republication. This changes no Influence method or authority; Influence
  v1.0.0 will be republished after review and merge. The immediately prior
  product tag target,
  `cbe41ccd84f2027f58ae7938df09131b5fbde3ca`, remains release evidence.
- Rebuilt the repository around a canonical business operating framework after
  the pre-release technical toolkit had grown beyond the intended scope.
- Condensed the operating method into seven practical moves and clarified that
  they overlap, repeat, and are not a mandatory lifecycle.
- Distinguished recipient-set communication boundaries from internal
  practitioner precautions.
- Required relevant disclosure and management of material interests and
  legitimate authority for consequential group decisions.
- Clarified that accountable people own judgment while software and AI cannot
  independently decide or transmit external actions, and that batch approval is
  not accountable review.
- Normalized decision labels, separated sustainability from commercial results,
  and compacted repeated learning guidance.
- Consolidated public authority in governance and made release review
  proportional to the consequence of a change.
- Standardized repository names: uppercase root policy and metadata files,
  lowercase kebab-case content and scripts, zero-padded numbered records, and
  dated public review records without internal reviewer sequence letters.
- Replaced named reviewer, tester, agent, model, and platform attribution with
  generic role-based attribution while preserving findings, verdicts,
  limitations, and dissent.
- Established a sanitized public-history baseline using generic review
  attribution and GitHub-provided no-reply author metadata.
- Restored concise repository-relative source evidence to historical findings.
- Documented Mermaid accurately: diagrams remain inline source; rendering uses
  a transient pinned renderer, with no package manifest, lockfile, generated
  export, or committed dependency tree.
- Made Mermaid validation portable across local and GitHub-hosted environments
  by relying only on Git plus standard shell tools before invoking the pinned
  renderer, with a CI-only Chromium configuration for the hosted runner's
  unavailable process sandbox.

### Removed

- Portable JSON Schemas, record migrations, graph fixtures, and profile
  records.
- Automation-agent contracts and implementation workflow templates.
- Generated SVG and PNG exports and diagram metadata.
- Technical release-assurance tests and reports tied to the superseded toolkit.
- The completed framework-first reset specification after its durable boundary
  and rationale were recorded in the decision log and changelog.
- Internal reviewer sequence suffixes and public tester or bot identities from
  release-review filenames and content.

### Review and Release Status

- The rc.3 reviews identified two Material findings involving recipient-set
  boundaries and narrow examples; rc.4 resolved both and received GO from the
  application and adversarial reviews.
- Four supplemental reviews evaluated initial commit
  `c840dd67e613a3d2ae2455f51c4b4eb6bd7895ea` for coherence, practical use,
  misuse resistance, and simplicity.
- Material corrections were committed as candidate
  `0638a29333532578a87f369c043596a15a70fff7` and subjected to fresh practical
  application and adversarial review.
- The canonical coherence, practical application, and adversarial misuse
  reviews of candidate `12947000c0a4f5272070f15024f500efdee61cd9`
  returned GO with no findings.
- The release-integrity review returned GO with three Minor repository
  maintenance findings. The publication pass resolved all three without
  changing framework meaning.
- The examples remain fictional, illustrative, and not domain-validated.
- The independent reports are source-bounded AI-assisted review evidence, not
  human, organizational, legal, ethical, professional, or domain validation.
- The Commons adoption preserves canonical framework meaning and keeps
  Influence's concerns, method, terminology, examples, research, governance,
  roadmap, implementation choices, and releases independent.
- Practical application and adversarial scope reviews of exact candidate
  `de0132859f457bb8008d0524d05eb06def50a7f8` returned GO with no findings after
  resolving two first-pass Minor consistency findings.
- Practical application and adversarial scope reviews of exact visualization
  candidate `998e8811ac920f2da287a0a17d41f030b5e29769` returned GO with no
  findings after four iterative Minor clarity findings and one layout
  suggestion were resolved.
- Before documented use, the owner directed v1.0.0 to be republished again with
  focused visualizations. The immediately prior annotated tag target was
  `f91851a1b42b28b01928e5db7aaac4c20b946417`.
- Before documented use, the owner directed v1.0.0 to be republished with the
  Commons adoption. The original annotated tag target was
  `7d4727a8cf889d621e45854c874a5e0a15a94a56`; `VERSION` and citation metadata
  remain 1.0.0 and retain the initial 2026-08-01 release date.
- The version 1.0.0 release is owner-approved, licensed under MIT, and published
  at `github.com/BradGroux/influence-operating-framework`.

## Pre-release History

### 1.0.0-rc.4 — 2026-08-01

- Closed all rc.3 application and adversarial findings.
- Received independent application and adversarial GO recommendations with zero
  Blocker, Material, or Minor findings.
- Became the initial v1.0.0 candidate and was later corrected in place after the
  supplemental review described above.

### 1.0.0-rc.3 — 2026-08-01

- Produced the first framework-first candidate.
- Independent application review returned GO; adversarial review identified two
  Material findings involving recipient-set boundaries and narrow examples.
- Was superseded by rc.4 after both findings were accepted.

### 1.0.0-rc.2 — 2026-08-01

- Hardened the initial portable-record and visual-toolkit candidate.
- Independent review found unresolved implementation concerns.
- Was superseded by the framework-first rewrite before public release.

### 1.0.0-rc.1 — 2026-08-01

- Produced the first fully validated technical release candidate.
- Was superseded before public release.
