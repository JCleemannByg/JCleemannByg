# Framework decision — bilingual DA/EN, GitHub Pages project URL

**Status:** bake-off complete 2026-11-09. Two independent prototypes of the *same* spec were built and measured. This supersedes the Astro recommendation in [`OPTIONS.md`](OPTIONS.md) — Astro and the ICV-Consult draft are off the table per your call.
**Decisions already made:** host on GitHub Pages **project URL** first (`https://<user>.github.io/<repo>/`), **Danish + English** from day one, no Astro, no ICV reuse.
**Evidence:** full reports in [`_spikes/hugo/REPORT.md`](_spikes/hugo/REPORT.md) and [`_spikes/eleventy/REPORT.md`](_spikes/eleventy/REPORT.md). Both are working sites — `_spikes/hugo/site/public/` and `_spikes/eleventy/_site/` build and serve under `/JCleemannByg/`.

---

## TL;DR — recommendation: **Hugo** (with Eleventy as the honest alternative)

| Why Hugo wins *for this exact brief* | Number |
|---|---|
| Bilingual is a first-class concept: DA/EN pages are paired by directory path, `.Translations` gives the switcher, i18n strings live in two TOML files | — |
| No Node, no `node_modules`, no lockfile, no npm audit — the site builds from **one pinned binary + markdown** | 0 dependencies |
| Images are built in: responsive WebP/JPEG variants, dimensions, lazy loading | 72 variants from 12 photos |
| Output is genuinely light | **2.25 MiB dist, 0 bytes JS** |
| Build is effectively instant after the first run | **52 ms warm / 2.7 s cold** |
| GitHub Pages subpath and the future custom-domain switch are one config value, mechanically verified | 406/406 URLs prefixed; 1-line switch |
| Site source you'd own and maintain | **677 LOC** in 30 files |

**The catch, stated plainly:** the site lives in **Go templates** (new syntax for you), Hugo's config surface **renamed 8 things** during this very spike (so the version must be pinned), and missing translations **fail silently** at three independent layers (so the repo needs a permanent verification script + `--printI18nWarnings` in CI). None of these is hard to handle once baked into the scaffold — but they are not zero.

**Choose Eleventy instead if** you would rather keep the toolchain in JS/Nunjucks. It is not much more code (511 vs 677 LOC), builds in 1.0 s and ships 218 B of JS — but its bilingual support is **not turnkey**: be prepared for **≈45 lines of hand-written i18n glue** plus two non-obvious workarounds, and one silent-404 trap at the image × path-prefix seam.

**Jekyll is eliminated** with evidence: `jekyll-polyglot` is **not** on GitHub Pages' plugin allowlist and is silently ignored — bilingual Jekyll requires a GitHub Actions build anyway, which was its only advantage (Jekyll 3.10.0 / Ruby 3.3.4 pinned on Pages).

---

## 1. What was actually tested

One identical spec, two independent implementations, built by two separate engineers:

- DA at `/`, EN at `/en/`; language switcher on every page that **preserves the page**; `hreflang` + `x-default` + `<html lang>`.
- 3 sample projects, markdown + frontmatter (`title`, `year`, `category`, `cover`, `gallery`, `summary`), DA + EN versions.
- Pages: home (hero + featured), projects index, project detail with gallery, about, contact.
- 12 placeholder photos (2400×1600, Pillow) → responsive 640/960/1280 + WebP, `width`/`height`, no CLS.
- Must work at `https://USERNAME.github.io/JCleemannByg/`, one-value switch to a custom domain later.
- No client-side JS except a mobile-nav toggle.

Nobody faked a requirement. Where something was impossible or mis-specified, it is called out in the reports (e.g. the plugin named in the Eleventy spec **does not exist on npm**).

## 2. Head-to-head

