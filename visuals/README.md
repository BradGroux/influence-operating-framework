# Visual system

The twelve required visuals are maintained as [Mermaid sources](source/), generated [SVG](exports/svg/) and [PNG](exports/png/) exports, [metadata](metadata/), and [accessible descriptions](descriptions/).

## Render

```bash
npm install
npm run render:visuals
```

The renderer uses the pinned Mermaid CLI development dependency, applies [the shared configuration](mermaid-config.json), and rewrites `manifest.json` with SHA-256 hashes for every artifact. Framework users do not need Node.js because rendered exports and descriptions are committed.

## Grammar

- Blue: evidence, records, and contextual inputs.
- Teal: contribution, approved practices, and constructive outputs.
- Amber: human judgment, review, uncertainty, and pause.
- Red: stop, prohibition, unsafe path, and do not contact.
- Solid edge: permitted flow or dependency.
- Dashed edge: optional, reflective, or evidence relationship.

Color is reinforced by labels and never carries meaning alone. Canonical details remain in [the visualization guidance](../docs/14-visualization-system.md).
