# Contributing

Contributions should leave the framework and its communities better than they were found.

## Before proposing a change

1. Read the [charter](docs/00-charter.md), [governance](GOVERNANCE.md), and [canonical vocabulary](CONTEXT.md).
2. Identify whether the change affects a locked principle, canonical meaning, an implementation contract, or only an illustration.
3. Bring public or authorized evidence for factual claims. Label inference and hypothesis honestly.
4. Remove personal contact data, confidential material, unsupported relationship claims, and real-person examples unless the maintainer has explicitly approved a safe source-based exception.

## Change paths

- **Correction:** Fix a demonstrable error and cite the supporting source.
- **Clarification:** Improve wording without changing meaning.
- **Extension:** Propose a new concept, schema field, workflow, or agent boundary with use cases and risks.
- **Principle amendment:** Follow the higher bar in [governance](GOVERNANCE.md); a normal pull request cannot silently amend a locked principle.

Material, hard-to-reverse decisions with genuine alternatives belong in an ADR. Routine implementation choices belong in the active specification or change description.

## Verification

Run `python3 scripts/validate.py`. Include the changed behavior, verification result, privacy implications, and any dissent or deferred review in the contribution description. Do not claim a check passed when it was skipped.
