# Layout and complexity

## Start with views

One view answers one question: overall deployment, network access, workload internals, availability, or governance. Number views and give each a title and scope. Arrange views left to right, then down, with at least 160px between their bounding boxes. Connect resources within a view; use labeled detail references instead of long arrows between views.

Start a detail view when an overview exceeds roughly **25 resource cards**, needs more than **four nested boundary levels**, or cannot route connections legibly. These are decomposition triggers, not limits on diagram complexity. An overview can collapse a subsystem into a card marked `Detail: view 3`; the detail must retain all inventoried resources and connections. If the user explicitly needs a single dense view, enlarge the canvas and lanes rather than shrinking type.

Separate competing hierarchies: a landing-zone ownership tree can sit above a hub/spoke network view; a Kubernetes workload view can sit beside a node/zone placement view. State what each omits.

## Geometry

- Snap boundaries and cards to an 8px grid. Use 16/24/32px padding, 48px between related groups, and **96px minimum routing corridors** between connected columns.
- Start resource cards at **240 x 112px**. Allow 16px inner padding; grow the card for labels or metadata instead of reducing type. Use identical sizes for equivalent resources.
- Place 40-48px official icons in a reserved area above or beside the text. Preserve aspect ratio; the allocation may be square, but the image need not be.
- Boundary header band: **56px minimum**, enlarged for wrapped titles. Boundary padding: **32px**. Compute each boundary from its children's union plus its header and padding, working inside out.
- Lay out the primary request path left to right. Put asynchronous processing below it and management/observability above it. Use sibling lanes for zones, environments, or independent providers.
- Compute row/column origins from the largest card or boundary in each row/column, not from nominal sizes. Expanded labels must ripple through both containing boundaries and neighboring lanes.

## Type and visual language

Use `fontFamily: 2` (Helvetica) for a compact, technical style and `roughness: 0` for crisp geometry. Use at least **16px** for resource and edge labels, **20px** for boundary headings, and **28px** for view titles. Text sizing and wrapping are specified in [excalidraw.md](./excalidraw.md).

| Meaning | Treatment |
|---------|-----------|
| Resource | White card, dark label, optional provider-colored outline |
| Ownership/location scope | Pale fill, solid thin outline, explicit scope kind |
| Network scope | Pale/transparent fill, dashed outline, explicit VNet/VPC/subnet label |
| Logical scope | Pale/transparent fill, dotted outline, explicit cluster/namespace label |
| Request/data path | Solid dark arrow; purpose and protocol when known |
| Asynchronous flow | Dashed arrow labeled with event/queue/topic |
| Control/telemetry | Dotted arrow labeled `deploys`, `configures`, `metrics`, etc. |
| Replication/failover | Distinct labeled connection stating its actual semantics |

Optional accents: Azure `#0078d4`, AWS `#b45309`, Google Cloud `#4285f4`, Kubernetes `#326ce5`; these are diagram accents, not replacements for official icon artwork. Keep primary text `#1e293b` on light backgrounds. Colors never carry meaning alone. Put a legend for the styles actually used in each independently readable view.

## Route after placement

1. Assign a port on each resource card's left/right/top/bottom edge. Keep arrow endpoints 8px away from the card. Space multiple ports at least 16px apart, or separate flows into views.
2. Reserve corridor tracks at least 24px apart. Use straight segments or explicit right-angle polylines; place the dominant path first, then secondary flows.
3. Route around unrelated cards, icons, labels, and boundary headers. A route may cross the outline of a scope it actually enters; it may not use another resource's interior as a shortcut.
4. Place an edge label beside a long straight segment. The segment must fit the measured label width plus **32px**; allocate extra corridor space for wrapped labels. Keep at least 8px between label ink and the line. A label background may cover its own line, never another connection.
5. Separate fan-out branches and name their destinations. Use two directional arrows when the two directions mean different things. Use a double-headed arrow only for a genuinely symmetric relationship.
6. If crossings remain, reorder siblings or use a numbered continuation (`C1`) at both ends, recorded in the legend and map. A crossing is not a junction; a junction must be intentional and labeled.

Bindings keep endpoints attached when cards move; explicit polyline bends are not an automatic obstacle router. Recheck the affected routes after a move.

## Final visual pass

Inspect each view at readable zoom, not just a fit-all thumbnail. Check long product names, outer padding, repeated resources, all arrowheads, and label collisions. Zooming out can hide clipped text and make a wrongly nested managed service look plausible. Validate topology separately from visual polish.