| Metric | Hugo 0.169.0 | Eleventy 3.1.8 |
|---|---|---|
| Toolchain from zero | self-contained binary, ~13 s download (CDN flaky: 504s on 5/6 retries) — CI caches it | `npm install`, 3.5 s, **165 packages** |
| Runtime footprint | **one 118 MiB binary** (gitignored) | 42 MB `node_modules` |
| Source files / LOC | 30 / **677** (config 80, templates 214/12, content 132, i18n 80, CSS 171) | 26 / **511** (config 81, templates 212/12, content 108, locale data 70, CSS/JS 40) |
| Hand-written **i18n glue** | pages pair natively; ~28 lines for switcher fallback + hreflang | **≈45 lines** (`t` filter 13, switcher 12, hreflang 11, DA-at-root permalink 9) |
| Clean build (median) | 2,669 ms cold / **52 ms warm** | **1,030 ms** clean (image cache warm) |
| Dist | **2.25 MiB**, 96 files | 1.6 MB, 89 files |
| **JS shipped** | **0 B** | 218 B |
| Image variants | 72 = 12 × 3 widths × {JPEG, WebP}; 38/38 `<img>` with dimensions | 72, same widths/formats; dimensions emitted |
| Pages | 14 real (7 DA + 7 EN) + 1 alias | 14 (7 + 7) |
| hreflang | 28 reciprocal pairs, 0 problems | self + alternate + x-default on all pages |
| Subpath verification | 406 root-absolute URLs checked, **0** missing prefix; dist served under `/JCleemannByg/` → all 200s | every internal `href`/`src`/`srcset` scanned, **0** unprefixed |
| Custom domain | 1 line: `baseURL` (verified, 0 leftovers) | 1 line: `PATH_PREFIX` (+ image `urlPath` must stay in sync) |

**Not comparable (but it matters):** Hugo's dist is bigger (2.25 vs 1.6 MiB) because it ships more HTML + bigger JPEG fallbacks; Eleventy's 218 B of JS is a mobile-nav toggle that Hugo does with a CSS checkbox. Neither difference is meaningful for a visitor.

## 3. How bilingual actually behaves (the thing you asked about)

**Hugo** — config declares `defaultContentLanguage = "da"`, `defaultContentLanguageInSubdir = false`, so DA is at `/`, EN under `/en/`. Pages pair by path: `content/projects/koekken/index.da.md` ↔ `index.en.md`. `.Translations` / `.AllTranslations` drive the switcher; string keys in `i18n/da.toml` + `i18n/en.toml`.

**Eleventy** — directory-per-locale (`src/da/`, `src/en/`) + directory data files. The bundled `I18nPlugin` pairs pages by **replacing the language segment in the input path**, provides `locale_url`/`locale_links` — but does **not** translate strings. Because DA must live at `/`, the plugin needed: `errorMode: "allow-fallback"` (default `strict` throws on every DA link), DA files inside `src/da/` with a custom permalink to strip `/da`, and a hand-written `t` filter for strings. ~45 LOC of glue, and the pairing contract is tied to plugin internals.

**Missing translation — measured on both:**

| | Hugo | Eleventy |
|---|---|---|
| Build | succeeds | succeeds |
| EN page | **not generated at all** (URL 404s, no warning) | not generated; old copy can linger until CI cleans `_site` |
| Switcher | falls back to EN home (needs ~10 lines of template logic) | renders disabled "English" label |
| hreflang | silently drops the missing language | only DA + x-default |
| Missing UI string | silently falls back to Danish, or renders **empty** | `t` filter warns + falls back to Danish |

**Verdict:** both are silently forgiving — which is the right behaviour for availability and the wrong behaviour for content completeness. Both need the same CI safety net: a script that (a) checks every DA page has an EN twin, (b) checks every image/URL is prefixed, (c) fails the build if not. Hugo additionally needs `--printI18nWarnings`. **The production scaffold will ship that script as a permanent, non-optional part of the repo** — this is the single most valuable thing the bake-off produced.

## 4. Scoring for this project

Weights reflect the brief (owner edits occasionally; visitors see photos; site must live 3+ years on free hosting).

| Criterion | Weight | Hugo | Eleventy | Notes |
|---|---:|---:|---:|---|
| Bilingual robustness / glue | 30 % | 4.5 | 3.5 | native pairing vs 45 LOC + plugin-internals dependency |
| Owner editing story | 20 % | 4 | 4 | tie: both are markdown + frontmatter; Pages CMS supports both |
| Photo pipeline | 15 % | 4.5 | 4 | tie on output; Hugo's is native, Eleventy's has the silent prefix trap |
| Deploy / subpath robustness | 10 % | 4.5 | 3.5 | Hugo one value; Eleventy two values that can drift |
| Long-term maintenance | 15 % | 4 | 3 | no runtime deps & pinned binary vs npm ecosystem + v4 migration ahead |
| Dev ergonomics / build speed | 10 % | 3.5 | 4 | Go templates vs Nunjucks; 52 ms vs 1 s |
| **Weighted total** | | **4.19** | **3.65** | |

