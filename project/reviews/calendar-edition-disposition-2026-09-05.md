# Calendar edition audit and disposition

- **Status:** Accepted candidate; publication checks remain separate
- **Decision date:** 2026-09-05
- **Baseline:** `cc5a25d3523a33347c75644d4f41920822cb12f5`
- **Authority:** Brad Groux, current owner instruction to audit, remediate and release

## Scope and source record

The audit covers the tracked public tree: canonical framework, glossary,
examples, governance/contribution/conduct/security policies, templates,
decisions, historical reviews/releases, signing record, validation scripts and
CI. Git history, released tags/bodies, all 14 preceding issue/PR records and
relevant discussion were inspected. There were no open baseline issues.
Historical #9's stale-citation diagnosis remains rejected: historical paths
must resolve at their reviewed commits, not today's tree. #5/#6 duplication and
#10/#11/#13 resolutions remain historical, not reopened requirements.

Exact Commons provenance and affected guidance are recorded in
[decision 0005](../../decisions/0005-calendar-editions-and-commons-adoption.md).
Relationship is the only neighboring method with a material local boundary;
its inspected charter explicitly separates stewardship from Influence's
participation. No other product integration, shared runtime or version consumer
exists here. No other repository was modified.

## Prioritized tracker and disposition

| Issue | Priority and evidence at baseline | Disposition and acceptance |
|---|---|---|
| [15](https://github.com/BradGroux/influence-operating-framework/issues/15) | Content first: Governance lines 88–92 conflates normative rationale with demonstrated practice improvement; assisted example lines 94–96 asserts unmeasured effort savings | Separate evidence classes; remove effect overstatement; exercise the adverse cases below. No field-effectiveness claim. |
| [16](https://github.com/BradGroux/influence-operating-framework/issues/16) | Owner-requested edition/adoption transition; VERSION and active Governance/README still use prior identities | Prospective calendar policy and exact independent Commons adoption; preserve every historical identity and assess compatibility separately. Depends on 15. |
| [17](https://github.com/BradGroux/influence-operating-framework/issues/17) | Validator lines 75, 266–278 reject correction suffixes and hardcode date; lines 492–503 omit candidate history when main exists | Actual date parsing, exact active fields and candidate/main history union, with isolated regressions. Depends on 16. |
| [18](https://github.com/BradGroux/influence-operating-framework/issues/18) | Live baseline had no version-tag ruleset and immutable releases disabled; release gate had only local readback | Tag ruleset 22320011 prevents update/deletion with no bypass; future release immutability enabled; runbook and exact public verifier. Depends on candidate reviews and 15–17. |

These are public documentation and release-assurance findings, not reports of
credential compromise or an observed coercive incident. Private disclosure
remains required for sensitive findings. No such finding was identified.

## Fictional adverse and ambiguous cases

These are document interpretation tests, not observations from practice or
specialist validation. Canonical guidance controls; the cases add no rules.

| Case | Reasoned decision and source |
|---|---|
| A beginner requests an accommodation before contributing | Help need not be earned; the recipient can state capacity. Practice-method introduction and responsible standard Contribution and power. |
| A practitioner spent days on an unwanted artifact and expects access in return | Accept refusal without debt or penalty; change or stop the contribution. Contribution concern and responsible standard. |
| A sponsor asks for private participant data and suggests nonparticipants lose unrelated benefits | Withhold data and refuse coercive terms; disclosure alone does not cure power imbalance. Privacy, power and conflicts sections; sponsorship example. |
| A volunteer promise has become unsafe; the recipient has also said not to contact them | End or narrow unsafe work, account for any safe handoff, and preserve the no-contact boundary. Sustain/completion and Relationship concern; closure is not permission to send. |
| A private lesson could make a persuasive public success story | Withhold or use an authorized safe summary; public-by-default does not override privacy. Charter and proportional research. |
| Readership doubles after publication, but evidence of use is absent | Report reach separately; useful benefit and causal impact remain unknown. Measurement Reflection. |
| Assistance drafts quickly but corrections take longer than manual drafting might have | Do not claim net savings without comparison. The assisted example explicitly leaves net effort unknown. |
| A refusal is nominally allowed but a manager controls the person's standing | Narrow or stop when refusal cannot be protected from unrelated penalty. Contribution and power. |
| A person requests no contact; time passes and a new channel becomes available | No retry: only their affirmative change lifts their boundary. Consent section and glossary. |
| A team uses Influence and Relationship together | No compulsory lifecycle, sales pipeline, duplicate notes or authority transfer. Relationship concern and independent product charter. |
| New Commons main wording seems inconsistent with an older adopted pin | Compare the exact adopted release; pause only the disputed representation. Record owner, rationale and revisit trigger through local Governance. |

## Coverage and non-findings

Six concerns, seven optional moves, measurement dimensions, glossary and all
three examples remain coherent. Existing safeguards cover false familiarity,
manufactured reciprocity, confidentiality, consent and authority, community
burden, honest uncertainty and restraint. No replacement framework, mandatory
forms, metrics quota or duplicated method is justified. Missing field evidence
remains an open knowledge limitation, not a completed research requirement.

This is Markdown documentation with local verification scripts. Application
architecture, runtime APIs, authentication sessions, persistence, data flows,
service concurrency, runtime resource/performance tuning, deployment and user
logs are non-applicable. Repository concerns do apply: bounded CI, read-only
permissions, unpersisted checkout credentials, input/date validation, signing,
public-history scanning and dependency exposure. No production dependencies
were added. The renderer pins its direct CLI version but uses transient,
unlocked transitive dependencies; full reproducibility is not claimed.

The existing inline Markdown link checker supports the repository's current
link style; it is not a general Markdown parser. Its enumerated checks and
secret scan do not establish absence of every possible unsafe publication.
No new visual meaning or layout is introduced; all eight unchanged Mermaid
sources require compilation, not a new visual redesign.

## Evidence and release gates

The independent [content/application/adversarial review](calendar-edition-content-review-2026-09-05.md)
and [standards review](calendar-edition-standards-review-2026-09-05.md) returned
GO with no unresolved findings at `e55af06e2492620514337650766d975a4fb6d71c`.
They resolved the authorized-representative summary inconsistency and the
fail-fast/publication-date runbook finding. Three regression methods with
subcases passed; full repository validation rendered 8/8 Mermaid diagrams.
Depth-1 validation passed with explicit unavailable-history reporting, while
release validation correctly rejected the shallow checkout. Full-history
Gitleaks found no secrets; npm audit reported zero known vulnerabilities in
the inspected transient renderer tree. The original v1.0.2 signed gate passed
at its unchanged commit. Merged-tree, CI, signature, tag workflow and release
readback remain separate publication conditions. This record-only follow-up
does not change the reviewed canonical content or executable scripts.

Historical v1.0.0/v1.0.1 remain unsigned legacy releases; v1.0.2 retains its
tracked-key signature and exact target. Existing review citations and release
bodies are preserved. The new calendar verifier intentionally does not claim
retroactive assurance for old releases. No practical effectiveness, external
adoption, certification or domain validation has been established.
