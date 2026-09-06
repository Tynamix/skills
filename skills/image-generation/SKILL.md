---
name: image-generation
description: Generate or edit images and web assets (hero images, backgrounds, illustrations, icons, logos) with OpenAI's gpt-image-2 API. Use when asked to generate/create an image, icon, logo, hero image, background, or asset for a website or app ("Bild generieren", "Icon erstellen"), or to edit/modify an existing image. Requires the OPENAI_API_KEY environment variable.
---

# Image Generation

Generate or edit web assets via the OpenAI `gpt-image-2` API. All logic lives in `scripts/generate.py` (Python 3, stdlib only) — one command per call, identical on macOS, Linux, and Windows.

## Prerequisite

`OPENAI_API_KEY` must be set in the environment. If it is missing, tell the user to set it and stop there.

## Workflow

1. Derive the parameters from the request using the tables below. Defaults: `quality=medium`, `format=webp`, `background=auto`, `size=1024x1024`.
2. Announce one line before the call — prompt, size, quality, target path — then run immediately. The user asked for the image; a confirmation round only adds latency.
3. Run the script (path relative to this skill's folder):
   - Generate: `python3 scripts/generate.py generate --prompt "<description>" --out <path> [--size WxH] [--quality low|medium|high] [--format png|jpeg|webp] [--background transparent|opaque|auto]`
   - Edit: `python3 scripts/generate.py edit --prompt "<what to change>" --image <file> [--image <file> …] --out <path> [same options as generate, except --background]`
4. Done when the script printed the saved path(s). Verify the file exists and report the path to the user.

## Sizes by purpose

| Purpose | Size |
| --- | --- |
| Hero image, page background | `1536x1024` |
| Icon, logo, avatar | `1024x1024` |
| Illustration, texture | `1024x1024` |
| Arbitrary | `WIDTHxHEIGHT`, both divisible by 16, aspect ratio 1:3 to 3:1, max `3840x2160` |

## Parameter rules

- Transparent background (icons, logos, anything to layer over a surface): `--background transparent --format png`. Everything else: `--format webp`.
- `--quality high` only when explicitly requested or for a final hero image — it is the cost lever.
- Target path comes from the request; otherwise a directory with trailing slash (e.g. `assets/`) — the script derives a kebab-case filename from the prompt.
- Write the prompt for an image model, not a chat model: subject, style, composition, color palette, and the surrounding context ("flat vector icon, single color on transparent background, no text").
