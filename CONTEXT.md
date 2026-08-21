# Skills

Glossary for the agent skills authored in this repository (skills/) and the conventions around installing third-party skills (.agents/skills/).

## Language

**Wireframe**:
A lo-fi, grayscale structural representation of a UI. Controls must be visually recognizable as their type: a button reads as a button, a checkbox as a checkbox, a label as a label. The deliverable of the ui-wireframes skill.
_Avoid_: Mockup, UI-Skizze

**Mockup**:
A high-fidelity visual design (color, typography, branding). Explicitly out of scope for the wireframe skill; users often say "mockup" when they mean a wireframe — treat it as a trigger alias only, never as the deliverable.
_Avoid_: Design, High-Fidelity-Entwurf

**Screen**:
One page or view inside a wireframe file, drawn as a labeled frame (desktop or mobile size). Screens carry a scene number ("2 · Dashboard"); branch screens use dotted numbers ("2.1 · Reports").
_Avoid_: Scene, Page

**Flow**:
A multi-screen journey shown as several Screens on one canvas, connected by labeled arrows. A Screen may have several outgoing paths (see Branch).
_Avoid_: Journey, Bestellstrecke

**Branch**:
An alternative path departing from a Screen in a Flow (e.g. a dashboard linking to several pages). Branch screens sit on a row below their source Screen and share its number as a dotted prefix (2.1, 2.2).

**Control**:
A recognizable UI element inside a Screen (button, input, checkbox, toggle, …). Controls have named visual states where relevant (e.g. checkbox checked/unchecked).
_Avoid_: Widget, Komponente

**Clip width**:
The `width` written on an Excalidraw text element. It bounds the canvas the glyphs are rendered into, so text beyond it is cut off — it is not a measurement of the text. Always over-estimated (see ADR-0002).
_Avoid_: Text width, Textbreite

**Ink width**:
The width the glyphs of a label actually occupy on screen. Used to size the shape around a label and to space neighbouring text. Distinct from Clip width.

**Map**:
The `<name>.map.md` sidecar next to a wireframe file: a small table of Screens, id prefixes and contents that lets an agent decide what to patch without reading the `.excalidraw` (see ADR-0003). An index, never the source of truth.
_Avoid_: Manifest, Index, Inhaltsverzeichnis
