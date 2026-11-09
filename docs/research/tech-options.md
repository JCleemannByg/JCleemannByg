# Static site + client editing + Instagram for J Cleemann Byg (GitHub Pages, 2026)

Researched 2026-11-09. Scope: photo-heavy carpenter showcase, owner-editable, free hosting, Instagram-leaning.
Facts below were checked against live sources (see "Sources"); anything I could not verify is flagged under **Uncertainties**.

## TL;DR

**Recommendation: Astro 7 + markdown content collection + Pages CMS (hosted, `.pages.yml`) + GitHub Actions → GitHub Pages.**
Astro because `../ICV-Consult` already proves the exact pattern (markdown in `src/content/`, image pipeline via `sharp`, zero JS output) and the code you must maintain is ~5 small files. Pages CMS because it is the only free editor here that needs **zero OAuth proxy, zero build step inside the CMS, works on a phone**, and is Astro-supported in Astro's own docs. Instagram: ship a curated, repo-committed photo gallery as the primary showcase, plus a "Follow on Instagram" button — do **not** build the site's feed on Instagram's API.

## 1. GitHub Pages constraints that actually bite

Source: [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) (checked 2026-11-09).

| Constraint | Reality | Impact for this project |
|---|---|---|
| Site size | Source repo "recommended" ≤ 1 GB; published site ≤ 1 GB | Fine for ~100–150 optimised photos; real risk only if raw 4 MB camera JPEGs are committed (ICV's 6 images are already 9.9 MB raw → 1.8 MB built) |
| Bandwidth | 100 GB/month **soft** | Irrelevant at this traffic level |
| Builds | 10 builds/hour **soft** — *does not apply* to custom Actions workflows | Non-issue with Actions |
| Deploy timeout | Pages deployment fails after **10 minutes** | Real risk once the image pipeline processes many large photos; cap uploads at ~2000 px long edge |
| Site types | One user/org site (`<user>.github.io`) per account; one project site per repo | Project site = `https://<user>.github.io/JCleemannByg` → needs Astro `base: '/JCleemannByg'`; a custom domain (e.g. `jcleemannbyg.dk`) removes base-path fiddling and needs no extra hosting plan |
| HTTPS | "Enforce HTTPS" toggle, free cert, also for custom domains | Free, one-time click |
| Server-side | None. No forms, no redirects file, no PHP | Contact = `tel:`/`mailto:` (as ICV did) or Formspree free tier |
| Private repo | Pages from a private repo needs a paid plan, **and the published site is still public** (private *site* visibility is GitHub Enterprise Cloud only, and it changes to a random `*.pages.github.io` subdomain) | Just make the repo public — nothing secret in a brochure site. Repo public is free. |
| Build source | Branch publishing runs **Jekyll 3.10.0 / Ruby 3.3.4** (`github-pages` gem 232, dependency page last updated 2025-08-13); Actions publishing runs anything | Another reason to use Actions, not branch mode |

## 2. Generators worth considering (current versions, 2026-11-09)

| Tool | Latest (npm/GitHub) | Markdown ergonomics | Output weight | Images | Owner learning curve | Ecosystem lock-in |
|---|---|---|---|---|---|---|
| **Astro** | 7.4.7 (`@astrojs/mdx` 8.1.3) | Excellent — content collections + Zod schema, frontmatter validates on build | ~0 KB JS by default (ICV builds 0 bytes JS, ~6 KB HTML/page) | Best in class: `image()` in schema, `sharp` 0.35.x, responsive `srcset`/webp automatic | Owner never touches code; dev needs Astro knowledge (already have it) | None — static output, MIT |
| **Eleventy** | 3.1.8 (canary 4.0.0-alpha.10) | Best pure-markdown feel, no schema; ESM config, a bit quirky | 0 KB JS | Manual: needs `@11ty/eleventy-img` or manual `sharp` steps | Low | None |
| **Hugo** | 0.169.0 | Good; frontmatter + shortcodes, but Go templates are the least approachable of the four | 0 KB JS | Built-in processing (resize/webp) — excellent, no Node | Low-medium (themes/config are the fiddly part) | None, but single binary + themes; modules can get confusing |
| **Jekyll** | 3.10.0 only, if you stay on Pages' native build | Good, familiar | 0 KB JS | None built in (`jekyll-picture-tag` plugin not on Pages' allowlist) | Lowest editor-side | High: pinned to Jekyll 3 / Ruby 3.3 on Pages; Jekyll 4 needs Actions and a Ruby toolchain |
| **VitePress** | 1.6.4 stable (2.0.0-alpha.21 on `next`) | Markdown-first, superb search/sidebar | Small but ships Vue JS | Manual | Low, but it is a **docs** framework — wrong shape for a portfolio; you fight it for a gallery layout |

