# 1. Write minimal Excalidraw JSON directly

Date: 2026-08-20
Status: Accepted

## Context

The ui-wireframes skill must produce lo-fi wireframes that are editable on a canvas (Excalidraw). The initial assumption was that Excalidraw's JSON is too verbose to write directly (~410 tokens per labeled button in canonical export form), so a more compact intermediate representation seemed necessary.

Alternatives considered:

- **Compact DSL + converter script**: ~30–50% fewer tokens than minimal JSON, but the generated file stops being the source of truth — canvas edits are lost on regeneration (no round-trip), and every target repo needs a Node toolchain.
- **HTML wireframes**: cheap to generate and preview, but not canvas-editable — violates the core requirement.
- **MCP live-canvas servers** (existing prior art): drive a running canvas via tools; heavy setup, not portable across agents, no artifact-as-file workflow.

Source verification against excalidraw/excalidraw `restore.ts` (master) showed the premise was wrong: the restore pipeline defaults **every** bookkeeping field (`seed`, `version`, `versionNonce`, `updated`, `angle`, `opacity`, `roughness`, fill/stroke styles, `groupIds`, `isDeleted`, …) when missing. Hand-written JSON needs only `type` plus geometry, cutting ~70–80% of tokens (~80–120 per labeled element). Hard constraints discovered: elements with `width === 0 && height === 0` are silently deleted on open; text needs `text`, `fontSize`, `fontFamily`; arrow points are relative.

## Decision

The model writes minimal Excalidraw JSON directly, guided by per-control templates (references/controls.md) and layout arithmetic (references/layout.md). No DSL, no converter, no runtime dependencies. The `.excalidraw` file is the single source of truth; iteration patches it in place and preserves user edits made on the canvas.

## Consequences

- The file survives round-trips: generate → edit on canvas → agent patches surgically.
- The skill is portable: any agent that can write a file can use it; nothing to install in target repos.
- Template maintenance is the ongoing cost: new controls are added to controls.md; the composition rule covers gaps in the meantime.
- Reading cost grows after canvas saves (canonical ~5× size); mitigated by patching instead of rewriting and by reading in sections.
