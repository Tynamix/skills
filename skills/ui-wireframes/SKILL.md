---
name: ui-wireframes
description: Generate or iterate lo-fi UI wireframes as editable Excalidraw (.excalidraw) files by writing minimal JSON directly. Use when the user asks for a wireframe, UI mockup, UI sketch, screen layout, or a multi-screen flow (e.g. a checkout, wizard, or onboarding) as a discussion basis — trigger phrases include "wireframe", "mockup", "UI-Skizze", "erstelle ein Mockup/Wireframe". Not for high-fidelity visual design.
---

# UI Wireframes

Produce **wireframes**: lo-fi, grayscale, structural. Every control must be visually recognizable as its type — a button reads as a button, a checkbox as a checkbox. Domain-agnostic: works for any application.

Output is a `.excalidraw` file written directly as **minimal JSON**. Excalidraw's restore pipeline defaults every bookkeeping field on open, so you write only the fields in the templates. Never emit canonical export fields (`seed`, `version` on elements, `opacity`, `roughness`, …).

## Workflow

1. **Clarify the screens.** From the request, list the screens, any branches (multiple paths leaving one screen, e.g. a dashboard linking to several pages), and the flow between them. If the request is ambiguous about which screens exist, ask before drawing.
2. **Decide the form factor.** Derive it from the request ("mobile view", app context, explicit device names). Default to **desktop** when unspecified and say so in your reply; ask only when both factors are genuinely plausible. A file may mix factors (e.g. a mobile variant in its own row).
3. **Choose the output path.** Derive it from the prompt's context (an attached file, an open folder, a named location). If unclear, ask the user where to put the file. Suggest a `<name>.excalidraw` filename.
4. **Load references as needed.** Read [references/layout.md](references/layout.md) before placing anything; read [references/controls.md](references/controls.md) for the exact minimal-JSON template of every control you use, and for the text sizing rules. Do not invent control geometry or text widths from memory.
5. **Write the file** following layout.md arithmetic, plus `<name>.map.md` beside it (see [references/iteration.md](references/iteration.md)).
6. **Run the self-check** below before reporting done.
7. Tell the user: open the file with the `pomdtr.excalidraw-editor` VS Code extension (recommended) or drag it onto excalidraw.com — it is fully editable there.

## Iteration

The `.excalidraw` file is **shared state with the human**. Once saved from a canvas it contains canonical fields and possibly manual edits (colors, freedraw, comments), and it grows to thousands of lines.

Follow the patch protocol in [references/iteration.md](references/iteration.md): orient on the map file, locate by ID with a text search, read only a window around the hit, patch surgically. Never read or rewrite the whole file; preserve every byte of untouched elements.

Assume the human added or deleted elements between runs. Anything you did not author is theirs: never rename its ID, never delete it without asking, and treat a failed lookup as "deleted", not as "misnamed".

## Hard rules (violations break the file)

- Root object: `{"type": "excalidraw", "version": 2, "elements": [...]}`.
- Every element needs `width > 0` and `height > 0` — 0×0 elements are silently deleted on import.
- Text elements need `text`, `fontSize`, and `fontFamily` (5 = Excalifont). Their `width`/`height` is a **clipping box**: too small and the label is cut off mid-word. Size it from the clip table in controls.md, and center labels with `"textAlign": "center"` over the container's box instead of estimating an offset.
- One element per line in the JSON — the file must stay line-addressable for cheap patching.
- Arrow/line points are **relative** to the element's `x`/`y`.
- IDs unique within the file and greppable (`s2-btn-save`).
- Grayscale only: strokes `#1e1e1e`, fills from the layout.md palette. No color, no branding, no real images.

## Self-check before reporting done

- [ ] Root has `"type": "excalidraw"` and `"version": 2`
- [ ] Every element: `width > 0`, `height > 0`
- [ ] Every text element: `text`, `fontSize`, `fontFamily` present
- [ ] Every text element: `width ≥ clipPerChar × charCount` (controls.md → Text sizing); every centered label carries `"textAlign": "center"` and its container's `x`/`width`
- [ ] Every label's ink width fits inside its container (button, input, badge, cell)
- [ ] Every arrow/line: `points` present and relative
- [ ] Every arrow label fits its gap: `ink(label) + 32 ≤ gap` (layout.md → Flow arrows); the gap is uniform across the file and the label is centered over it, never over a frame
- [ ] IDs unique
- [ ] Grayscale only
- [ ] Controls recognizable as their type (check against controls.md templates)
- [ ] Every screen label carries its scene number; branching screens follow the layout.md branching rules
- [ ] `<name>.map.md` written or updated
- [ ] If iterating: diff contains only intended changes; no untouched element was reformatted; no human-authored element was renamed or removed

## Token discipline

Minimal JSON costs roughly 80–120 tokens per element. A 5-screen flow should stay under ~8k output tokens. If you catch yourself emitting canonical export fields, stop and use the templates.

On an existing file the cost is in _reading_, not writing: a canvas-saved file is ~5× larger and reading it whole dwarfs the edit itself. Use the map + search + window protocol in [references/iteration.md](references/iteration.md).
