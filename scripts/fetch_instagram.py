#!/usr/bin/env python3
"""Refresh the Instagram post list from the public profile-embed endpoint.

Writes data/instagram_posts.json and downloads preview images into
assets/images/instagram/posts/. The site only ever reads those files — it never
talks to Instagram at request time.

This is a convenience for the site owner, not an official API: the endpoint is
public and requires no login, but it can change or rate-limit without notice.
Failures are non-fatal by design — the previous snapshot simply stays in place.

Usage:
  python3 scripts/fetch_instagram.py                     # default account, 6 posts
  python3 scripts/fetch_instagram.py --dry-run           # print, change nothing
  python3 scripts/fetch_instagram.py --limit 9
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "instagram_posts.json"
IMAGE_DIR = ROOT / "assets" / "images" / "instagram" / "posts"
UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
)
EMBED = "https://www.instagram.com/{username}/embed/"
PREVIEW_WIDTH = 900


def fetch_html(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "da-DK,da;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def extract_posts(html: str) -> tuple[str, list[dict]]:
    """Return (profile_url, posts) from the embed page's contextJSON blob."""
    key = '"contextJSON":'
    start = html.find(key)
    if start == -1:
        raise ValueError("contextJSON not found — Instagram may have changed the embed page")
    value, _ = json.JSONDecoder().raw_decode(html[start + len(key):])
    context = json.loads(value)["context"]

    username = context.get("username") or ""
    profile_url = f"https://www.instagram.com/{username}/" if username else ""

    posts = []
    for item in context.get("graphql_media") or []:
        media = item.get("shortcode_media") or {}
        shortcode = media.get("shortcode")
        if not shortcode:
            continue
        caption_edges = (media.get("edge_media_to_caption") or {}).get("edges") or []
        raw_caption = caption_edges[0]["node"].get("text", "") if caption_edges else ""
        posts.append(
            {
                "shortcode": shortcode,
                "url": f"https://www.instagram.com/p/{shortcode}/",
                "image_url": media.get("display_url"),
                "caption": clean_caption(raw_caption),
            }
        )
    return profile_url, posts


def clean_caption(text: str) -> str:
    """First paragraph, hashtags removed, single line, sensible length."""
    paragraph = re.split(r"\n\s*\n", text.strip())[0] if text.strip() else ""
    lines = [line.strip() for line in paragraph.splitlines() if not line.strip().startswith("#")]
    caption = re.sub(r"\s+", " ", " ".join(lines)).strip()
    if len(caption) > 160:
        caption = caption[:157].rstrip(" ,.;:") + "…"
    return caption


def preview_path(shortcode: str) -> str:
    """Path as used in frontmatter — relative to assets/."""
    return f"images/instagram/posts/{shortcode}.jpg"


def download_preview(url: str, shortcode: str, dry_run: bool) -> str | None:
    """Save a 900px-wide preview; skip if it already exists."""
    target = IMAGE_DIR / f"{shortcode}.jpg"
    if target.exists():
        return preview_path(shortcode)
    if dry_run:
        print(f"  would download preview: {target.name}")
        return preview_path(shortcode)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = response.read()
    tmp = target.with_suffix(".tmp")
    tmp.write_bytes(payload)
    with Image.open(tmp) as image:
        image = image.convert("RGB")
        if image.width > PREVIEW_WIDTH:
            height = round(image.height * PREVIEW_WIDTH / image.width)
            image = image.resize((PREVIEW_WIDTH, height), Image.LANCZOS)
        image.save(target, quality=82, optimize=True, progressive=True)
    tmp.unlink(missing_ok=True)
    print(f"  downloaded preview: {target.name} ({target.stat().st_size // 1024} KB)")
    return preview_path(shortcode)


def load_existing() -> dict:
    if not DATA_FILE.exists():
        return {}
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError:
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="jcleemann_byg")
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    print(f"Fetching public embed for @{args.username} …")
    try:
        html = fetch_html(EMBED.format(username=args.username))
        profile_url, found = extract_posts(html)
    except (urllib.error.URLError, ValueError, KeyError) as error:
        print(f"FAILED: {error}", file=sys.stderr)
        print("Keeping the existing snapshot; nothing was changed.", file=sys.stderr)
        return 1

    if not found:
        print("No posts found in the embed payload; keeping the existing snapshot.", file=sys.stderr)
        return 1

    existing = load_existing()
    previous_en = {
        post["url"]: (post.get("caption") or {}).get("en")
        for post in existing.get("posts", [])
        if post.get("url")
    }

    posts = []
    for item in found[: args.limit]:
        image = download_preview(item["image_url"], item["shortcode"], args.dry_run)
        caption = {"da": item["caption"]} if item["caption"] else {}
        en = previous_en.get(item["url"])
        if en:
            caption["en"] = en
        posts.append({"url": item["url"], "image": image, "caption": caption})

    if args.dry_run:
        print(json.dumps({"profile_url": profile_url, "posts": posts}, ensure_ascii=False, indent=2))
        return 0

    # Idempotent: if the post list (including image paths and captions) is unchanged,
    # leave the file — and its timestamp — alone so the daily run makes no commit.
    if existing.get("posts") == posts and existing.get("profile_url") == profile_url:
        print(f"No changes — {len(posts)} posts already up to date.")
        return 0

    data = {
        "generated_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile_url": profile_url,
        "posts": posts,
    }
    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(rendered)
    print(f"Updated {DATA_FILE.relative_to(ROOT)} with {len(posts)} posts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
