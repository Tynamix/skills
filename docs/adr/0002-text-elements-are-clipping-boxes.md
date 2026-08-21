# 2. Text elements are clipping boxes, not layout boxes

Date: 2026-08-21
Status: Accepted

## Context

Generated wireframes routinely showed labels cut off mid-word: `"Add Jira Data Center"` rendered as `Add Jira Data Cent`, `"Base URL"` as `Base UR`. The skill's heuristic was `width ≈ 8.8 × chars + 10` at fontSize 20 (≈0.44em per character) with the note "prefer slightly too wide over too narrow" — but no explanation of what happens when it is too narrow, so it was treated as cosmetic.

Verification against excalidraw/excalidraw (`restore.ts`, `element/textElement.ts`) showed:

- `autoResize` defaults to `true` on restore and text is **not** re-measured when a file is opened (`refreshDimensions` is off), so the declared `width` survives untouched.
- Excalidraw caches each element in a canvas sized from the element's `width`/`height`. Glyphs are drawn at their true metric width, so anything past the declared width is clipped away. Measured Excalifont advance widths are ≈0.55–0.65em per character — every generated label was between 20% and 40% too narrow.
- The renderer honours `textAlign` on unbound text: `center`/`right` position the glyphs inside the element's own width box.

## Decision

1. Two separate estimates, both rounded up to the 8px grid: **clip width** (`0.8 × fontSize × chars`) is what goes on the text element, **ink width** (`0.65 × fontSize × chars`) is what sizes the surrounding shape and neighbour spacing. Overshooting the clip width is invisible; undershooting is a defect.
2. Centered and right-aligned labels are never positioned by arithmetic. The text element copies its container's `x` and `width` and carries `"textAlign": "center"` (or `"right"`), which removes the estimate from the centering path entirely.

## Consequences

- Text element `width` no longer approximates the rendered text; selection boxes on the canvas look wider than the glyphs until the user edits the text, at which point Excalidraw re-measures.
- Overlapping clip boxes between neighbouring labels are acceptable and expected; collision checks use ink width instead.
- Centered labels gained a required `textAlign` property — a template change across controls.md, layout.md, and the example.
