#!/usr/bin/env python3
"""Generate placeholder photography for local design review.

Real project photos will replace these later. Everything here is procedural
warm texture (oak, painted panelling, lime plaster, workshop light) so the
layout can be judged without shipping copyrighted stock imagery.

Run:  python3 scripts/gen_placeholders.py
"""
from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "assets" / "images"


def _gradient(h: int, w: int, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> np.ndarray:
    """Vertical linear gradient as float RGB array."""
    t = np.linspace(0.0, 1.0, h)[:, None, None]
    top_a = np.array(top, dtype=np.float32)
    bot_a = np.array(bottom, dtype=np.float32)
    return np.repeat(top_a + (bot_a - top_a) * t, w, axis=1)


def _noise(h: int, w: int, blur: float, rng: np.random.Generator) -> np.ndarray:
    """Smooth low-frequency noise in [-1, 1]."""
    n = rng.normal(0.0, 1.0, (h, w)).astype(np.float32)
    img = Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8))
    img = img.filter(ImageFilter.GaussianBlur(blur))
    arr = np.asarray(img, dtype=np.float32) / 255.0
    return (arr - 0.5) * 2.0


def _vignette(h: int, w: int, strength: float = 0.55) -> np.ndarray:
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cy, cx = h / 2.0, w / 2.0
    r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    mask = 1.0 - strength * np.clip(r / 1.35, 0.0, 1.0) ** 1.7
    return mask[:, :, None]


def _finish(arr: np.ndarray, path: Path, quality: int = 85) -> None:
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr).save(path, quality=quality, optimize=True, progressive=True)
    print(f"  {path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")


def wood(h: int, w: int, seed: int, dark=(74, 46, 27), light=(150, 101, 60), grain: float = 0.22) -> np.ndarray:
    """Horizontal wood grain with warped lines and a lit side."""
    rng = np.random.default_rng(seed)
    arr = _gradient(h, w, dark, light) * 0.92
    # warp field + high-frequency grain
    warp = _noise(h, w, blur=max(h, w) / 90.0, rng=rng) * 26.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    phase = (yy * 0.9 + warp) * (math.pi * 2.0 / 26.0) + rng.uniform(0, 6.28)
    lines = np.sin(phase) * 0.5 + np.sin(phase * 2.13 + 1.1) * 0.22
    dark_streak = (np.sin(phase * 0.37 + 0.4) * 0.5 + 0.5) ** 2
    arr = arr * (1.0 - grain * (lines + 0.6 * dark_streak)[:, :, None])
    # a few darker knots/streaks
    for _ in range(4):
        ky, kx = rng.integers(0, h), rng.integers(0, w)
        rad = rng.integers(30, 110)
        k = np.exp(-(((xx - kx) ** 2 + (yy - ky) ** 2) / (2 * rad**2))).astype(np.float32)
        arr *= (1.0 - 0.22 * k)[:, :, None]
    # direction of light: left brighter
    lx = np.linspace(1.12, 0.86, w)[None, :, None]
    arr *= lx
    arr *= _vignette(h, w, 0.38)
    arr += _noise(h, w, 1.1, rng)[:, :, None] * 4.0
    return arr


def panels(h: int, w: int, seed: int, base=(146, 100, 62), groove=(58, 36, 22)) -> np.ndarray:
    """Vertical shaker-style panelling (kitchen fronts)."""
    rng = np.random.default_rng(seed)
    arr = _gradient(h, w, base, tuple(int(c * 0.78) for c in base)).astype(np.float32)
    arr += _noise(h, w, max(h, w) / 70.0, rng)[:, :, None] * 12.0
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    n = 5
    pw = w / n
    for i in range(n):
        x = i * pw
        d.rectangle([x + 2, 0, x + pw - 3, h], outline=groove + (26,), width=4)
        # recessed inner panel
        inset = pw * 0.14
        d.rectangle([x + inset, h * 0.16, x + pw - inset, h * 0.92], outline=groove + (34,), width=3)
    arr = np.asarray(img, dtype=np.float32)
    # subtle grain across the whole panel
    warp = _noise(h, w, max(h, w) / 120.0, rng) * 8.0
    yy = np.mgrid[0:h, 0:w][0].astype(np.float32)
    arr *= (1.0 - 0.06 * np.sin((yy + warp) * 0.07))[:, :, None]
    arr *= _vignette(h, w, 0.42)
    arr *= np.linspace(1.1, 0.9, w)[None, :, None]
    return arr


