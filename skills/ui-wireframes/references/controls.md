# Controls — minimal Excalidraw JSON templates

One template per control, built from five primitives: `rectangle`, `ellipse`, `diamond`, `text`, `line`, `arrow`. Copy a template, set `x`/`y` (and text), adjust `width`/`height` per the sizing rules. Coordinates below assume origin (0,0) — translate everything by your target origin.

Rounding: rectangles default to sharp corners; add `"roundness": {"type": 3}` where the template says rounded.

---

## Text sizing (read before writing any text element)

A text element's `width`/`height` is a **clipping box**, not a layout box. Excalidraw draws the glyphs at their real metric width but caches the element in a canvas of exactly `width × height`, so anything beyond gets **cut off mid-word** (`"Add Jira Data Center"` → `Add Jira Data Cent`). This is the most common defect in generated wireframes. Too wide costs nothing visually; too narrow is broken.

Two estimates for Excalifont, both rounded **up** to the next multiple of 8:

| fontSize | `height` (line height) | **ink** per char — size containers with this | **clip** per char — the text element's `width` |
|----------|------------------------|----------------------------------------------|------------------------------------------------|
| 12       | 15                     | 8                                            | 10                                             |
| 16       | 20                     | 10                                           | 13                                             |
| 20       | 25                     | 13                                           | 16                                             |
| 28       | 35                     | 18                                           | 23                                             |

- `width = clipPerChar × charCount`, minimum 24. Count every character, spaces and punctuation included.
- `ink = inkPerChar × charCount` approximates what is actually drawn — use it to size the shape around a label and to check that neighbouring text does not collide.
- Other font sizes: `clipPerChar = 0.8 × fontSize`, `inkPerChar = 0.65 × fontSize`, `height = 1.25 × fontSize`.
- One text element per line. Never put `\n` in `text`; if you do, `height = lines × lineHeight`.

### Centered and right-aligned labels — never estimate

For a label centered in a shape, do not compute an offset. Give the text element the **shape's `x` and `width`** and set `"textAlign": "center"` — Excalidraw centers the glyphs inside that box, so the estimate cannot be wrong:

`label.x = shape.x`, `label.width = shape.width`, `label.y = shape.y + (shape.height − textHeight) / 2`

Right-aligned: same box, `"textAlign": "right"`. Only left-aligned text (`x = container.x + padding`) needs the clip estimate.

Keep `shape.width ≥ ink + 2 × padding`, otherwise the label clips at the shape's edge.

---

## Text primitives

**Screen title** (28px): `{"id":"t1","type":"text","x":0,"y":0,"width":208,"height":35,"text":"Dashboard","fontSize":28,"fontFamily":5}` (9 chars × 23 = 207 → 208)

**Body / paragraph line** (16px, gray): `{"id":"t2","type":"text","x":0,"y":0,"width":280,"height":20,"text":"Some descriptive text","fontSize":16,"fontFamily":5,"strokeColor":"#868e96"}` (21 chars × 13 = 273 → 280)

**Link** (16px, underlined): body text plus `"textDecoration": "underline"` — if in doubt, body text + a `line` 2px below it, width = the text's ink width.

---

## Actions

**Button — primary** (dark fill, white centered label):

```json
{"id":"b1","type":"rectangle","x":0,"y":0,"width":152,"height":44,"backgroundColor":"#343a40","roundness":{"type":3}},
{"id":"b1l","type":"text","x":0,"y":10,"width":152,"height":25,"text":"Continue","fontSize":20,"fontFamily":5,"textAlign":"center","strokeColor":"#ffffff"}
```

**Button — secondary**: same, but `backgroundColor` `transparent`, label `strokeColor` `#1e1e1e`.

Sizing: `width = ink + 48` (24 padding each side, e.g. "Continue" = 8 × 13 = 104 → 152), minimum 120, height 44. The label box mirrors the button box exactly (`x`, `width`) and is centered vertically at `btn.y + 10`.

---

## Form controls

**Input** (with 16px placeholder in gray):

```json
{"id":"i1","type":"rectangle","x":0,"y":0,"width":280,"height":44,"backgroundColor":"#ffffff","roundness":{"type":3}},
{"id":"i1p","type":"text","x":12,"y":12,"width":176,"height":20,"text":"Email address","fontSize":16,"fontFamily":5,"strokeColor":"#868e96"}
```

The placeholder box may extend past the input's right edge in the JSON — harmless, since the clip box is invisible. But keep the *ink* inside the input: `input.width ≥ ink + 24`.

**Textarea**: input with height 120 and the placeholder top-left (`y + 12`).

**Select**: input shape, placeholder left, plus a chevron — two short lines forming a "v" at the right edge:

```json
{"id":"s1c1","type":"line","x":246,"y":18,"points":[[0,0],[8,8]]},
{"id":"s1c2","type":"line","x":254,"y":26,"points":[[0,0],[8,-8]]}
```

**Checkbox — off**: `{"id":"c1","type":"rectangle","x":0,"y":0,"width":22,"height":22,"backgroundColor":"#ffffff","roundness":{"type":3}}` + optional 16px label text at `x + 32`.

**Checkbox — on**: box plus checkmark, two lines:

```json
{"id":"c1k1","type":"line","x":4,"y":11,"points":[[0,0],[5,6]]},
{"id":"c1k2","type":"line","x":9,"y":17,"points":[[0,0],[9,-12]]}
```

**Radio — off**: `{"id":"r1","type":"ellipse","x":0,"y":0,"width":22,"height":22,"backgroundColor":"#ffffff"}` + label as checkbox.

