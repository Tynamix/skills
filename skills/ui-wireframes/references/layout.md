# Layout arithmetic

## Grid & spacing

- Everything snaps to the **8px grid**: all `x`, `y`, `width`, `height` are multiples of 8 (exception: 4px nudges for checkmarks/chevrons inside a control).
- Spacing scale: **8 / 16 / 24 / 32 / 48**. Inner padding of containers: 24. Between related elements: 8–16. Between sections: 32–48.
- Prefer uniform gaps over pixel-perfect art: same gap everywhere reads as intentional.

## Palette (grayscale only)

| Use                                                  | Hex       |
|------------------------------------------------------|-----------|
| Strokes, primary text                                | `#1e1e1e` |
| Secondary text, placeholders, inactive               | `#868e96` |
| Subtle fill (nav bar, table header)                  | `#f1f3f5` |
| Placeholder fill (images), toggle off                | `#e9ecef` |
| Avatar fill                                          | `#ced4da` |
| Primary action fill (button, toggle on, active step) | `#343a40` |
| Surface (screen, card, input)                        | `#ffffff` |

## Screens

- Desktop frame: **1440×900**. Mobile frame: **390×844**. Frame fill `#ffffff`.
- Screen label: 16px gray (`#868e96`) text **above** the frame at `(frame.x, frame.y − 28)`, formatted `"<number> · <name>"` — see Branching flows.
- Arrange screens **left → right** with a **uniform horizontal gap**: 160px by default, widened for the whole file when an arrow label needs it (see Flow arrows). Same value for mobile — consistency beats platform aesthetics.
- After **4 screens**, wrap to a new row: `y += 900 + 200` (or 844 + 200 for mobile), restart `x` at the first screen's `x`.
- First screen starts at a round origin like (0, 0).

## Flow arrows

- Connect screens in reading order: plain `arrow` from right edge of screen A (mid-height) to left edge of screen B, e.g. `{"id":"a1","type":"arrow","x":1440,"y":450,"points":[[0,0],[160,0]]}`.
- 16px gray (`#868e96`) label above the arrow naming the trigger ("click Continue"). Required when a screen has more than one outgoing arrow, optional otherwise.
- No `startBinding`/`endBinding` — unbound arrows are intentional (cheaper, and restore repairs them to null).
### Write the labels first, then size the gap

A label that is wider than its gap spills over the neighbouring frame — the second most common defect after clipped text. The gap follows the labels, never the other way round.

1. Write down every horizontal arrow label before placing screens.
2. For each, `neededGap = ink(label) + 32` (ink per char from controls.md → Text sizing; 16px text ≈ 10px/char, so 160px holds ~12 characters — `"click Continue"` already needs 176).
3. `gap = max(160, largest neededGap in the file)`, rounded up to a multiple of 8, and used for **every** horizontal gap. Compute all screen `x` values from that gap before writing any element.
4. Arrow `points` span the same `gap`: `[[0,0],[gap,0]]`.

Place the label with the centering trick instead of an offset: `x = arrow.x`, `width = gap`, `"textAlign": "center"`, `y = arrow.y − 28`.

If a label would push the gap past ~280px, shorten it to verb + object ("Add integration tool from the catalog" → "Add tool") or stack it as two text elements at `y − 52` and `y − 28`, each centered over the gap and each sized by its own `neededGap`.

## Branching flows

A screen can have **several outgoing paths** (e.g. a dashboard linking to different pages). Numbers give every screen a stable reference; the arrows express the topology.

- **Scene numbers**: main path = 1, 2, 3… The branch row of screen N holds its destinations as N.1, N.2… left→right — whether they are alternative destinations or linear continuations. Deeper nesting recurses (branches of 2.3 → 2.3.1, 2.3.2).
- **Placement**: the branch row of screen S sits **below S's row** (`y = S.y + frameHeight + 200`), starting at `S.x`, extending right with the normal 160px gap. If several screens on one row branch, their branch rows stack in the reading order of their source screens.
- **Branch arrows**: one labeled arrow per outgoing path. Vertical from S's bottom edge to the branch screen's top edge, x aligned to the branch's center: `{"type":"arrow","x":<branchCenterX>,"y":<S.y+900>,"points":[[0,0],[0,200]]}`. If the branch screen sits beyond S's right edge, use a single-bend elbow from S's right edge: `"points":[[0,0],[dx,0],[dx,dy]]`. Never route an arrow across a screen frame.
- **Branch arrow labels**: the 200px band between rows is empty, so the label may be wider than the gap between screens. Center it on the arrow: `width = max(160, ink + 32)`, `x = arrow.x − width / 2`, `"textAlign": "center"`, `y = arrow.y + 88`. Keep neighbouring branch labels ≥ 16px apart; if two collide, shorten them rather than moving them off their arrows.
- On an **elbow** arrow, label the horizontal leg: `x = arrow.x`, `width = dx`, centered, `y = arrow.y − 28` — and treat `dx` like a gap, i.e. it must satisfy `dx ≥ ink + 32`.

## Labels on shapes

A label centered in a shape is **not** positioned by arithmetic on the text width — that estimate is exactly what produces clipped labels. Give the text element the shape's `x` and `width` and set `"textAlign": "center"`:

`label.x = shape.x`, `label.width = shape.width`, `label.y = shape.y + (shape.height − textHeight) / 2`

Left-aligned text inside a container sits at `container.x + padding` and needs the clip-width estimate from controls.md → Text sizing. No `containerId` binding — overlay is the convention.

## Common content regions (desktop)

- Nav bar: y = 0..64 (see controls.md).
- Page title: y = 104 (nav 64 + 40 gap).
- Content area: y = 160..860, x = 96..1344 (96px side margins) — or a 2-column split at x = 96 / x = 736 with 48 gutter.
- Footer: y = 860.

## Common content regions (mobile, 390×844)

- Status / top bar: y = 0..48 — title 20px centered at y = 12, optional back chevron or action text at the edges (x = 16 / right-aligned).
- Content: single column, 16px side margins (x = 16..374). Inputs, buttons and selects span the full content width (358).
- Vertical rhythm: title 24px at y = 64; sections separated by 24–32; form fields label(20) + 8 + input(44) + 16.
- Tab bar: y = 780..844 (see controls.md). With a tab bar, content ends at y = 772.
- Sticky bottom CTA: button at y = 772, height 48, width 358 (see controls.md).
- Bottom sheet: anchored to the bottom edge (see controls.md).

## Canvas hygiene

- Keep all screens' frames non-overlapping; arrows and their labels live in the gaps, and no label ink may cross a frame edge.
- IDs: short, readable, unique, and **greppable** — `s2-nav-logo`, `s2-form-email-input`, `s2-btn-save`. Pattern: `s<scene>-<region>-<name>[-part]`, where `<scene>` matches the screen's scene number with dots replaced by `_` (`s2_1-…`). Iteration finds elements by ID with a text search instead of reading the file (see [iteration.md](iteration.md)), so a guessable ID is worth more than a short one.
- One element per line in the JSON, screens separated by a blank line. Line-addressable files can be patched line by line.
