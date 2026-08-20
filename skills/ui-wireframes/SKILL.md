---
name: ui-wireframes
description: Generate or iterate lo-fi UI wireframes as editable Excalidraw (.excalidraw) files by writing minimal JSON directly. Use when the user asks for a wireframe, UI mockup, UI sketch, screen layout, or a multi-screen flow (e.g. a checkout, wizard, or onboarding) as a discussion basis — trigger phrases include "wireframe", "mockup", "UI-Skizze", "erstelle ein Mockup/Wireframe". Not for high-fidelity visual design.
---

# UI Wireframes

Produce **wireframes**: lo-fi, grayscale, structural. Every control must be visually recognizable as its type — a button reads as a button, a checkbox as a checkbox. Domain-agnostic: works for any application.

Output is a `.excalidraw` file written directly as **minimal JSON**. Excalidraw's restore pipeline defaults every bookkeeping field on open, so you write only the fields in the templates. Never emit canonical export fields (`seed`, `version` on elements, `opacity`, `roughness`, …).

## Workflow

1. **Clarify the screens.** From the request, list the screens, any branches (multiple paths leaving one screen, e.g. a dashboard linking to several pages), and the flow between them. If the request is ambiguous about which screens exist, ask before drawing.
2. **Choose the output path.** Derive it from the prompt's context (an attached file, an open folder, a named location). If unclear, ask the user where to put the file. Suggest a `<name>.excalidraw` filename.
3. **Load references as needed.** Read [references/layout.md](references/layout.md) before placing anything; read [references/controls.md](references/controls.md) for the exact minimal-JSON template of every control you use. Do not invent control geometry from memory.
4. **Write the file** following layout.md arithmetic.
5. **Run the self-check** below before reporting done.
6. Tell the user: open the file with the `pomdtr.excalidraw-editor` VS Code extension (recommended) or drag it onto excalidraw.com — it is fully editable there.

## Iteration

The `.excalidraw` file is **shared state with the human**. Once saved from a canvas, it contains canonical fields and possibly manual edits (colors, freedraw, comments).

- **Never rewrite the whole file.** Read it, then patch surgically: add, modify, or delete only the affected elements.
- Preserve every byte of untouched elements, including canonical fields and user edits.
- New elements you add follow the minimal templates as usual.
- When adding an element, reuse existing IDs where referenced and keep ID style consistent with the file.

## Hard rules (violations break the file)

- Root object: `{"type": "excalidraw", "version": 2, "elements": [...]}`.
- Every element needs `width > 0` and `height > 0` — 0×0 elements are silently deleted on import.
- Text elements need `text`, `fontSize`, and `fontFamily` (5 = Excalifont), plus plausible `width`/`height` estimates.
- Arrow/line points are **relative** to the element's `x`/`y`.
- IDs unique within the file.
- Grayscale only: strokes `#1e1e1e`, fills from the layout.md palette. No color, no branding, no real images.

## Self-check before reporting done

- [ ] Root has `"type": "excalidraw"` and `"version": 2`
- [ ] Every element: `width > 0`, `height > 0`
- [ ] Every text element: `text`, `fontSize`, `fontFamily` present
- [ ] Every arrow/line: `points` present and relative
- [ ] IDs unique
- [ ] Grayscale only
- [ ] Controls recognizable as their type (check against controls.md templates)
- [ ] Every screen label carries its scene number; branching screens follow the layout.md branching rules
- [ ] If iterating: diff contains only intended changes; no untouched element was reformatted

## Token discipline

Minimal JSON costs roughly 80–120 tokens per element. A 5-screen flow should stay under ~8k output tokens. If you catch yourself emitting canonical export fields, stop and use the templates.