## 5. The case against each (so the choice is informed)

**Hugo**
- Go template syntax is the least approachable of the options; you will touch 214 lines of it rarely, but you *will* touch it.
- Config/API churn: a brand-new project on v0.169.0 threw **8 deprecation warnings** for ordinary patterns; `_build` is already a hard error. → pin `HUGO_VERSION`, upgrade deliberately once a year.
- Local install is now awkward on Apple Silicon (v0.169 macOS ships a universal `.pkg` only; no arm64 tarball) and the release CDN was flaky. `brew install hugo` or the GitHub Action are the sane paths.
- Silent translation failure in three layers (mitigated by the CI script).
- Image cache (`site/resources/`) must be cached in CI, or every deploy pays 2.7 s — trivial, but easy to forget.
- Page bundles publish original photos by default (41 % of dist wasted) unless `publishResources = false` is cascaded — a one-line config, but a real trap.

**Eleventy**
- Bilingual needs ~45 LOC of glue around plugin internals (`eleventy.inputPath`, contentMap, computed `page.lang`) — these are version-pinned internals, not public API.
- The image × `pathPrefix` seam: `@11ty/eleventy-img` is prefix-blind; the naive setup ships `/img/...` → **silent 404s on GitHub Pages with a green build**; the obvious fix (`| url`) double-prefixes (`/JCleemannByg/JCleemannByg/...`). One line once known, not discoverable.
- No clean step: deleted/renamed pages stay published until CI runs `rm -rf _site`.
- 165 npm packages + lockfile + Node version lifecycle; Eleventy 4 is already in alpha ⇒ a future migration.
- Every one of these is fixable — the reports document the fixes — but the repo carries more hidden invariants.

**Other paths considered and rejected:** Jekyll (polyglot not allowlisted — see above); Astro (your call); a bespoke ~250-line Python generator (fully ownable, Python + Pillow + Jinja2 are installed, and it would be the *smallest* mental model — but you become the maintainer of your own SSG: RSS/sitemap/i18n/images all hand-rolled, and no ecosystem to lean on. Worth it only if "no framework at all" is a hard preference).

## 6. If you approve Hugo: what I'll scaffold

Repo `JCleemannByg` (GitHub project site), production files only — the spikes are throwaway and will not be committed:

```
hugo.toml                 # baseURL via env, languages da/en, menus, imaging, build cascade
content/
  _index.da.md / _index.en.md
  projekter/<slug>/index.da.md|index.en.md + photos   # or per-language contentDir (see below)
  om/, kontakt/
layouts/                  # baseof, home, list, single, project, contact, partials
i18n/da.toml i18n/en.toml
assets/css/main.css       # one stylesheet, CSS-only mobile nav
scripts/verify.py         # permanent guard: translations complete? URLs prefixed? images?
.pages.yml                # Pages CMS: Danish labels, mobile-friendly project editor
.github/workflows/deploy.yml   # build (cached binary + resources) → upload-pages-artifact → deploy-pages
.gitignore, README.da.md
```

Decisions already baked in from the bake-off:
- **Pin** `HUGO_VERSION=v0.169.0`; never float on "latest".
- **Per-language `contentDir`** (`content/da/`, `content/en/`) instead of `.da.md`/`.en.md` suffix files — the spike found bilingual page bundles share resources asymmetrically, and separate dirs map cleanly onto Pages CMS collections.
- **`--printI18nWarnings --printPathWarnings`** + `scripts/verify.py` in CI; the build fails on a missing translation, an unprefixed URL, or an image without dimensions.
- **`build.publishResources = false`** cascade (keeps originals out of dist).
- **`baseURL` from GitHub context** in CI (`https://${{ github.repository_owner }}.github.io/${{ github.event.repository.name }}/`), so nothing is hardcoded; custom domain later = one line + a CNAME.
- **Branch `main` everywhere** (workflow, README, git init agree — the ICV repo had main/master drift).
- **Image upload rule:** ≤ 2000 px long edge, JPEG q80 (~200–400 KB) → ~150 photos ≈ 45 MB, inside the 1 GB site cap and the 10-minute deploy limit.
- **Instagram:** unchanged from `OPTIONS.md` — curated gallery in the repo + "Følg på Instagram" buttons; embed only as an optional, consent-gated, click-to-load afterthought. The engine choice doesn't change this.
- Content/editing: Pages CMS on top (Danish field labels), with plain-markdown editing as the fallback. No CMS lock-in.

