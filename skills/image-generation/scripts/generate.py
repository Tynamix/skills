#!/usr/bin/env python3
"""Generate or edit images with the OpenAI gpt-image-2 API.

Stdlib only. Reads OPENAI_API_KEY from the environment.

Usage:
  generate.py generate --prompt "..." --out assets/ [--size WxH] [--quality ...]
                       [--format png|jpeg|webp] [--background ...] [--n N]
  generate.py edit --prompt "..." --image a.png [--image b.png ...] --out assets/
                   [--size WxH] [--quality ...] [--format ...] [--n N]
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
import uuid

API_URL = "https://api.openai.com/v1/images/generations"
API_URL_EDITS = "https://api.openai.com/v1/images/edits"
MODEL = "gpt-image-2"


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:60] or "image"


def build_out_path(out: str, prompt: str, ext: str, index: int, total: int) -> str:
    """Accepts a directory (trailing slash or existing dir) or a file path."""
    if out.endswith(os.sep) or out.endswith("/") or os.path.isdir(out):
        os.makedirs(out, exist_ok=True)
        name = slugify(prompt)
        if total > 1:
            name = f"{name}-{index}"
        return os.path.join(out, f"{name}.{ext}")
    parent = os.path.dirname(os.path.abspath(out))
    os.makedirs(parent, exist_ok=True)
    if total > 1 and index > 1:
        base, old_ext = os.path.splitext(out)
        return f"{base}-{index}{old_ext}"
    return out


def post_json(url: str, payload: dict, api_key: str) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
            msg = body.get("error", {}).get("message", str(body))
        except Exception:
            msg = str(e)
        die(f"API returned {e.code}: {msg}")
    except urllib.error.URLError as e:
        die(f"request failed: {e.reason}")


def post_multipart(url: str, fields: dict, files: list, api_key: str) -> dict:
    boundary = f"----skill-{uuid.uuid4().hex}"
    parts = []
    for name, value in fields.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"'
            f"\r\n\r\n{value}\r\n".encode()
        )
    for name, path, content_type in files:
        with open(path, "rb") as f:
            content = f.read()
        parts.append(
            (
                f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; '
                f'filename="{os.path.basename(path)}"\r\n'
                f"Content-Type: {content_type}\r\n\r\n"
            ).encode()
            + content
            + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
            msg = body.get("error", {}).get("message", str(body))
        except Exception:
            msg = str(e)
        die(f"API returned {e.code}: {msg}")
    except urllib.error.URLError as e:
        die(f"request failed: {e.reason}")


def save_images(resp: dict, out: str, prompt: str, ext: str) -> list:
    paths = []
    items = resp.get("data", [])
    if not items:
        die("API returned no images")
    for i, item in enumerate(items, start=1):
        b64 = item.get("b64_json")
        if not b64:
            die("API returned no b64_json data (url responses are not supported)")
        path = build_out_path(out, prompt, ext, i, len(items))
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64))
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--prompt", required=True)
    common.add_argument("--out", required=True, help="target file or directory (trailing slash)")
    common.add_argument("--size", default="1024x1024")
    common.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    common.add_argument("--format", default="webp", choices=["png", "jpeg", "webp"])
    common.add_argument("--n", type=int, default=1)

    gen = sub.add_parser("generate", parents=[common])
    gen.add_argument("--background", default="auto", choices=["transparent", "opaque", "auto"])

    edit = sub.add_parser("edit", parents=[common])
    edit.add_argument("--image", action="append", required=True, dest="images")

    args = parser.parse_args()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        die("OPENAI_API_KEY is not set")

    if args.command == "generate":
        payload = {
            "model": MODEL,
            "prompt": args.prompt,
            "size": args.size,
            "quality": args.quality,
            "output_format": args.format,
            "background": args.background,
            "n": args.n,
        }
        resp = post_json(API_URL, payload, api_key)
    else:
        if not 1 <= len(args.images) <= 16:
            die("provide between 1 and 16 input images")
        fields = {
            "model": MODEL,
            "prompt": args.prompt,
            "size": args.size,
            "quality": args.quality,
            "output_format": args.format,
            "n": str(args.n),
        }
        files = []
        for path in args.images:
            if not os.path.isfile(path):
                die(f"input image not found: {path}")
            ctype = mimetypes.guess_type(path)[0] or "image/png"
            files.append(("image[]", path, ctype))
        resp = post_multipart(API_URL_EDITS, fields, files, api_key)

    paths = save_images(resp, args.out, args.prompt, args.format)
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
