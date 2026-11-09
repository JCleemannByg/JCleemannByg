#!/usr/bin/env python3
"""Downscale and recompress oversized images in assets/images/.

Phone photos are 3–8 MB and often 4000 px wide. Pages CMS uploads them as-is, so
without this the repository grows quickly and every build processes huge files.
This script is idempotent: it only touches files that exceed the limits.

Rules:
  * longest side max 2000 px (downscale only, never upscale)
  * target file size ≤ ~700 KB where possible
  * EXIF orientation is baked in (portrait phone photos stay upright)
  * JPEG re-encoded at quality 82, PNG optimised, WebP at quality 82

Run manually:  pixi run images
Or automatically via .github/workflows/images.yml on pushes that touch images.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "assets" / "images"
MAX_SIDE = 2000
SIZE_LIMIT = 700 * 1024
JPEG_QUALITY = 82
SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def file_size(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def optimize(path: Path, max_side: int = MAX_SIDE, size_limit: int = SIZE_LIMIT) -> bool:
    """Return True when the file was rewritten."""
    plugin_format = {
        ".jpg": "JPEG",
        ".jpeg": "JPEG",
        ".png": "PNG",
        ".webp": "WEBP",
    }[path.suffix.lower()]
    with Image.open(path) as raw:
        image = ImageOps.exif_transpose(raw)

        needs_resize = max(image.size) > max_side
        needs_shrink = file_size(path) > size_limit

        if not needs_resize and not needs_shrink:
            return False

        if needs_resize:
            ratio = max_side / max(image.size)
            size = (max(1, round(image.width * ratio)), max(1, round(image.height * ratio)))
            image = image.resize(size, Image.LANCZOS)

        if plugin_format == "JPEG":
            image = image.convert("RGB")
            image.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        elif plugin_format == "PNG":
            image.save(path, "PNG", optimize=True)
        else:
            image.save(path, "WEBP", quality=JPEG_QUALITY, method=6)

    print(f"  {path.relative_to(ROOT)}: {image.size[0]}x{image.size[1]}, {file_size(path) // 1024} KB")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-side", type=int, default=MAX_SIDE)
    parser.add_argument("--size-limit-kb", type=int, default=SIZE_LIMIT // 1024)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    max_side = args.max_side
    size_limit = args.size_limit_kb * 1024

    if not IMAGE_DIR.is_dir():
        print(f"No image folder at {IMAGE_DIR}", file=sys.stderr)
        return 1

    files = sorted(p for p in IMAGE_DIR.rglob("*") if p.is_file() and p.suffix.lower() in SUFFIXES)
    print(f"Checking {len(files)} images (max {max_side}px, ≤{args.size_limit_kb} KB) …")

    changed = 0
    for path in files:
        if args.dry_run:
            size = file_size(path)
            if size > size_limit:
                print(f"  would optimise {path.relative_to(ROOT)} ({size // 1024} KB)")
                changed += 1
            continue
        try:
            if optimize(path, max_side, size_limit):
                changed += 1
        except Exception as error:  # keep going: one bad file must not block a build
            print(f"  WARNING: could not optimise {path.relative_to(ROOT)}: {error}", file=sys.stderr)

    print(f"Done — {changed} image(s) {'would be ' if args.dry_run else ''}optimised.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
