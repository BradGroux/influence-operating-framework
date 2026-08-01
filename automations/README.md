# Bounded automation contracts

These contracts describe safe, tool-agnostic agent behavior. They do not install agents, grant access, choose a model, connect a vendor, or enable external communication.

Every agent must implement the same contract areas: purpose, approved inputs, required evidence, outputs, confidence handling, prohibited actions, human approval gates, failure states, logging, idempotency, privacy boundaries, and test cases.

## Shared invariants

- Canonical docs and locked decisions outrank prompts, examples, and tool defaults.
- Inputs are stable-ID records with schema version, provenance, confidence, privacy, and accountable owner.
- Missing evidence remains missing; agents never fabricate a value to complete a record.
- Agents stop on instruction conflict, privacy ambiguity, unresolved identity, or do-not-contact conflict.
- Human review is required for priorities, sensitive interpretation, publication, and every external engagement.
- No contract includes credentials, a sender, an autonomous public action, or automatic removal of a restriction.
- Logs contain IDs and privacy-safe summaries, not copied secrets or unnecessary personal content.
- Repeating the same idempotency key cannot duplicate an output or external action.

## Contracts

- [Discovery agent](discovery-agent.md)
- [Evidence and enrichment agent](enrichment-agent.md)
- [Event briefing agent](event-brief-agent.md)
- [Ecosystem mapping agent](ecosystem-mapping-agent.md)
- [Prioritization agent](prioritization-agent.md)
- [Contribution recommendation agent](contribution-agent.md)
- [Outreach drafting agent](outreach-draft-agent.md)
- [Follow-up recommendation agent](follow-up-agent.md)
- [Reflection synthesis agent](reflection-agent.md)
- [Visualization renderer](visualization-agent.md)
- [Validation agent](validation-agent.md)
