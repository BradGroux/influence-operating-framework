# Contributing

Contributions should leave the framework and its communities better than they
were found.

## Before proposing a change

1. Read the [charter](framework/charter.md),
   [operating framework](framework/operating-framework.md), and
   [business-framework decision](decisions/0001-business-framework-not-technical-specification.md).
2. Decide whether the proposal is a correction, clarification, canonical
   change, charter amendment, or illustration.
3. Bring public, community-owned, or authorized evidence for factual claims.
4. Remove private contact details, unsupported relationship claims,
   confidential material, and unnecessary personal information.
5. Explain which concern, practice move, or responsible-practice boundary the
   proposal improves.

## Content standard

- Write for practitioners, not for a particular tool or platform.
- Keep requirements in canonical framework documents and scenario-specific
  choices in examples.
- Separate observed facts, interpretation, and open questions.
- Preserve waiting, declining, no action, and do not contact as valid outcomes.
- Do not introduce schemas, protocols, automation architectures, agent
  contracts, migrations, or technical conformance as framework requirements.
- Use an inline Mermaid diagram only when it explains something prose cannot
  explain as clearly.

Real-person or real-organization examples require explicit maintainer approval,
safe sourcing, appropriate permission, and a clear reason fiction would not
serve the same explanatory purpose.

## Decision records

Use the [decision template](decisions/template.md) for a material framework
choice with real alternatives. Do not create a decision record for routine
editing, formatting, or project administration.

## Verification

Run:

```bash
python3 scripts/validate_repository.py
bash scripts/validate_mermaid.sh
```

In the contribution description, report what changed, how it was checked, and
any remaining risk or disagreement. Passing validation establishes document
integrity only.
