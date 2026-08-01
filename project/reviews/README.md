# Reviews

This directory preserves release findings, dissent, and maintainer disposition.
Reports evaluate an exact commit and do not become framework requirements.

## Review perspectives

1. **Application:** Can a practitioner use the framework across realistic
   contexts without hidden technical machinery?
2. **Adversarial:** Is the business method coherent, bounded, and resistant to
   transactional or manipulative use?
3. **Simplicity and scope:** Does each canonical element earn its place without
   turning the framework into a technical system or exhaustive procedure?

Reviewers read the canonical framework before examples. Optional
implementation choices are not defects or requirements.

## Standard report format

Each report contains:

- review date, reviewer role, reviewed version, and exact commit;
- verdict and counts for Blocker, Material, Minor, and Suggestion findings;
- executive summary, findings, verification, limitations, and final verdict;
- repository-relative evidence without reviewer personas, model names, local
  machine paths, temporary checkout details, or access diagnostics.

Sanitization may remove operational noise and normalize presentation. It must
not change the reviewed commit, verdict, severity, finding substance, or stated
limitations. A disposition may accept, reject, downgrade, or combine findings,
but it preserves material dissent.

## Severity and verdict

- **Blocker:** the framework is unusable or directly permits a serious breach
  of its commitments.
- **Material:** a canonical ambiguity or omission is likely to change normal
  practitioner decisions.
- **Minor:** a bounded clarity or consistency problem that does not change the
  likely decision.
- **Suggestion:** optional improvement or editorial judgment.

`GO` requires no unresolved Blocker or Material finding. The maintainer records
the release decision in a separate disposition.

## v1.0.0 record

| Candidate | Application | Adversarial or coherence | Disposition |
|---|---|---|---|
| rc.3 | GO; 1 Minor | NO-GO; 2 Material | NO-GO; findings accepted for rc.4 |
| rc.4 | GO; no findings | GO; no findings | GO; promoted to initial v1.0.0 |
| Initial v1.0.0 supplemental review | GO; 2 Minor | Three NO-GO reports with overlapping and disputed findings | [GO after bounded correction](v1.0.0-supplemental-review-disposition-2026-08-01.md) |
| Corrected v1.0.0 candidate | GO; 1 Minor | GO; 1 Minor | Shared terminology issue corrected |
| Tagged v1.0.0 final audits | GO; no findings | GO in coherence and misuse reviews; no findings | No framework changes requested |

Final tagged-commit reports:

- [canonical coherence](v1.0.0-final-canonical-coherence-review-2026-08-01-i.md)
- [practical application](v1.0.0-final-practical-application-review-2026-08-01-j.md)
- [adversarial misuse](v1.0.0-final-adversarial-misuse-review-2026-08-01-k.md)