## 7. What I need from you to start

1. **Hugo or Eleventy?** (my recommendation: Hugo — say "go" and I'll scaffold it)
2. **GitHub username + repo name** — needed for `base_url`, the deploy workflow, and the preview URL. If the repo is `JCleemannByg`, the site will be `https://<user>.github.io/JCleemannByg/`.
3. **Does the GitHub account have Pages enabled** (Settings → Pages → Source: GitHub Actions), or should the scaffold's README walk you through it?
4. **Language of the workflow docs/README:** Danish (for Johann) with an English summary, or both full?

Photos and company facts (CVR, phone, services) can arrive later — the scaffold ships with clearly marked placeholder content so you can see the real thing running the same day.

---

*Spikes are at `_spikes/hugo/` (25 files + binary, 125 MB) and `_spikes/eleventy/` (26 files + `node_modules`, 42 MB). They are gitignored in the planned repo and can be deleted once you've picked — nothing in them is intended for production.*

---

## 8. Free themes — do we need one? (checked 2026-11-09)

Yes, both engines have free templates, but the supply is lopsided and "free" is not the same as "fits".

| Source | Supply | Fit for this brief |
|---|---|---|
| **Hugo theme gallery** (themes.gohugo.io) | hundreds of themes, mostly MIT/Apache; ~50 tagged *portfolio*, many tagged *multilingual* | **Best supply anywhere.** Some are genuinely business-shaped. |
| **Eleventy starters** (11ty.dev/docs/starter) | 1 official starter + ~30 community starters | Mostly blog/documentation-shaped; **no bilingual portfolio/business theme** that fits |
| Generic HTML templates (HTML5UP, Start Bootstrap, ThemeForest freebies) | many | Need conversion into Hugo templates, often attribution requirements, no content model — not worth it here |

**The standout: [Localcraft](https://github.com/maciejkosiarski/localcraft)** (MIT, theme gallery). Purpose-built for small local service businesses, and its section set reads like a carpenter's brief: hero, services, gallery with **before/after sliders**, testimonials, pricing, FAQ, opening hours, location map, contact. Also includes multilingual i18n (`content/<lang>/` + `i18n/*.yaml` + per-language data files), automatic WebP/responsive images + lazy loading, JSON-LD/Open Graph/Twitter SEO, GTM with GDPR cookie consent, no JS frameworks — vanilla JS only. Requires Hugo ≥ 0.123.

Measured on its live demo (EN home page), so this is real, not marketing:

| | Localcraft | Our custom Hugo spike |
|---|---|---|
| JS | **807 B** (nav toggle; other scripts load per page) | 0 B |
| CSS | 54,890 B, one plain stylesheet (no Tailwind) | 6,565 B |
| HTML | 31 KB | ~5 KB/page |

**Caveats, honestly:** it is a young, single-maintainer theme (4 GitHub stars, last push 2026-07-23) with a salon/spa aesthetic ("organic warm minimalism") that would need rebranding for a carpenter — colours, type, and the pet-grooming demo content go. It also brings a larger content model (data files per language, gallery items with `image_before`/`image_after`), which means more Pages CMS config work than our 6-field project frontmatter. Vendoring a copy into the repo (rather than a submodule) removes the abandonment risk, but you then own it.

**Other free candidates, for the record:** Hugo Profile (MIT, ~1.1k stars — developer portfolio, not a business site), Blowfish (MIT, ~2.9k stars — excellent blog/personal theme, Tailwind, not business-shaped), Toha / Beautiful Hugo / Gokarna (creative personal sites). Hugo Blox has free themes but a paid-component upsell — check before committing.

**Recommendation:** templates don't remove the work, they relocate it — from design/CSS to **rebranding someone else's structure**. For this site there is exactly one free theme worth a serious try: **Localcraft**, because *before/after* is the single most persuasive section a carpenter can have and building it ourselves is real work. The honest decision is:

- **Use Localcraft as the base** → faster visual start, professional sections out of the box, accept a rebrand + slightly heavier page + theme ownership.
- **Keep the custom build** → 0 JS, 7 KB CSS, exact brand, simplest content model, but we hand-build the before/after section (a ~40-line CSS/JS component) and design everything ourselves.

I'd only pay for a theme if Localcraft's rebrand turns out to be fighting the layout — which the port would reveal in about an hour.
