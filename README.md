# Influence Operating Framework

The Influence Operating Framework is an open operating model for building meaningful influence through useful contribution, sustained relationships, reflection, and repeatable practice.

It helps a practitioner answer four connected questions:

1. Where can I contribute to communities and ecosystems aligned with my mission?
2. What do verified evidence and existing relationships actually support?
3. What thoughtful action—including no action, waiting, or not contacting—fits the context?
4. What did the outcome teach, and how should the practice change?

This is not a sales CRM, a lead funnel, an engagement-farming playbook, or a speaking checklist. Growth and commercial outcomes are supported as downstream effects; they are not the framework's center. No default agent or workflow sends external communication.

## Start here

- Read the [charter](docs/00-charter.md) and [framework overview](docs/01-framework-overview.md).
- Learn the [operating model](docs/02-operating-model.md) and [research method](docs/16-research-methodology.md).
- See how human control works in [human-reviewed outreach](docs/09-human-reviewed-outreach.md).
- Adapt the framework with the [implementation guide](docs/15-implementation-guide.md) and [templates](templates/README.md).
- Review [Brad Groux's owner-supplied profile](profiles/brad-groux/profile.md) and the [fictional Riverbend profile](profiles/riverbend-learning-collective/profile.md).
- Browse the generated [repository index](INDEX.md).

## One-command validation

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
npm install
python3 scripts/validate.py
```

The validator checks repository structure, JSON Schemas and every fictional example, linked record IDs, Markdown links, public-data safety, external-action boundaries, visual sources and renders, and the generated index. It rewrites [the validation report](reports/validation-report.md) with explicit passed, failed, and deferred items.

When records have changed since a prior authoritative export, verify that human decision histories were only appended:

```bash
python3 scripts/validate.py --only schemas --baseline-root /path/to/authoritative-snapshot --no-report
```

No self-contained current snapshot can prove that omitted prior history never existed; release and private-overlay procedures must retain the authoritative baseline used by this check.

To rerender diagrams separately:

```bash
npm run render:visuals
```

## Human and agent use

Humans and agents use the same canonical documents. Agents may perform only the bounded work described in [automation contracts](automations/README.md). A draft can receive a human disposition of approve, revise, wait, or do not contact; even approval is not a send. Any later sending system is separate and requires explicit authorization outside this repository.

## Public and private records

Everything committed here is safe for public review. Real sensitive notes, personal contact details, consent records, and restricted evidence belong in a private overlay governed by [ethics, privacy, and safety guidance](docs/12-ethics-privacy-and-safety.md). The public repository documents that boundary but does not contain private data.

## Status

Version 1.0.0-rc.1 is a local release candidate under independent review. It is not the final v1.0.0 release and does not claim independent ethics, privacy, accessibility, legal, or domain approval. See [v1.0.0 release criteria](project/specifications/v1.0.0-release-criteria.md), [project status](project/planning/status.md), and [the validation report](reports/validation-report.md).

## License

[MIT](LICENSE)