Verdict: Astro is the only option that is simultaneously (a) already proven in this workspace, (b) the strongest image story for a photo portfolio, and (c) listed as a first-class CMS target by both Pages CMS and Decap. Eleventy is the honest runner-up if you want to avoid Astro's abstractions; Hugo wins only if you want a single binary and no npm.

## 3. Editing UX for a non-technical owner (decisive criterion)

Owner persona: 40–60s craftsman, phone photos, no git, will not install Node.

| Option | Cost | Needs build step? | Needs OAuth proxy? | Mobile | Teachable in one sitting? |
|---|---|---|---|---|---|
| **Pages CMS** ([pagescms.org](https://pagescms.org/), app 2.1.8, Jun 2026, MIT, free hosted app or self-host on Vercel) | **Free**, GitHub-only | No — commits to repo; GitHub Actions rebuilds | **No** — it is a GitHub App, sign in with GitHub, install on repo | **Yes**, "full responsive design, optimized for mobile" | **Yes.** Log in → pick site → edit fields / drag photos → save. `.pages.yml` defines the sidebar and field labels (Danish!). |
| Decap CMS ([decapcms.org](https://decapcms.org/docs/github-backend/), 3.17.3) | Free OSS; **Decap Turbo Free = 1 site + 1 seat with hosted auth**; Pro €19/mo | No (static `/admin` page hits the API) | Historically yes (Netlify Identity or self-run OAuth). Now avoidable via Turbo Free, but that ties the client to a paid product's free tier | Usable | Yes, but more moving parts and a second login provider to explain |
| TinaCMS Cloud | Free = 2 users; **Team $29/project/month** | Yes — Tina edits through a live preview/GraphQL layer, needs its build integration | No (Tina's own auth) | Usable | Overkill and *paid* for a one-person brochure site |
| GitHub web editor (github.dev / github.com edit) | Free | No | No | Poor on phone (file tree, raw frontmatter, image upload friction) | Borderline — markdown + YAML frontmatter + `../../images/x.jpg` paths confuses non-technical users (ICV's README needs 100+ lines to explain it); the image field is the part that breaks them |
| GitHub Codespaces | Free monthly core-hour quota (verify current number) | Yes | No | No (desktop VS Code) | No |
| Obsidian + git plugin | Free app, paid sync or DIY git | No | No | Obsidian mobile + git on iOS is fragile | No |
| StackEdit / plain browser editors | Free | No | No | OK | Edits one file at a time, no media library, no schema — not a CMS |

**Conclusion:** Pages CMS is the single biggest UX win available here, and it is free. The owner gets named Danish fields ("Titel", "Billeder", "Beskrivelse"), a drag-and-drop media manager, and phone upload — while the truth on disk stays plain markdown + images, so there is no lock-in: delete `.pages.yml` and hand-editing still works.

## 4. Image workflow for a photo-heavy portfolio

- **Location:** keep originals *out* of git where possible. Pattern that works: `src/images/<project-slug>/01.jpg` committed at **≤ 2000 px long edge, JPEG q80 (~200–400 KB)**, Astro generates the responsive webp variants at build time (`image()` in the content schema, exactly as ICV does).
- **Compression:** do it before commit. Google's Squoosh repo is **archived** ([GoogleChromeLabs/squoosh](https://github.com/GoogleChromeLabs/squoosh)) and `squoosh-cli` is unpublished on npm — use `sharp-cli` (6.1.0) in a tiny `npm run images` script, or resize client-side before upload via Pages CMS's image field. Do not rely on Squoosh.
- **Git LFS:** do **not** use it. GitHub Pages does not serve LFS content (visitors get pointer files), and Decap's GitHub backend explicitly does not support LFS. Plain compressed files only.
- **Repo budget:** 150 photos × 300 KB ≈ 45 MB — far inside the 1 GB soft cap, and keeps Actions build under the 10-minute deploy ceiling.
- **Phone path (the one that matters):** Pages CMS media manager from the phone browser → uploads the (already camera-sized) photo to `src/images/...`, commits, Actions rebuilds in ~1–2 min. Alternative: owner air-drops to the developer, who batch-runs `npm run images`. Decide this with the owner — do not assume.

## 5. Instagram integration — what is actually possible in 2026

| Approach | Works without tokens? | Cost | Fidelity | Risks / gotchas |
|---|---|---|---|---|
| (a) Profile link / follow button / handle badge | Yes | Free | Just a link out | Zero risk, zero upkeep. Underrated for a carpenter: Instagram *is* the feed. |
| (b) Official native embeds (per post/reel/profile, `instagram.com/embed.js` + `blockquote.instagram-media`, oEmbed → iframe) | **Yes** — no token, no app | Free | Real post, real caption, auto-updating likes | **One post at a time** — there is no official grid/feed widget; each new post = a new embed code pasted in. Loads Meta JS **on page load** and sets third-party cookies → under GDPR/Fashion ID (CJEU C-40/17) the site is a joint controller; for a Danish site you'd need consent/click-to-load. Can be blank inside strict consent walls, corporate networks, or Safari content blockers; owner also can't restyle it. Deleted/private post → empty box. |
| (c) Instagram Graph API pull (`/me/media`, Business/Creator account, Meta app + **App Review**, v25.0 since Feb 2026, long-lived token ≤ 60 days, ~200 req/hour) | No | Free API, real cost = setup + upkeep | Genuine auto-updating feed, first-party markup | Wrong shape for a static site: the token must live in a repo secret, a scheduled Action must refresh it every ≤60 days and rebuild, and app review can take weeks. Also **Basic Display API was shut down Dec 2024**; its replacement ("Instagram API with Instagram Login") is read-only but still app-review/token territory. Unofficial scrapers break Meta ToS and break silently. **Recommend against.** |
| (d) Build-time snapshot: curator copies chosen photos into `src/images/instagram/` with a caption + link to the post | Yes | Free | Perfect visual fidelity, own compression, no iframe, no cookies, no CJEU problem | Manual curation per update (5 minutes); must respect the owner's own photo rights (he owns them — trivial here) |
| (e) Third-party widgets (LightWidget: free tier refreshes every **24 h**, $15 one-time per widget for 30-min refresh, $39/yr image optimisation add-on; SnapWidget; Elfsight: free tier is heavily branded/limited, paid from monthly) | No — they hold the API connection | Free tier or $15–$120/yr | Auto-updating grid, styled to site | Third-party script + their cookies/consent story, another account the owner must keep, and a vendor that can vanish or reprice. Acceptable *only* if "auto-updating" is a hard requirement. |

**Recommended low-maintenance combo:** (d) + (a), with (b) available as an opt-in.
1. Primary gallery = curated photos committed to the repo (fast, GDPR-clean, matches the site design, works forever).
2. Prominent "Følg os på Instagram" button in header/footer → `https://instagram.com/<handle>`.
3. If the owner insists on live embeds, add **one** click-to-load facade (a styled placeholder that injects the blockquote + `embed.js` only on click) — satisfies consent, costs one small component, no token, no vendor.

## 6. Three concrete recipes

### Recipe A — Astro + Pages CMS + Actions (recommended)
Files: `astro.config.mjs` (site/base + sitemap), `src/content.config.ts` (Zod schema incl. `image()`), `src/content/projekter/*.md` (one file per project), `src/pages/index.astro`, `src/pages/[slug].astro`, `src/layouts/Base.astro` (all CSS, per ICV), `src/images/**`, `.pages.yml` (~40 lines: `media: src/images`, collections `projekter`/`sider`, Danish labels), `.github/workflows/deploy.yml`, `README.md` in Danish.
Owner flow: Pages CMS (phone) → edit → save → Actions builds Astro (sharp images) → Pages. ~1–2 min to live.
New files for a new project = zero developer work. New *page type* = developer work.
Yearly maintenance: bump Astro major (~1×/yr, 30–60 min with the v7→v8 guide), no service to pay for, no token to rotate, no CMS server.

### Recipe B — Eleventy + Decap (or Decap Turbo Free)
Files: `.eleventy.js`, `_layouts/base.njk`, `_includes/`, `content/projekter/*.md`, `admin/index.html` + `admin/config.yml` (Decap), an auth path (Decap Turbo Free, or a Netlify/GitHub OAuth proxy Worker), `deploy.yml`, image optimisation via `eleventy-img`.
Tradeoff: simplest templating, but you hand-build the image pipeline and the Decap auth/deploy-preview wiring; the CMS is a static `/admin` page coupled to a beta-ish Turbo tier. More files, more ways to break.

### Recipe C — Jekyll on GitHub Pages' native build + GitHub web editing
Files: `_config.yml`, `_layouts/default.html`, `projekter/*.md`, `index.html` (Liquid), images in `assets/img`.
Tradeoff: literally zero CI to maintain (Pages builds on push), and the owner *can* edit in the GitHub web UI. But: pinned to **Jekyll 3.10.0**, no image optimisation, no media manager, and editing lives inside GitHub's code editor — this is the recipe that most often produces a broken site the owner can't diagnose. Only pick it if you truly want zero Actions.

## 7. Comparison table (decision view)

| | Astro + Pages CMS (A) | Eleventy + Decap (B) | Jekyll + GitHub editor (C) | Hugo + Pages CMS |
|---|---|---|---|---|
| Owner edits on phone | **Yes, nice** | Yes, ok | No, painful | Yes |
| Photo pipeline quality | **Best (sharp, built-in)** | Manual | None | Very good (native) |
| Files you must maintain | ~9 | ~12 | ~5 | ~8 |
| Runtime services/accounts to keep alive | 1 (Pages CMS app) | 2 (Decap Turbo/Turbo or proxy + GitHub OAuth app) | 0 | 1 |
| Recurring cost | **0** | 0 (or €19/mo Pro) | 0 | 0 |
| Reuses proven ICV code | **Yes, ~95 %** | No | No | No |
| Risk of silent breakage | Low | Medium | Medium-high | Low-medium |
| Fits Instagram-as-showcase | Good (curated gallery) | Good | Weak | Good |

## 8. Recommendation, in one paragraph

Build **Recipe A**: clone the ICV-Consult structure (Astro 7.4.x, one markdown file per project, `image()`-validated frontmatter, one `Base.astro` holding all CSS, `withastro/action` → `deploy-pages`), add a `projekter` collection plus a homepage gallery, and put **Pages CMS** in front of it with a Danish-labelled `.pages.yml` so the owner edits on his phone and never sees git. Host free on GitHub Pages under a custom domain if `jcleemannbyg.dk` is available (drop `base` handling) or as a project path if not. Treat Instagram as *content source, not integration*: curate his best Instagram photos into `src/images/` with captions, link out to the profile, and optionally ship one consent-gated click-to-load embed. That gives a 0 kr/year site, one dependency to teach, and no token that can expire on a Sunday.

## 9. Notes from reading ICV-Consult (what to copy, what to fix)

- `package.json`: `astro ^7.4.2`, `@astrojs/mdx ^8.1.1`, `@astrojs/sitemap ^3.7.4`, Node ≥ 22.23.4 — current and clean.
- `.github/workflows/deploy.yml` uses `actions/checkout@v4` and `actions/deploy-pages@v4`; current Astro docs use `actions/checkout@v7` + `withastro/action@v6` + `actions/deploy-pages@v5`. Copy the current majors, not ICV's.
- **Actual drift bug to not repeat:** ICV's `deploy.yml` triggers on `master` (with a comment saying so) while its README tells the owner every push to `main` deploys. Pick one branch name in the scaffold and make README + workflow + `git init` agree.
- `src/images` is 9.9 MB for six photos (two > 3 MB) — proves the need for an upload-size rule for a project with dozens of project photos.
- Content authoring is genuinely simple (`title`, `titel`, `beskrivelse`, `billede`, `slideshow`), which is exactly why Pages CMS can map onto it 1:1.
- README is hand-written Danish, ~150 lines, and is the *real* onboarding artefact. Budget a similar one; it is not optional for a non-technical owner.

## 10. Uncertainties / verify before committing to the plan

1. **Owner's willingness to use any CMS.** Everything above assumes he'll log into `app.pagescms.org` with a GitHub account. If he won't, the honest fallback is "send photos + text to the developer", i.e. Recipe A minus Pages CMS — cheaper to maintain, but not self-service.
2. **Pages CMS is effectively one maintainer** (Ronan Berder; latest release 2.1.8, 2026-06-08). Mitigation: MIT + deployable on Vercel in minutes — plan a 1-hour escape hatch, don't depend on the hosted app forever.
3. **Instagram embed behaviour on the owner's audience's devices** (iPhone content blockers, Danish consent tooling) can't be verified from here — test one click-to-load embed on a real phone before promising it.
4. **Graph API specifics** were confirmed via vendor/community write-ups ([zernio.com](https://zernio.com/blog/instagram-api), Meta dev forum), not Meta's own docs page-by-page; before any API work, re-read `developers.facebook.com` for the current version and app-review requirements. Basic Display's Dec 2024 shutdown and the Business/Creator + app-review requirement are corroborated across sources and are safe to plan around.
5. **Exact free quotas** for GitHub Codespaces minutes, Formspree submissions and LightWidget/Elfsight free tiers change; re-check if any of them become part of the design.
6. **Custom domain decision** (`jcleemannbyg.dk` vs `.github.io/JCleemannByg`) is the owner's call; it changes `base`/`site` config and the README's DNS section, so settle it before scaffolding.

## Sources

- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) · [What is GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) · [Pages visibility (GHEC-only private sites)](https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site) · [Pages dependency versions (Jekyll 3.10.0)](https://pages.github.com/versions/)
- [Astro GitHub Pages deploy guide](https://docs.astro.build/en/guides/deploy/github/) · [Astro Pages CMS guide](https://docs.astro.build/en/guides/cms/pages-cms/) · [Astro Sept 2026 release notes](https://astro.build/blog/whats-new-september-2026/)
- [Pages CMS](https://pagescms.org/) · [Pages CMS quick start](https://pagescms.org/docs/quick-start/) · [Decap CMS GitHub backend](https://decapcms.org/docs/github-backend/) · [Decap Turbo plans](https://decapcms.org/turbo/) · [TinaCloud pricing](https://tina.io/blog/tinacloud-pricing-changes)
- [Instagram API in 2026 (overview)](https://zernio.com/blog/instagram-api) · [Native embed code and its limits](https://flockler.com/blog/instagram-embed-code) · [Click-to-load consent pattern & Fashion ID](https://cookiebeam.com/guides/social-media-embeds-consent-click-to-load-2026) · [Instagram embed GDPR notes](https://www.flowconsent.com/en/services/social-media/instagram-embed) · [LightWidget pricing](https://lightwidget.com/pricing)
- [Squoosh is archived](https://github.com/GoogleChromeLabs/squoosh)
- Local evidence: `../ICV-Consult/{package.json,astro.config.mjs,.github/workflows/deploy.yml,src/content.config.ts,README.md}`
