# Validation report

**Repository version:** 1.0.0-rc.2
**Candidate source SHA-256:** `9ed0011a4abb41e70b2e04c0a20e7f3020ca5056ba6d4936bcd0146e8b3f752e`
**Source worktree state (excluding this report):** DIRTY
**Overall:** PASS
**Command:** `python3 scripts/validate.py --baseline-root <authoritative-root>`

This report records direct repository checks. It does not convert owner decisions or independent reviews into implementation success.

## Automated gates

| Gate | Status | Evidence |
| --- | --- | --- |
| index | PASS | INDEX.md is current |
| links | PASS | 278 repository-local Markdown links resolve |
| public-data-safety | PASS | public examples are fictional, public-classified, and contain no non-reserved email addresses |
| outreach-safety | PASS | approve, revise, wait, and do-not-contact are explicit; schema and contracts expose no sender |
| schemas | PASS | 13 schemas and 18 fictional records validate under Draft 2020-12 |
| graph-references | PASS | all references resolve across 18 stable record IDs |
| history-baseline | PASS | authoritative baseline source SHA-256 f2667c94e9f6db84f8f116107c0661751ab6cc7ce1fd86cc48eba5f511c8a29b compared across 18 records and 5 decision histories |
| structure | PASS | 108 required repository artifacts exist |
| documentation | PASS | 17 canonical docs and all agent contracts are substantive and complete |
| tests | PASS | 60 acceptance tests pass |
| visuals | PASS | 12 Mermaid sources have synchronized SVG, PNG, metadata, and accessible descriptions |
| report | PASS | deterministic full-gate report regenerated and read back |

## Failed or deferred automated gates

No automated gate failed.

## Visual inspection

The release-candidate lifecycle change passed the recorded [visual readback](../project/reviews/v1.0.0-rc.1-visual-readback-2026-08-01.md). This is not an independent human accessibility review.

## Deferred items

| Item | Status | Completion condition |
| --- | --- | --- |
| Public repository host and slug | DEFERRED | Owner selects and authorizes a publication target. |
| Additional maintainers and CODEOWNERS | DEFERRED | Named maintainers accept documented responsibilities. |
| Dedicated private security and conduct channel | DEFERRED | Owner publishes an appropriate monitored private channel. |
| Release signing and long-term cadence | DEFERRED | Maintainers approve signing, custody, and cadence policy. |
| Tool-specific private overlay and messaging integrations | DEFERRED | Separate proposals pass privacy, access, retention, and external-action review. |
| Fresh post-fix two-agent review | DEFERRED | Both independent agents review the same exact hardened candidate SHA with no unresolved Blocker or Material findings. |
| Independent ethics, privacy, accessibility, legal, and domain review | DEFERRED | Qualified human reviewers complete reviews and dispositions before a final 1.0.0 maturity claim. |
| Independent verification of Brad profile statements | DEFERRED | Owner approves source-based public research; the release candidate remains explicitly owner-supplied. |
| Final owner approval | DEFERRED | Owner reads the validation and review dispositions and approves the final commit and annotated tag. |

## Safety conclusion

The public examples are fictional, schemas and graph references validate, every outreach path retains human approve/revise/wait/do-not-contact dispositions, and the default implementation exposes no sending capability.
