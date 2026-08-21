# 3. Iterate via a sidecar map, not by reading the wireframe

Date: 2026-08-21
Status: Accepted

## Context

ADR-0001 accepted "reading cost grows after canvas saves (canonical ~5× size); mitigated by patching instead of rewriting and by reading in sections." In practice that mitigation was too weak. Once a user opens a wireframe in Excalidraw and saves it, the file comes back canonical and pretty-printed — roughly 30 lines and ~400 tokens per element, so a five-screen flow is several thousand lines. An agent asked to "rename that button" would read the whole file to find it, spending far more on orientation than on the edit.

Options considered:

- **Read in sections** (status quo): still requires knowing which section, which requires reading.
- **Metadata inside the file**: element-level unknown props and `customData` survive Excalidraw's restore, but retrieving them means reading elements — circular. Unknown *root* keys are dropped on save, so a file-level manifest cannot live in the `.excalidraw`.
- **Regenerate from a compact spec**: a second source of truth that silently discards canvas edits — rejected for the same reason as the DSL in ADR-0001.

## Decision

Ship a sidecar index, `<name>.map.md`, written next to the `.excalidraw`: a table of scene → id prefix → origin → contents, on the order of ten lines.

Iteration follows a fixed protocol (references/iteration.md): orient on the map, locate the element with a single text search by ID or visible label, read only a window around the hit, patch that window, then update the map. The `.excalidraw` stays the single source of truth; the map is an index that may go stale, and a failed lookup means "search wider", never "the element is gone".

Supporting conventions: greppable IDs (`s<scene>-<region>-<name>`, dots in branch scene numbers become `_`) and one element per line so files stay line-addressable.

## Consequences

- Changing one control costs a map read plus one search plus a windowed read, instead of the whole file — roughly two orders of magnitude fewer tokens on a large flow.
- A second file to keep in sync; the skill's self-check enforces it, and staleness degrades to a slower search rather than a wrong edit.
- The map doubles as a human-readable table of contents for the wireframe.
