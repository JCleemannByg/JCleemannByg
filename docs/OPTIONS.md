# J Cleemann Byg — website options

**Status:** research done 2026-11-09. Nothing built yet — this is the decision menu, not the build.
**Brief:** small photo-led site for a one-man Danish joiner/carpenter. Free hosting on GitHub Pages, content the owner can edit (markdown/rst), Instagram-friendly.

> **Update, later on 2026-11-09 — decisions changed.** Hosting: **GitHub Pages project URL first** (`github.io/<repo>/`), custom domain later. Scope: **Danish + English from day one**. Engine: Astro and the ICV-Consult draft are **off the table**; a Hugo-vs-Eleventy bake-off was run instead — see [`FRAMEWORK.md`](FRAMEWORK.md). Sections below are kept as the original option survey; where they contradict FRAMEWORK.md, FRAMEWORK.md wins.

Detail lives in [`research/company-profile.md`](research/company-profile.md) and [`research/tech-options.md`](research/tech-options.md) — every version number and limit below was checked against live sources there.

---

## 0. TL;DR — the recommended package

| Layer | Recommendation | Why |
|---|---|---|
| **Hosting** | GitHub Pages, free, **project URL now** (`github.io/<repo>/`), custom domain later | Decision made 2026-11-09: start on `github.io`, switch to the registered `jcleemannbyg.dk` with a one-line config change once the site is right. |
| **Engine** | **Hugo** (recommended after bake-off; Eleventy the alternative) | See [`FRAMEWORK.md`](FRAMEWORK.md): native DA/EN pairing, built-in photo pipeline, no Node, 0 B JS, 52 ms warm build. Astro/ICV reuse dropped by request. |
| **Editing** | **Markdown as source of truth, with [Pages CMS](https://pagescms.org/) on top** | Free (MIT), works on his phone, drag-and-drop photos, no OAuth proxy, Danish field labels. Markdown stays the file format, so there is no lock-in. |
| **Instagram** | **Curated gallery committed to the repo + "Følg på Instagram" buttons** | No API, no token expiry, no cookie/consent problem. Instagram remains the feed; the site is the portfolio. |
| **Scope** | 6 pages, **Danish + English**, mobile-first | Decision made 2026-11-09: bilingual from day one. Matches what local customers expect (see `spange.dk`, the strongest local reference). |

**Cost: 0 kr/year** — domain and Titan email are already in place (his existing Hostinger cost), GitHub Pages and Pages CMS are free.
**Effort: ~2–3 working days of build work**, plus the owner's content (photos, service list, CVR number) — that is the real bottleneck.

---

## 1. What investigation turned up (short version)

| Finding | Source | Consequence for the build |
|---|---|---|
| Trading name **"J Cleemann Byg V/Johann Cleemann"**; Johann is the owner, J Cleemann Byg the brand | [krak.dk](https://www.krak.dk/j+cleemann+byg+v%252fjohann+cleemann+n%c3%a6rum/171060879/firma) | Use "J Cleemann Byg" as the visual brand, "Johann Cleemann" in the about section. |
| Address Nærum Hovedgade 15, 3. sal. tv-d, **2850 Nærum** | krak.dk, degulesider.dk | Show address + map pin; local SEO matters more than anything else. |
| Categorised **Snedker** (joiner) by Eniro, but auto-generated portals call him **Tømrer** (carpenter) | krak.dk vs. the two low-trust portals | Copy/SEO title must pick one. Ask him. |
| `jcleemannbyg.dk` **is registered** (Hostinger DNS), A-record → `72.60.81.210`, MX → Titan, SPF set | DNS probes (`dig`), verified | Email works. HTTP 308-redirects to HTTPS, but **TLS has no certificate** → the site is effectively unreachable. Wayback has **zero** captures. |
| No CVR number, full phone number, email address or service list verifiable publicly | CVR/Krak/Proff all bot-walled | One conversation with him resolves it; do not publish guesses. |
| Instagram `@jcleemann_byg` exists and is linked from both listings | krak.dk, degulesider.dk | It is his showcase channel → the site should feed from it, not compete with it. Followers/posts unverifiable (login wall). |
| **Zero indexable web presence** — Bing returns nothing for the exact name | search probes | Low bar, real upside: a clean site plus a Google Business Profile will outrank most local competitors. |
| Local baseline: `spange.dk` has 5–8 pages, service pages, references, "Indhent et tilbud" | fetched | The bar for "looks credible" is low but not zero: projects + real photos + visible phone. |

---

## 2. Hosting options

All options are free and static. They differ only in URL, DNS work and how much you're tied to GitHub.

| | **A. GitHub Pages project URL** | **B. GitHub Pages + `jcleemannbyg.dk`** ← recommended | **C. Cloudflare Pages / Netlify** |
|---|---|---|---|
| URL | `https://<user>.github.io/JCleemannByg` | `https://jcleemannbyg.dk` | own subdomain / domain |
| Extra setup | `base: '/JCleemannByg'` in Astro config | DNS A/CNAME records at Hostinger; HTTPS toggle | connect repo, no Actions file needed |
| Effort | 10 min | 30 min once, then zero | 30 min |
| Downside | Ugly for a business card; breaks if repo renamed | DNS edit must **not** touch MX/TXT or email dies | Leaves the "GitHub Pages" requirement; extra account |
| Cost | 0 | 0 | 0 (free tier) |

**Recommendation: B.** He already pays for the domain; putting the site on it costs nothing extra and removes the subpath/base-path fiddling entirely.

DNS change (at Hostinger — keep the nameservers, keep MX/SPF, only replace the A record):

| Type | Name | Old | New |
|---|---|---|---|
| A | `@` | `72.60.81.210` | `185.199.108.153` … `185.199.111.153` (all four) |
| CNAME | `www` | → apex | → `<github-user>.github.io` |
| MX / TXT | — | Titan | **leave untouched** |

Then: repo Settings → Pages → Source *GitHub Actions*, Custom domain `jcleemannbyg.dk`, Enforce HTTPS. GitHub issues the certificate itself. Verify the four A-record IPs against GitHub's current docs at that moment — they are stable but not worth trusting from memory.
Caveat: this needs his Hostinger login (or DNS access) — the only real dependency on him for launch.

GitHub Pages limits that actually matter here (checked, 2026): published site ≤ **1 GB**, 100 GB/month soft bandwidth, deployment fails after **10 min**, private repo needs a paid plan *and* still publishes a public site → **use a public repo**. Branch-based publishing runs an old Jekyll; **publish from Actions instead**.

---

## 3. Engine options — and why markdown, not rst

| Tool | Current | Markdown-in-repo feel | Images (the deciding factor) | Fit here |
|---|---|---|---|---|
| **Astro** ← recommended | 7.4.x | Excellent: content collections + Zod frontmatter, one `.md` per project | Best: `image()` in the schema, `sharp` builds responsive webp/srcset automatically | **Proven**: `ICV-Consult` is this exact stack; ~95 % reuse |
| Eleventy | 3.1.x | Most "plain markdown", zero schema | Manual (`eleventy-img`/`sharp` wiring) | Honest runner-up if you dislike Astro's abstractions |
| Hugo | 0.169 | Good, but Go templates are the least approachable to hand over | Excellent, built in, no npm | Only if you want a single binary |
| Jekyll | **3.10 only** on Pages | Good | None built in | Zero CI to maintain, but old and image-less — the recipe most likely to hand the owner a broken site |
| VitePress | 1.6 | Markdown-first, great search | Manual | Docs framework, wrong shape for a gallery |

**On rst:** technically possible (Sphinx/MkDocs pipelines exist), but **don't**. For this job rst is strictly worse: the JS/static-site ecosystem with image optimisation and CMS integrations is markdown-native; MkDocs/Sphinx are shaped like documentation (search, nav trees, code blocks), not portfolios; Pages CMS/Decap/Obsidian all speak markdown, essentially none speak rst; and the owner would never type either syntax anyway — he will use a CMS or hand photos to you. **Markdown is the right call; rst buys nothing and costs the gallery.**

**Astro detail:** one markdown file per project (`src/content/projekter/*.md`), schema-validated frontmatter (title, year, category, cover image, gallery images, description), one `Base.astro` holding all CSS (the ICV pattern — no design system, no Tailwind, nothing to maintain), `@astrojs/sitemap`, and images in `src/images/`.

---

## 4. Editing options — what "easy to edit" really means

The syntax is not the hard part. **The hard parts are the image field and the frontmatter**, in that order. Four levels, from cheapest to nicest:

| Level | Setup | Cost | Owner experience | Verdict |
|---|---|---|---|---|
| **0. He sends you content** | nothing | 0 | WhatsApps you photos; you commit | Valid fallback; not self-service. Decide with him, don't assume he wants a login. |
| **1. GitHub web editor** (github.com / github.dev) | nothing | 0 | Edits raw markdown + YAML in a code editor; image upload needs a path like `../../images/x.jpg`; poor on a phone | Free but this is exactly the part non-technical users break. ICV's README needs 100+ lines to explain it. |
| **2. [Pages CMS](https://pagescms.org/)** ← recommended | one `.pages.yml` (~40 lines) | **0** (MIT, self-hostable on Vercel as escape hatch) | Sign in with GitHub → pick site → named Danish fields, drag-and-drop media manager, **works on his phone** | The single biggest UX win available, and it needs no OAuth proxy or CMS server. No lock-in: delete the file and markdown editing still works. |
| **3. Decap CMS / TinaCMS** | `/admin` page + auth layer | 0–€29/month | Comparable, more moving parts | Not worth it at this scale; Decap needs an OAuth proxy (or its paid Turbo tier), Tina is paid beyond 2 users. |

**Recommended: markdown files as the truth + Pages CMS as the face.** Danish labels in `.pages.yml` ("Titel", "Kategori", "Billeder", "Beskrivelse"). New project = zero developer work: he adds a project, uploads photos, saves, Actions rebuilds in ~1–2 min.

Image rule to bake into the workflow: uploads at **≤ 2000 px long edge, JPEG q80 (~200–400 KB)** → ~150 photos ≈ 45 MB, inside both the 1 GB cap and the 10-minute build ceiling. Do **not** use git-lfs (Pages doesn't serve it). Squoosh is archived/should not be used; `sharp-cli` or the CMS's own resize is the replacement.

---

## 5. Instagram options

| Approach | Free? | Auto-updates? | Risk | Verdict |
|---|---|---|---|---|
| **Link / follow button / handle in header & footer** | yes | n/a | none | **Always ship this.** |
| **Curated gallery committed to the repo** (his best photos, captions, optional link to the post) | yes | no, by choice | none, fast, GDPR-clean, matches the design | **Primary gallery.** This is what visitors actually want to see. |
| Official per-post embed (`embed.js` + blockquote) | yes | yes, per post | Loads Meta JS on page load → third-party cookies; under GDPR/Fashion ID (CJEU C-40/17) that makes the site a joint controller, so Danish sites need consent/click-to-load. Blank boxes behind consent walls/content blockers; deleted post = empty hole; one embed code pasted per post | Optional: **one** consent-gated click-to-load embed, after testing on a real phone. |
| Instagram Graph API feed (`/me/media`) | yes (API) | yes | Business/Creator account + Meta App Review + token that must be rotated within 60 days + a scheduled Action. Basic Display API was shut down Dec 2024. Maintenance trap for a 0 kr site | **Don't.** |
| Third-party widgets (LightWidget/SnapWidget/Elfsight) | free tier w/ branding, then $15–120/yr | yes | Vendor holds the API connection, their cookies, their pricing; another account to keep alive | Only if "live grid" is a hard requirement — it isn't. |

**Recommended combo:** curated gallery + follow buttons, with an optional consent-gated single embed later. Treat Instagram as the *content source*, not an integration: he posts to Instagram as he already does; his best shots get copied into the site (he owns the photos, so rights are trivial).

---

## 6. Site structure

Danish copy throughout. Mobile-first, phone number visible on every screen. Six pages:

| Page | Purpose | Content |
|---|---|---|
| **Forside** | Convert in 5 seconds | Big hero photo of finished work, one-line pitch ("Snedker- og tømrerarbejde i Nærum og omegn"), 3–4 highlight photos, services teaser, phone CTA, Instagram link |
| **Projekter** | The portfolio (the whole point) | Grid of project cards → per-project page with photo gallery, short story, materials. This is the markdown-per-project collection. |
| **Ydelser** | What he sells | Confirmed services only: køkken, skabe/indbygget, bordplader, renovering, montage… Do not publish the affiliate portals' list unverified. |
| **Om** | Trust | Johann, years of experience, craftsmanship approach, guarantee/insurance if applicable |
| **Kontakt** | Action | Phone (`tel:`), email (`mailto:` — static sites have no server), address + map, Instagram DM option, CVR in footer |
| **Referencer** (optional) | Trust | Testimonials with permission — skip if he has none yet |

Extras that pay off, all cheap: LocalBusiness JSON-LD (name, address, phone, area), `og:image` + meta descriptions, sitemap, Danish `lang="da"`, and — biggest single SEO lever — a **Google Business Profile** pointing at the new site.

Also: **one-pager vs. 6 pages** — a one-pager is 30 % less build work and fine for a first launch, but per-project pages are what make a portfolio grow and what customers with a renovation job actually read. Recommend pages.

Language: **Danish now**, English later only if he wants the Rudersdal expat market — Astro i18n can be added without a rewrite, so don't pay for it upfront.

---

## 7. Three packages

| | **Lean** | **Recommended** | **Full** |
|---|---|---|---|
| Hosting | GitHub Pages at `github.io/JCleemannByg` | GitHub Pages on `jcleemannbyg.dk` | same as Recommended |
| Pages | 1 page (hero, gallery, services, contact) | 6 pages, one per-project collection, gallery lightbox | + EN version |
| Editing | markdown via GitHub web editor | **Pages CMS**, Danish labels, mobile upload | same |
| Instagram | follow buttons | curated gallery + follow buttons (+ consent-gated embed) | + live Widget (if he insists) |
| Extras | — | sitemap, JSON-LD, og:images, favicon, Danish README | + form via Formspree, Plausible/GoatCounter analytics, Google Business Profile walkthrough |
| Build effort | ~1 day | **~2–3 days** | +1–2 days |
| Recurring cost | 0 | **0** | 0–15 €/yr (form/analytics free tiers) |
| Who edits it | mostly you | **he can, himself** | he can |

---

## 8. What is needed from the owner (blockers for launch)

Condensed from the 11-item questionnaire in `research/company-profile.md`:

1. **CVR number** + legal form + founded year (expected in a Danish business footer).
2. **Full phone number** (publicly truncated to "42 58 11…") and preferred channel.
3. **Services he actually sells** — and whether he brands himself *snedker* or *tømrer*.
4. **Service area** — Nærum/Rudersdal only, or wider north Copenhagen.
5. **Photo set** — 15–25 good photos: finished work, details, a before/after, ideally a project or two with a short story. He owns his Instagram photos.
6. **Testimonials** + permission, guarantee scheme/insurance (if any).
7. **Hostinger DNS access** (or he changes the A record while you watch) — only for launch.
8. Whether **email `@jcleemannbyg.dk` is actually read** — the site will publish it.

---

## 9. Risks and yearly maintenance

| Risk | Mitigation |
|---|---|
| Pages CMS is effectively a **one-maintainer** MIT project | Escape hatch: self-host on Vercel in minutes; markdown remains editable without it |
| Astro **major upgrade** ~1×/yr | 30–60 min per upgrade; pinned versions, `package-lock.json` committed |
| **DNS edit kills email** | Keep nameservers + MX/SPF at Hostinger; only change A/CNAME for the web host |
| Huge phone photos bloat repo / hit 10-min deploy limit | 2000 px / JPEG q80 upload rule; `sharp` pipeline |
| Instagram embed breaks or annoys visitors on iOS | Optional, click-to-load, behind consent; gallery is the primary path |
| Silent drift like ICV's `main` vs `master` mismatch | Decide the branch name once; workflow + README + `git init` must agree. Also don't copy ICV's stale Action versions (`checkout@v4`/`deploy-pages@v4`) — pin current majors when scaffolding. |
| Owner never logs in | Level 0 fallback already works; site doesn't depend on him editing |

---

## 10. Decisions needed before scaffolding

> **Status 2026-11-09:** hosting (#1) = `github.io` project URL first; language (#5) = Danish + English; engine = Hugo recommended after the bake-off in [`FRAMEWORK.md`](FRAMEWORK.md). Current open items are listed at the end of FRAMEWORK.md; the list below is the original decision set, kept for reference.

1. **Domain:** launch straight on `jcleemannbyg.dk` (recommended) or start on `github.io/JCleemannByg` and point the domain later?
2. **Editing:** Pages CMS overlay (recommended), plain markdown + GitHub editor, or "he sends content to you"?
3. **Scope:** **Recommended package** (6 pages + project collection + Pages CMS) — or a one-pager first?
4. **Instagram:** curated gallery + follow buttons (recommended), plus the optional consent-gated embed, or a live third-party feed?
5. **Language:** Danish only now, or Danish + English from day one?
6. **DNS:** do you have (or can you get) Hostinger access, or should I write a step-by-step for him?

Once 1–3 are settled I can scaffold the repo (Astro project, content schema, Pages CMS config, Actions workflow, Danish README) and have a clickable preview the same day.
