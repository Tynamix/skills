# Official icons, embedded and portable

## Source selection

Use a suitable user-supplied or already-local icon first, retaining its known provenance. Otherwise reach the official page for each platform in the diagram and follow its current download links. Archive versions and member names change; inspect the downloaded inventory instead of guessing an asset URL.

| Platform | Authoritative entry point | Selection |
|----------|--------------------------|-----------|
| Azure | [Azure Architecture Center icons](https://learn.microsoft.com/en-us/azure/architecture/icons/) | Official SVG product set; choose the exact product |
| AWS | [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/) | Current architecture/service/resource icon package; match the resource and size variant |
| Google Cloud | [Google Cloud product icons](https://cloud.google.com/icons) | Current core-product set first, category set only for category-level nodes; legacy only when explicitly needed |
| Kubernetes | [Kubernetes community icons](https://github.com/kubernetes/community/tree/main/icons) | Resource and infrastructure icons, preferably unlabeled with native diagram labels |

Check the applicable usage terms, license, and trademark guidance at the source. Permission to use artwork in an architecture diagram is not a blanket license to redistribute an icon library. Embed only the icons used, and record provenance in the map.

Keep official artwork unmodified: preserve colors and aspect ratio, with no cropping, rotation, stretching, or invented vendor lookalikes. Put the product name in an adjacent native text element. A generic cloud or Kubernetes logo cannot stand in for every product/resource kind.

## Retrieval and failure behavior

1. Retrieve only public image packages/files from an official source. Do not send the user's architecture, code, identifiers, or credentials to an icon-search or diagram service.
2. Inspect archive entries before extracting selected images. Reject absolute or parent-traversing paths and symlinks; do not run scripts or installers from an icon pack.
3. Prefer SVG, then PNG. Check SVGs for scripts, event handlers, `foreignObject`, and external image/font/style references. Use a trusted self-contained variant or fall back; diagram opening must not execute code or retrieve remote content.
4. If access fails, terms are unclear, or the exact product icon is missing, draw the native labeled card. Record the specific fallback and reason in the map and handoff. Do not silently substitute another product's icon.

Avoid fetching entire icon catalogs into the target repository. Temporary downloads belong outside it and are removed after the used icons have been embedded and verified.

## Binary-file entries

The root `files` object maps a stable file ID to an image record. Each image element refers to it with `fileId`. Encode the actual bytes programmatically; never invent a base64 string or use a filesystem path as `dataURL`.

For example, with Node's built-in modules, after selecting an SVG or PNG:

```javascript
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";

const bytes = readFileSync(iconPath);
const mimeType = iconPath.endsWith(".svg") ? "image/svg+xml" : "image/png";
const fileId = createHash("sha256").update(bytes).digest("hex");
const entry = {
  id: fileId,
  mimeType,
  dataURL: `data:${mimeType};base64,${bytes.toString("base64")}`,
  created: Date.now(),
};
// Set scene.files[fileId] = entry; image.fileId = fileId.
```

One `files` entry can serve many image elements, including repeated resources in detail views. Verify the decoded MIME type and bytes, positive image dimensions, aspect ratio, and that each image resolves before opening the diagram.

In the map, record file ID, product/resource, official source URL, package member (if any), and usage/license link. The hash identifies the exact bytes; the diagram stays portable without the download. Preserve required notices. On edits, remove an unused entry only after checking references across every view.
