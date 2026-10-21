# Map and surgical iteration

The `.excalidraw` file is shared state with the human and is the source of truth. The `<name>.map.md` sidecar is a compact, rebuildable index, never a second scene definition.

## Map contents

Keep it small enough to read before touching a canvas-saved JSON file:

```markdown
# platform.excalidraw - map

Scope: proposed production deployment. Views 1 and 2 depict the same workload.
Assumptions: zone placement not yet specified.

| View | Prefix | Bounds (x,y,w,h) | Focus / detail references |
|------|--------|------------------|---------------------------|
| 1 | `v1-` | 0,0,1600,960 | Azure network; workload detail in view 2 |
| 2 | `v2-` | 1760,0,1200,960 | Kubernetes logical application |

| Logical resource / boundary | Element IDs or prefix | Parent / notes |
|-----------------------------|-----------------------|----------------|
| orders workload | `v1-orders`, `v2-orders-*` | Same workload, two depictions |
| production VNet | `v1-vnet` | Regional network, not a zone |

| Connections | IDs / prefix | Meaning |
|-------------|--------------|---------|
| API to data | `v1-api-to-db*` | SQL over TLS |

Icons: file ID, product, source URL, package member, usage/license link.
Fallbacks: product and reason, or none.
Validation: structural checks and editor/version actually used; unchecked steps.
```

List resources and boundaries individually when that is needed to locate them; a prefix can cover repeated Pods or a well-described subsystem. Include the legend, numbered continuations, omitted detail, and every overview-to-detail reference.

## Patch protocol

1. **Orient:** read the map and identify affected views/resources/connections. An absent map can be built from a structural inventory of IDs, types, labels, groups, bindings, image IDs, and bounds. Parse locally if convenient, but return only that inventory to context; skip base64 data and bookkeeping.
2. **Locate:** search for all target IDs/labels together, then read bounded windows around matches. Canonical canvas exports spread each element over many lines. Read image payloads only when actually replacing that image.
3. **Reconcile drift:** a missed ID may mean the map is stale. Inspect the relevant view's inventory for renamed/replaced or user-added elements. If the resource is absent or `isDeleted`, do not resurrect it. Ask when the requested change depends on it. Preserve user IDs and unrelated elements.
4. **Patch:** edit only affected properties/element blocks; preserve untouched bytes, existing styles, and canonical fields. For text, update `originalText` if present and recalculate its box. For grouped moves, move all parts and affected scope titles/contents, then repair connector routes and labels.
5. **Maintain references:** adding/removing a connection updates both endpoint cards' `boundElements`. Deleting a resource also removes or retargets incident arrows and their labels, and clears text `containerId`/frame references where applicable. Inspect all views before removing any `files` entry. Duplicate depictions have different element IDs; change only the requested instance unless the change concerns their shared identity.
6. **Validate the affected view and whole-file integrity:** parse JSON, check IDs/bindings/images across the file, and inspect changed layout regions. Update the map's affected rows and validation status. Report known missing resources or unverified checks.

Ask before a change would overwrite human-authored artwork or require a wholesale redraw. For an approved global change, handle one view at a time and preserve shared image records and cross-view identities.
