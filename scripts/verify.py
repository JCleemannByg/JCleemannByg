#!/usr/bin/env python3
"""Verify the built site before it is published.

Checks (all of them have caught a real bug in this project's history):
  1. every Danish page has an English counterpart and vice versa
  2. every page declares <html lang>
  3. hreflang alternates are reciprocal and point at pages that exist
  4. every <img> has width + height (prevents layout shift)
  5. every internal link / asset reference resolves to a built file
  6. every root-absolute URL carries the GitHub Pages base path

Usage:
  python3 scripts/verify.py --public public --base /JCleemannByg/
  python3 scripts/verify.py --public public --base /          # local builds
"""
from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

LANG_RE = re.compile(r"^[a-z]{2}(-[A-Z]{2})?$")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang: str | None = None
        self.hreflang: list[tuple[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.refs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v if v is not None else "") for k, v in attrs}
        if tag == "html":
            self.html_lang = a.get("lang")
        elif tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang.append((a["hreflang"], a.get("href", "")))
        elif tag == "img":
            self.images.append(a)
            if a.get("src"):
                self.refs.append(a["src"])
        elif tag == "source" and a.get("srcset"):
            self.refs.extend(part.strip().split(" ")[0] for part in a["srcset"].split(","))
        if tag in ("a", "link", "script") and a.get("href"):
            self.refs.append(a["href"])


def html_files(public: Path) -> list[Path]:
    return sorted(p for p in public.rglob("*.html"))


def url_to_file(public: Path, url: str) -> Path | None:
    """Map a site URL path to a built file, or None if external/anchor."""
    if not url or url.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path.startswith("/"):
        return None
    base = path
    target = public / base.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    if target.is_file():
        return target
    if (target.with_suffix(".html")).is_file():
        return target.with_suffix(".html")
    return None


def to_path(href: str) -> str:
    """Reduce an absolute or relative href to its path component."""
    parsed = urlparse(href)
    return parsed.path or href


def strip_base(path: str, base: str) -> str:
    """Remove the GitHub Pages subpath from a URL path."""
    if base != "/" and path.startswith(base):
        path = "/" + path[len(base):]
    return path or "/"


def counterpart(url: str) -> str:
    """Danish URL -> English URL (and back)."""
    if url == "/":
        return "/en/"
    if url.startswith("/en/"):
        return url[3:]
    return "/en" + url


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", default="public")
    ap.add_argument("--base", default="/", help="base path, e.g. /JCleemannByg/")
    ap.add_argument("--i18n", default="i18n", help="folder with the per-language TOML label files")
    args = ap.parse_args()

    public = Path(args.public)
    if not public.is_dir():
        print(f"FAIL  {public} does not exist — run hugo first", file=sys.stderr)
        return 1

    base = args.base if args.base.endswith("/") else args.base + "/"
    pages = [p for p in html_files(public) if p.relative_to(public).as_posix() != "da/index.html"]
    problems: list[str] = []
    checked_images = 0
    checked_refs = 0

    parsed: dict[Path, PageParser] = {}
    for page in pages:
        pp = PageParser()
        pp.feed(page.read_text(encoding="utf-8", errors="replace"))
        parsed[page] = pp

        rel = "/" + page.relative_to(public).parent.as_posix().strip("./") + "/"
        rel = rel.replace("//", "/")

        # 2. <html lang>
        if not pp.html_lang or not LANG_RE.match(pp.html_lang):
            problems.append(f"{rel}: missing or malformed <html lang> ({pp.html_lang!r})")

        # 1. translation counterpart
        other = counterpart(rel)
        other_page = public / other.lstrip("/") / "index.html"
        if not other_page.is_file():
            problems.append(f"{rel}: no translation at {other}")

        # 3. hreflang reciprocity
        for lang, href in pp.hreflang:
            href = strip_base(to_path(href), base)
            target = url_to_file(public, href)
            if target is None:
                problems.append(f"{rel}: hreflang {lang} points to a non-page ({href})")
                continue
            tp = PageParser()
            tp.feed(target.read_text(encoding="utf-8", errors="replace"))
            target_url = "/" + target.relative_to(public).parent.as_posix().strip("./") + "/"
            if not any(strip_base(to_path(h), base) == href for _, h in tp.hreflang):
                problems.append(f"{rel}: hreflang {lang} -> {href} is not reciprocal")

        # 4. images have dimensions
        for img in pp.images:
            checked_images += 1
            if not img.get("width") or not img.get("height"):
                problems.append(f"{rel}: <img> without width/height ({img.get('src', '?')})")

        # 5./6. references resolve and carry the base path
        for ref in pp.refs:
            if ref.startswith(("#", "mailto:", "tel:", "data:", "https://", "http://")):
                continue
            if ref.startswith("/"):
                checked_refs += 1
                if not ref.startswith(base):
                    problems.append(f"{rel}: root-absolute ref missing base {base!r}: {ref}")
                    continue
                stripped = ref[len(base) - 1 :] if base != "/" else ref
                if url_to_file(public, stripped) is None:
                    problems.append(f"{rel}: broken link/asset: {ref}")

    # translation of UI labels: both language files must expose the same keys
    i18n = Path(args.i18n)
    if i18n.is_dir():
        keys = {}
        for toml_file in sorted(i18n.glob("*.toml")):
            found = set()
            for line in toml_file.read_text(encoding="utf-8").splitlines():
                match = re.match(r"^([a-z_][a-z0-9_]*)\s*=", line)
                if match:
                    found.add(match.group(1))
            keys[toml_file.stem] = found
        if len(keys) >= 2:
            languages = sorted(keys)
            union = set().union(*keys.values())
            for lang in languages:
                missing = union - keys[lang]
                if missing:
                    problems.append(f"i18n/{lang}.toml: missing keys {sorted(missing)}")

    # report
    print(f"public:            {public}")
    print(f"base path:         {base}")
    print(f"html pages:        {len(pages)} (+1 language alias ignored)")
    print(f"images checked:    {checked_images}")
    print(f"internal refs:     {checked_refs}")
    print(f"hreflang pairs:    {sum(len(p.hreflang) for p in parsed.values())}")
    print(f"i18n languages:    {len(list(Path(args.i18n).glob('*.toml')))}")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nOK — no problems found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
