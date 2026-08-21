# Iterating on an existing wireframe

The first version is cheap to write. Every version after that is expensive to *read* — once the file has been opened and saved on a canvas, Excalidraw rewrites it in canonical form: every bookkeeping field present, one property per line, roughly 30 lines and ~400 tokens per element. A 5-screen flow becomes several thousand lines. Reading it whole to change one label is the failure mode this page prevents.

**Two rules that follow from that:**

- Never read the whole file. Never rewrite the whole file.
- Locating and changing one control should cost well under ~500 tokens of reading.

## The map (sidecar index)

Write `<name>.map.md` next to the `.excalidraw` when you create the wireframe, and keep it current with every patch. It is the cheap index that replaces reading the JSON:

```md
# checkout.excalidraw — map

desktop 1440×900 · ids `s<scene>-<region>-<name>`

| scene                | id prefix | origin    | contents                                 |
|----------------------|-----------|-----------|------------------------------------------|
| 1 · Cart             | `s1-`     | 0,0       | nav, table (3 rows), btn-checkout        |
| 2 · Address          | `s2-`     | 1600,0    | nav, form (name, street, city), btn-next |
| 2.1 · Payment failed | `s2_1-`   | 1600,1100 | modal, toast-error                       |
```

The map says *what exists and what it is called*. The `.excalidraw` remains the single source of truth — the map is a hint that can go stale when the human edits on canvas, so a failed lookup means "search wider", never "the element is gone".

If a file has no map (older file, or one you did not create), build one from a single search for `"text"` in the `.excalidraw`: one hit per label is enough to reconstruct the screen inventory, and it costs a fraction of reading the file.

## Patch protocol

1. **Orient** — read the map, not the JSON. Decide which elements the request touches.
2. **Locate** — one text search in the `.excalidraw` for the element ID (`s2-btn-next`) or, if the ID is unknown, for the visible label (`"text": "Continue"`). Search for all targets at once with alternation: `s2-btn-next|s2-btn-back`.
3. **Window** — read only the hit's surroundings (±30 lines in canonical form, ±3 lines in minimal form). Never widen to "get context" for elements you are not changing.
4. **Patch** — string-replace inside that window, touching only the properties that must change (`x`, `y`, `width`, `text`, `backgroundColor`, …). Do not re-emit an element you only meant to move, and do not reformat canonical fields back to minimal form.
5. **Add** — new elements go right after the last element of their screen (same search, last hit for that prefix), written from the minimal templates, with IDs that follow the file's convention.
6. **Delete** — remove the element *and its parts* (search the shared ID prefix: a checkbox has `-cb`, `-cbk1`, `-cbk2`). If anything references it via `boundElements` or `containerId`, clear that reference too.
7. **Sync the map** — only when a screen, control group, or ID prefix changed.
8. **Verify** — one targeted search for the changed ID. Do not re-read the file to "check the result".

## When the human added or deleted things on the canvas

Assume they did. The map is an index of what *you* wrote; the canvas is theirs too. The protocol is built so drift shows up as a failed lookup, not as a wrong edit.

**Deleted.** A saved `.excalidraw` no longer contains what the human erased (deleted elements are filtered out on export; a host that keeps them marks `"isDeleted": true` — treat both as gone). So a search that finds nothing means *deleted*, not *misnamed*: do not resurrect it, drop it from the map, and mention it in your reply ("`s2-btn-back` no longer exists — I left it out"). If the request depended on it, ask instead of re-creating it.

**Added.** Canvas-drawn elements carry random 20-character IDs, full canonical fields, and possibly colors, freedraw strokes or bound text. Rules:

- Never rename their IDs — bindings (`boundElements`, `containerId`, `frameId`) reference them.
- Never delete or "clean up" what you did not author. If the request would move, overwrite, or collide with one of them, say so and ask.
- Assign them to a screen by comparing their `x`/`y` to the screen origins in the map, and record them there with their real ID, e.g. `+ btn "Cancel" (user, kX9dLm2…)`. Reference them by ID or by their label text afterwards.

**Bound text** is the usual shape of a human-added label: double-clicking a rectangle produces a text element with `containerId`, and the container gains a `boundElements` entry. Do not convert it to this skill's overlay convention. To change it, patch `text` **and** `originalText`, keep `width ≤ container.width − 10` (bound text uses 5px padding per side), and delete the pair together.

**Re-sync** when an ID lookup fails, when the request targets a whole screen or region rather than a named control, or when the user says they changed something. One search for `"text"` across the file lists every label with its line number — enough to rebuild the inventory and spot additions, at a fraction of the cost of reading the file. Shapes without labels stay invisible to that search; if the user says "I drew something there", read that screen's region once and update the map.

## Layout ripples

Moving or resizing one control usually shifts its neighbours below it. Do not re-read the screen to find them: the map plus the layout rhythm from [layout.md](layout.md) tell you which IDs sit below, and each one is a `+Δy` on a single line. Patch them in the same pass.

## When the request is genuinely global

"Make every screen mobile" or "replace the whole flow" touches everything. Say so, then regenerate **one screen at a time** — locate the screen's first and last element, replace that block, move on — so no single step holds the whole file in context. Warn the user that a full regeneration drops manual canvas edits, and get confirmation first.
