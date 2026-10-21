---
name: deployment-diagrams
description: Draw or revise deployment diagrams as editable Excalidraw (.excalidraw) files. Use for cloud infrastructure diagrams, landing zones, Kubernetes topologies, and complex multi-cloud or hybrid architectures on Azure, AWS, and Google Cloud (GCP), including requests for a "Deploymentdiagramm" or "Infrastrukturdiagramm". Supports official provider icons, nested boundaries, and overview/detail views.
---

# Deployment Diagrams

Produce **deployment diagrams**: where workloads run, which boundaries contain them, and how they communicate. Support Azure, AWS, Google Cloud, Kubernetes, and their connections to on-premises or external systems.

Write `.excalidraw` JSON directly, without a DSL, converter, or required runtime. Boundaries, resource cards, labels, and connectors are native editable elements. Official icons are embedded images: individually movable and replaceable, but their internal paths are not editable shapes. The diagram is never a flattened screenshot.

## Workflow

1. **Establish the topology.** Determine whether this is an existing deployment or a proposal, the audience, platforms, and scope. For an existing deployment, inspect the supplied IaC, manifests, documentation, or diagram before drawing. Ask when missing facts would change placement, exposure, connectivity, or redundancy. Mark proposed choices and remaining unknowns explicitly; a reference image supplies visual direction, not evidence of hidden infrastructure.
2. **Choose the deliverable.** Derive the output directory and name from the request or nearby architecture documents; ask if neither supplies a location. Default to one `<name>.excalidraw` containing numbered views, plus a `<name>.map.md` sidecar. For an existing file, follow [references/iteration.md](./references/iteration.md) before reading scene elements.
3. **Model before placing.** Read the relevant platform sections of [references/platforms.md](./references/platforms.md). Inventory resources with stable IDs, product names, roles, containing boundaries, and known location/replica information. Inventory connections with source, destination, direction, purpose, and known protocol. Each resource and connection must be accounted for in a view; containment and communication are different relationships.
4. **Partition and lay out.** Read [references/layout.md](./references/layout.md). Select an overview and, where needed, detail views before assigning coordinates. Every collapsed group in an overview names its detail view. Preserve the requested complexity through decomposition rather than tiny labels or omitted components.
5. **Resolve icons.** Default to official icons using [references/icons.md](./references/icons.md). Reuse suitable supplied icons or retrieve the relevant official set. When an icon cannot be obtained or its permitted use is unclear, use a native card with the exact product name and report the fallback. Icon availability must not block the topology.
6. **Write the scene.** Read [references/excalidraw.md](./references/excalidraw.md) for JSON, text sizing, grouping, and binding templates. Place boundaries behind their contents, then route connections through reserved corridors. Group each resource's card, icon, and labels; bind connectors to the card, not its icon.
7. **Verify the result** using the completion checks below. Correct layout defects before declaring the diagram ready. Write or update the map using [references/iteration.md](./references/iteration.md).
8. **Hand off.** Link the diagram and map, summarize its views, assumptions, and any icon fallbacks. Recommend the `pomdtr.excalidraw-editor` VS Code extension; offer excalidraw.com only when the user is allowed to open the diagram there. Distinguish programmatic validation from a visual check that actually ran.

## Completion checks

- **Coverage:** every requested resource, boundary, and connection appears in the inventory and an appropriate view. Provider product names, placement, protocols, and HA claims agree with the input; unknowns are visible.
- **Structure:** JSON parses; IDs are unique; geometry is finite; shapes, images, and text have positive dimensions; linear elements have at least two distinct points. Every binding and image reference resolves, including reverse `boundElements` entries.
- **Readability:** text fits at the sizes in layout.md; siblings do not overlap; children clear their boundary headers; routes avoid unrelated nodes and labels. Every numbered flow, line style, abbreviation, and detail reference is explained.
- **Portability:** every used icon has a decodable embedded `files` entry, with provenance in the map. Opening the scene needs no local image path or remote icon request.
- **Round-trip:** when a local Excalidraw editor or renderer is available, open the scene and inspect each view at a readable zoom. Check missing icons, clipped text, boundary layering, and arrow direction. Move one resource group in a disposable copy and confirm its labels/icons move together and attached arrow endpoints follow; save and reopen that copy. Keep the deliverable's layout unchanged.
- **Iteration:** changes preserve unrelated human-authored elements and image data; the map reflects affected resources and views. Report any check that could not be performed rather than substituting a claim of success.

## Reference example

[examples/cloud-platforms.excalidraw](./examples/cloud-platforms.excalidraw) is an original, illustrative set of Azure, AWS, Google Cloud, and Kubernetes views. Its [map](./examples/cloud-platforms.map.md) explains the topology, scope, and icon provenance. Use its construction patterns, not its fictional infrastructure, as defaults.
