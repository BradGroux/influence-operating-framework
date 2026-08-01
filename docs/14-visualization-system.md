# Visualization system

Visuals are maintained framework artifacts, not decoration. They clarify relationships, sequence, hierarchy, or state while equivalent prose remains available.

## Required set

The 0.1.0 baseline includes framework overview, influence lifecycle, ecosystem map, relationship graph model, event intelligence workflow, contribution-before-ask, human-reviewed outreach, reflection and learning loop, measurement model, automation architecture, profile-to-framework relationship, and repository information architecture.

## Visual grammar

- Dark navy background supports consistent dark-theme viewing.
- Blue denotes evidence, records, and contextual inputs.
- Teal denotes contribution, approved practice, and constructive outputs.
- Amber denotes human judgment, review, uncertainty, and pause.
- Red denotes stop, prohibition, do-not-contact, or unsafe paths.
- Solid arrows show permitted flow or dependency.
- Dashed arrows show optional, reflective, or evidence links.
- A node label names a concept; prose explains nuance outside the diagram.

Color is never the only carrier of meaning. Text labels, shapes, and accessible descriptions identify every state.

## Source and export contract

Each visual has:

- one Mermaid `.mmd` source;
- one SVG and one PNG generated from that source;
- one metadata record containing title, concept, source, exports, accessible description, version, and hashes;
- one Markdown description that explains purpose, nodes, edges, reading order, and limits.

The manifest records hashes for sources, exports, metadata, and descriptions. The renderer updates exports and manifest together. Validation fails when an artifact is missing or a checked-in hash is stale.

## Rendering

Mermaid CLI is a pinned development dependency. It is a repository-maintenance tool, not part of the framework semantics. Adopters can read the checked-in exports without Node.js. Maintainers run `npm run render:visuals` after changing source or visual configuration.

## Review

Automated checks confirm presence, format, and synchronization. A human still inspects representative renders for clipped labels, unreadable contrast, misleading direction, color-only meaning, and divergence from canonical prose.