def plaster(h: int, w: int, seed: int, base=(228, 221, 208)) -> np.ndarray:
    """Lime-washed wall with soft blotches and daylight from one side."""
    rng = np.random.default_rng(seed)
    tone = _gradient(h, w, tuple(int(c * 1.03) for c in base), tuple(int(c * 0.86) for c in base))
    cloud = _noise(h, w, blur=max(h, w) / 14.0, rng=rng)
    tone += cloud[:, :, None] * 10.0
    tone += _noise(h, w, 2.0, rng)[:, :, None] * 3.0
    tone *= np.linspace(1.09, 0.9, w)[None, :, None]
    tone *= _vignette(h, w, 0.3)
    return tone


def workshop(h: int, w: int, seed: int) -> np.ndarray:
    """Dark moody workshop corner: warm wood, single light from upper left."""
    rng = np.random.default_rng(seed)
    arr = wood(h, w, seed, dark=(38, 26, 18), light=(126, 84, 48))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    glow = np.exp(-(((xx - w * 0.22) ** 2) / (2 * (w * 0.35) ** 2) + ((yy - h * 0.18) ** 2) / (2 * (h * 0.4) ** 2)))
    arr += glow[:, :, None] * 46.0
    arr *= _vignette(h, w, 0.62)
    return arr


def linen(h: int, w: int, seed: int, base=(196, 184, 165)) -> np.ndarray:
    rng = np.random.default_rng(seed)
    arr = _gradient(h, w, tuple(int(c * 1.06) for c in base), tuple(int(c * 0.9) for c in base))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    weave = (np.sin(xx * 1.6) * np.sin(yy * 1.6)) * 5.0
    arr += weave[:, :, None]
    arr += _noise(h, w, 1.4, rng)[:, :, None] * 5.0
    arr *= _vignette(h, w, 0.22)
    return arr


def main() -> None:
    print("Generating placeholder photography…")

    # Hero: workshop light, wide crop.
    _finish(workshop(1800, 2800, seed=11), IMAGES / "hero.jpg", 84)

    # Projects: cover + three gallery frames each.
    sets = {
        "koekken-eg": [panels(1400, 2000, 21), panels(1200, 1800, 22), wood(1200, 1800, 23), panels(1200, 1800, 24)],
        "indbygget-skab": [wood(1400, 2000, 31), wood(1200, 1800, 32), wood(1200, 1800, 33), wood(1200, 1800, 34)],
        "renovering-villa": [plaster(1400, 2000, 41), plaster(1200, 1800, 42), wood(1200, 1800, 43), plaster(1200, 1800, 44)],
    }
    for slug, frames in sets.items():
        for i, frame in enumerate(frames, start=1):
            _finish(frame, IMAGES / "projekter" / slug / f"{i:02d}.jpg")

    # About portrait: workshop, tall crop.
    _finish(workshop(1500, 1200, seed=51), IMAGES / "om" / "portraet.jpg", 84)

    # Instagram strip: square crops.
    _finish(wood(900, 900, 61), IMAGES / "instagram" / "01.jpg")
    _finish(panels(900, 900, 62), IMAGES / "instagram" / "02.jpg")
    _finish(plaster(900, 900, 63), IMAGES / "instagram" / "03.jpg")

    print("Done.")


if __name__ == "__main__":
    main()