**Radio — on**: add inner dot `{"id":"r1d","type":"ellipse","x":6,"y":6,"width":10,"height":10,"backgroundColor":"#343a40"}`.

**Toggle — off**: pill + knob left:

```json
{"id":"tg1","type":"rectangle","x":0,"y":0,"width":48,"height":26,"backgroundColor":"#e9ecef","roundness":{"type":3}},
{"id":"tg1k","type":"ellipse","x":4,"y":4,"width":18,"height":18,"backgroundColor":"#ffffff"}
```

**Toggle — on**: pill `backgroundColor` `#343a40`, knob at `x + 26`.

**Slider**: track line + knob: `{"id":"sl1","type":"line","x":0,"y":13,"points":[[0,0],[200,0]],"strokeWidth":4}` + ellipse knob (18×18) centered on the track at the value position.

---

## Structure & navigation

**Screen frame**: `{"id":"f1","type":"rectangle","x":0,"y":0,"width":1440,"height":900,"backgroundColor":"#ffffff"}` + screen label as 16px gray text at `x`, `y - 28`, formatted `"<number> · <name>"` (see layout.md → Branching flows). Mobile: 390×844.

**Nav bar**: rectangle full screen width × 64, fill `#f1f3f5`; logo placeholder left (small dark square 32×32 or short bold text), links as 16px text, next link starts at `previous.x + ink + 32`.

**Tabs**: row of 16px labels, next label at `previous.x + ink + 24`; the active tab gets a `line` underline (width = its ink width, y = label.y + 24), inactive tabs gray `#868e96`.

**Breadcrumb**: 16px labels joined by `" / "` text separators, all gray except last segment dark.

**Pagination**: row of 28×28 rounded squares (fill `#f1f3f5`, active `#343a40` with white number), 8 apart, each with a 16px digit as a centered label (text box = square box, `"textAlign":"center"`).

**Card**: `backgroundColor` `#ffffff`, `"roundness":{"type":3}`, padding 24 inside; typical size 320×200.

**Modal**: dim backdrop = full-screen rectangle `backgroundColor` `#1e1e1e`, `strokeColor` `transparent`, `"opacity": 40`; dialog = centered white rounded rectangle (e.g. 480×320) with title (20px), body, and a button row.

**Table**: header row rectangle (height 48, fill `#f1f3f5`) with bold-ish 16px column labels; body rows 48 high separated by horizontal lines; cell text 16px left-aligned at `cell.x + 16`, `row.y + 14`.

**List**: stacked rows (height 56) separated by lines; optional avatar + two text lines per row.

**Badge**: small rounded rectangle (height 22, fill `#e9ecef`, `width = ink(12px) + 24`) with 12px dark text as a centered label (text box = badge box).

**Toast**: rounded dark rectangle (`#343a40`, height 48, `width = ink(16px) + 48`, minimum 320) with white 16px text as a centered label, typically bottom-center of a screen.

**Tooltip**: small dark rounded rectangle with white 12px text, placed above its target.

**Avatar**: `ellipse` 40×40, fill `#ced4da`.

**Icon placeholder**: 24×24 square, `strokeStyle` `"dashed"`, transparent fill.

**Image placeholder**: rectangle fill `#e9ecef` plus the diagonal cross:

```json
{"id":"p1x1","type":"line","x":0,"y":0,"points":[[0,0],[W,H]]},
{"id":"p1x2","type":"line","x":0,"y":H,"points":[[0,0],[W,-H]]}
```

**Stepper** (multi-step progress): circles 32×32 per step, each with its number as a centered label (text box = circle box); a 16px caption beneath each, also centered on the circle box but widened symmetrically (`x = circle.x − (w − 32) / 2`) so long captions are not clipped. Done steps: fill `#343a40`, white number; current: white fill, thick ring (`"strokeWidth": 4`); upcoming: fill `#e9ecef`, gray number. Connect circles with horizontal lines between circle edges.

---

## Mobile patterns

**Tab bar** (bottom, 390 wide): rectangle at `(frame.x, frame.y + 780)`, width 390, height 64, fill `#f1f3f5`. Four items, each an 80-wide slot at x offsets 8/88/168/248 (add 328 for five): a 24×24 dashed icon placeholder at `item.x + 28, bar.y + 8`, and a 12px label beneath at `bar.y + 36` as a centered label over the 80-wide slot. Active item: dark icon border + dark label; inactive: gray `#868e96`.

**Sticky bottom CTA**: primary button (see Actions) at `(frame.x + 16, frame.y + 772)`, width 358, height 48.

**Bottom sheet**: dim backdrop like Modal; sheet = rounded rectangle width 390 (full frame width) anchored at the bottom edge, height ≈ 320 (`y = frame.y + 524`), with a grabber: 40×4 line-equivalent (small rounded rect 40×4, fill `#ced4da`) centered at `sheet.y + 12`. Content: title 20px at `sheet.y + 32`, rows or buttons below.

**List row with chevron** (mobile settings-style): row height 56, 16px label at left (`x + 16, row.y + 18`), optional 16px gray value right-aligned, chevron at the right edge: `{"type":"line","x":frame.x+354,"y":row.y+20,"points":[[0,0],[8,8]]}` + `{"type":"line","x":frame.x+362,"y":row.y+28,"points":[[0,0],[-8,8]]}`. Rows separated by full-width lines.

---

## Composition rule (extensibility)

If a control you need is missing: compose it from the primitives in this file's **style** — 1px-look strokes (`strokeWidth` 2 default is fine), grayscale palette from layout.md, 8px grid, overlay text labels. Then tell the user the control was improvised and is missing upstream in the skill, so it can be added to this file.
