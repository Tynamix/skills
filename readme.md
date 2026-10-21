# Skills

A collection of agent skills, authored in this repository and pulled in from third-party sources.

Skills are instructions that an AI agent reads to perform a specific kind of work. Each skill is a directory with a `SKILL.md` (and, where needed, reference files) that walks the agent through a workflow, its conventions, and its hard rules.

## Layout

```
skills/                     # skills authored in this repo
  deployment-diagrams/      # cloud and Kubernetes deployments in Excalidraw
    SKILL.md
    references/             # platform semantics, layout, icons, JSON, iteration
    examples/               # editable multi-view example + its sidecar map
  ui-wireframes/            # lo-fi UI wireframes as editable Excalidraw files
    SKILL.md
    references/             # templates, layout arithmetic, iteration protocol
    examples/               # a generated wireframe + its sidecar map
.agents/skills/             # third-party skills installed via `npx skills`
docs/
  adr/                      # architecture decision records
  agents/                   # agent-facing conventions (domain, issue tracker, triage)
skills-lock.json            # lockfile for installed third-party skills
CONTEXT.md                  # glossary of the repo's domain vocabulary
AGENTS.md                   # entry points for agents working in this repo
```

## `ui-wireframes`

The repo's flagship skill. It generates **lo-fi, grayscale wireframes** as editable
[Excalidraw](https://excalidraw.com) `.excalidraw` files by writing **minimal JSON** directly —
no DSL, no converter, no runtime dependencies. The file is the single source of truth and
survives round-trips: generate → edit on canvas → patch surgically.

Key design decisions are recorded as ADRs:

- **ADR-0001** — Write minimal Excalidraw JSON directly (Excalidraw's restore pipeline defaults
  every bookkeeping field, so hand-written files need only `type` plus geometry).
- **ADR-0002** — Text elements are *clipping boxes*, not layout boxes. Clip width and ink width
  are computed separately, and centered labels never use arithmetic positioning.
- **ADR-0003** — Iterate via a sidecar `<name>.map.md` index rather than reading the whole file,
  which keeps patches token-cheap after the canvas pretty-prints the file.

See [skills/ui-wireframes/SKILL.md](skills/ui-wireframes/SKILL.md) for the full workflow, and
[skills/ui-wireframes/examples/](skills/ui-wireframes/examples/) for a generated wireframe and its map.

## `deployment-diagrams`

Draws **editable deployment diagrams** for Azure, AWS, Google Cloud, Kubernetes, and
hybrid/multi-cloud systems. Like `ui-wireframes`, it writes Excalidraw JSON directly and
preserves canvas edits through a sidecar map and surgical patches.

- Official provider/resource icons are embedded in the file, with provenance and usage
  terms recorded in the map. When unavailable, explicitly reported native labeled cards
  keep the diagram usable. No icon library or converter is required in the target repo.
- Ownership, region/zone, network, and orchestration boundaries remain distinct.
- Numbered overview/detail views, reserved routing corridors, and readable type support
  complex landing zones and cluster topologies without flattening them into an image.
- Resource groups and bound arrow endpoints remain editable. Icon artwork itself is an
  embedded image, not a collection of editable vector paths.

Example requests: "Draw our Azure landing zone in Excalidraw", "Create an AWS multi-AZ
deployment diagram", or "Zeichne ein Deploymentdiagramm fuer GKE mit Kubernetes-Detailansicht".

See [skills/deployment-diagrams/SKILL.md](skills/deployment-diagrams/SKILL.md) and the
[multi-view example](skills/deployment-diagrams/examples/cloud-platforms.excalidraw) with its
[map](skills/deployment-diagrams/examples/cloud-platforms.map.md).

## Domain vocabulary

This repo maintains a controlled glossary in [CONTEXT.md](CONTEXT.md). When agent output names a
concept — in an issue title, a proposal, a test name — it should use the glossary term (e.g. a
*wireframe* is lo-fi and structural, never a *mockup*). Terms are defined and ADRs recorded
lazily via the `domain-modeling` skill; see [docs/agents/domain.md](docs/agents/domain.md).

## Issue tracker & triage

Issues and specs are local markdown files under `.scratch/<feature>/` rather than a hosted tracker.
Five canonical triage roles map to label strings; see
[docs/agents/issue-tracker.md](docs/agents/issue-tracker.md) and
[docs/agents/triage-labels.md](docs/agents/triage-labels.md).

## Installing third-party skills

Third-party skills (e.g. `mattpocock/skills`) are installed with:

```bash
npx skills@latest add tynamix/skills
```

The installed skills live under `.agents/skills/` and are recorded in `skills-lock.json`.
