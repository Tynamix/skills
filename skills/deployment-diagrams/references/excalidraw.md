# Excalidraw scene construction

## Document and geometry

```json
{"type":"excalidraw","version":2,"appState":{"viewBackgroundColor":"#ffffff"},"elements":[],"files":{}}
```

Write one element per line, with blank lines between views. `files` is required when images are used. The restore pipeline supplies bookkeeping fields; omit element `seed`, `version`, `versionNonce`, and timestamps in new elements. Visual fields such as `roughness`, `fillStyle`, and `strokeStyle` are intentional and may be set.

- Use unique, greppable IDs: `v2-orders-api`, `v2-orders-api-label`, `v2-api-to-db`. A repeated resource in another view gets a distinct element ID, with its shared logical identity recorded in the map.
- All coordinates and dimensions must be finite numbers. Rectangles, ellipses, diamonds, images, and text need positive width and height.
- A line/arrow needs at least two distinct points. Points are **relative to its `x`/`y`**, starting at `[0,0]`; negative deltas are valid. `width = max(point.x) - min(point.x)` and similarly for height. A horizontal line may have zero height, a vertical line zero width; reject zero-length lines rather than adding artificial diagonal nudges.
- Layer boundaries outermost first, inner boundaries next, connectors next, resource cards/icons next, and labels last. Place parent fills behind child fills. Use ordinary rectangles for nested scopes; Excalidraw frames are not a general-purpose nested containment model.

## Resource groups and labels

Group a card, its image, and overlay labels using the same `groupIds`. For nested group movement, use `[resourceGroup, innerScopeGroup, outerScopeGroup]` on each resource part. A scope outline and title belong to that scope's group, not a descendant resource group. Internal connections belong to their nearest common ancestor scope; cross-scope connections must not join just one endpoint's group.

Overlay labels keep the icon area free. A group makes the parts move together; it does not make text resize with a card. When resizing, update the card, label boxes, and icon position together.

### Text sizing

Use `fontSize`, `fontFamily: 2`, `lineHeight: 1.25`, and `autoResize: false` explicitly. Wrap long names at word boundaries with `\n`; retain the exact product name across the lines.

For each line, measure its ink with the matching font when a local renderer/canvas is available. Reserve a text box at least `ceil8(maxLineInk + 16)` wide and `ceil8(lineCount * fontSize * 1.25 + 8)` high. Without measurement, conservatively reserve `ceil8(longestLineCharacterCount * fontSize + 16)` width. Enlarge the card or wrap the label if that does not fit.

For centered labels, use the available label area's `x` and `width` with `textAlign: "center"`; do not estimate a centering offset. Keep the entire label box inside the card's padding and outside the icon area.

Existing canvas-authored bound text uses `containerId` and the container's reverse `boundElements` entry. Preserve that convention on edits and change `originalText` along with `text`; do not turn it into an overlay.

## Bound connection template

This fragment contains two grouped cards, their labels, and a horizontal connection. It deliberately has `height: 0` on the arrow.

```json
[
  {"id":"v1-api","type":"rectangle","x":64,"y":96,"width":240,"height":112,"roughness":0,"fillStyle":"solid","backgroundColor":"#ffffff","groupIds":["g-v1-api"],"boundElements":[{"id":"v1-api-to-db","type":"arrow"}]},
  {"id":"v1-api-label","type":"text","x":80,"y":136,"width":208,"height":32,"text":"Orders API","fontSize":16,"fontFamily":2,"lineHeight":1.25,"autoResize":false,"textAlign":"center","groupIds":["g-v1-api"]},
  {"id":"v1-db","type":"rectangle","x":480,"y":96,"width":240,"height":112,"roughness":0,"fillStyle":"solid","backgroundColor":"#ffffff","groupIds":["g-v1-db"],"boundElements":[{"id":"v1-api-to-db","type":"arrow"}]},
  {"id":"v1-db-label","type":"text","x":496,"y":136,"width":208,"height":32,"text":"Database","fontSize":16,"fontFamily":2,"lineHeight":1.25,"autoResize":false,"textAlign":"center","groupIds":["g-v1-db"]},
  {"id":"v1-api-to-db","type":"arrow","x":312,"y":152,"width":160,"height":0,"points":[[0,0],[160,0]],"roughness":0,"strokeColor":"#334155","startArrowhead":null,"endArrowhead":"arrow","startBinding":{"elementId":"v1-api","focus":0,"gap":8,"fixedPoint":[1,0.5],"mode":"orbit"},"endBinding":{"elementId":"v1-db","focus":0,"gap":8,"fixedPoint":[0,0.5],"mode":"orbit"}},
  {"id":"v1-api-to-db-label","type":"text","x":312,"y":112,"width":160,"height":32,"text":"SQL / TLS","fontSize":16,"fontFamily":2,"lineHeight":1.25,"autoResize":false,"textAlign":"center"}
]
```

Bind to the card rectangle and add the arrow's ID to **both** cards' `boundElements`. Only text/arrow relationships belong in `boundElements`; grouping icons is a different operation.

Bindings include legacy `focus`/`gap` for older editors and `fixedPoint`/`mode` for newer ones. For center ports use `focus: 0`, `gap: 8`, `mode: "orbit"` and these normalized fixed points: left `[0,0.5]`, right `[1,0.5]`, top `[0.5,0]`, bottom `[0.5,1]`. Prefer separate center-port routes; verify off-center bindings in the target editor rather than inventing legacy focus values.

For an orthogonal detour, change the points to a route such as `[[0,0],[80,0],[80,160],[240,160]]`, and update dimensions and endpoint bindings. Ordinary multi-point arrows are portable; use `elbowed: true` only after testing the target editor's elbow-routing behavior.

For an attached arrow label, bind text to the arrow with `containerId` and the reverse text entry. For a deliberately positioned corridor label like the template, keep it unbound and update it when the route changes.

## Icons

```json
{"id":"v1-api-icon","type":"image","x":160,"y":104,"width":48,"height":48,"fileId":"icon-content-hash","status":"saved","scale":[1,1],"groupIds":["g-v1-api"]}
```

This is an image-element template, not a complete scene: its `fileId` must resolve in the root `files` table. Allocate a separate label area below it when composing the card. Follow [icons.md](./icons.md) to create the binary-file entry from real image bytes.

## Compatibility references

- [Restore utilities](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils/restore) explain defaulting and binding repair.
- [Element types](https://github.com/excalidraw/excalidraw/blob/master/packages/element/src/types.ts) and [restore implementation](https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/data/restore.ts) are the schema source when a target editor behaves differently.

When debugging compatibility, test a two-card/one-arrow scene and one embedded icon first. Do not regenerate a large human-edited diagram to probe a schema guess.
