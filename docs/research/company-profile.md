# J Cleemann Byg v/Johann Cleemann — evidence-based company profile

Research date: 2026-11-09. Method: public web only (no registry login, no browser JS).
Legend: **FACT** = observed on the cited source. **INFERENCE** = my reading, not stated by a source.
**UNKNOWN** = not found; verification path given. Sources listed at the bottom.

**Headline:** a genuine but almost invisible one-man tradesman business. Registry data
was subsequently found via **Håndværkerregistret** (CVR 43 89 14 99, founded 2023-03-03,
sole trader, branchekode 433200). The Eniro/Krak listing remains the source for the
address/phone; the two "review portals" that mention him are auto-generated affiliate
sites and must not be used as fact. The domain is owned, but no site was ever served.

## 1. Identity & registry

| Field | Value | Status |
|---|---|---|
| Trading name | "J Cleemann Byg V/Johann Cleemann" (exact wording on both Eniro brands) | FACT (krak, degulesider) |
| Person | **Johann Cleemann** — listed as the address/contact person name on the listing | FACT (krak, degulesider) |
| Person vs. business | "J Cleemann Byg" is the business; Johann Cleemann is the owner. The "J" is presumably Johann's initial | INFERENCE from naming convention |
| Legal form | **Enkeltmandsvirksomhed** (sole trader) | FACT (Håndværkerregistret) |
| CVR number | **43 89 14 99** | FACT (Håndværkerregistret, 2026-11-09) |
| Founded / registered date | **3 March 2023** (stiftelsesdato 03-03-2023) | FACT (Håndværkerregistret) |
| Industry code (branchekode) | **433200** (tømrerarbejde); registry category "Tømrere"; Krak category "Snedker" | FACT (Håndværkerregistret + krak) |
| Employees | none displayed ("Antal ansatte –"); gives no figures | FACT (krak) |
| Financials | none displayed ("Bruttofortjeneste –", "Afkastningsgrad –") | FACT (krak) |
| Eniro listing ID | 171060879 (identical ID on krak.dk and degulesider.dk) | FACT (krak, degulesider) |

Category inconsistency worth knowing: **Krak/Degulesider class it as "Snedker"**
(joiner/cabinetmaker), while **Håndværkerregistret files him under "Tømrere" with
branchekode 433200 (tømrerarbejde)** — and his own posts show both framing/insulation and
built-in furniture. The site therefore says "Tømrer & snedker", which is defensible; the
owner should still confirm the preferred headline. Note: Håndværkerregistret also shows
both "Reklamebeskyttelse: Ja" and "Nej" in two blocks — contradictory, do not rely on it.

## 2. Contact data

| Field | Value | Status |
|---|---|---|
| Address | Nærum Hovedgade 15, 2850 Nærum (Krak adds "3. sal. tv-d"; registry shows street only) | FACT (krak, degulesider, Håndværkerregistret) |
| Coordinates | 55.818616, 12.530606 (OSM matches the Krak map pin 55.8186188, 12.5306101) | FACT (krak, OSM Nominatim) |
| Phone | **42 58 11 01** (full number; Krak truncates it behind "Vis nummer", registry shows it) | FACT (Håndværkerregistret) |
| Phone type | 42-series is a Danish mobile range → likely a mobile, consistent with a one-man firm | INFERENCE |
| Email | **kontakt@jcleemannbyg.dk** (Cloudflare-obfuscated on the registry page; decodes to this address, matching the Titan mail setup on the domain) | FACT (Håndværkerregistret, decoded) |
| Website | `jcleemannbyg.dk` listed by the registry, but nothing was ever served there | FACT (registry + DNS/TLS probes) |
| Service area | not stated by any reliable source | UNKNOWN |
| Opening hours | "Man-Fre 07:00-16:30" appears **only** on the templated portals | UNVERIFIED — assume boilerplate |

## 3. Services

The only service wording that exists publicly is on two templated affiliate pages
(tomrer-oversigt-danamark.dk, dansk-service-hub.dk). Both share the same author name,
the same partner links to 3byggetilbud.dk, and near-identical copy, i.e. they are
**programmatically generated profiles**, not the owner describing himself:

> "Pålidelig tømrer dækker Nærum og omegn. Få et uforpligtende tilbud på dit projekt."
> Specialopgaver: Køkken montage · Skabsmontering · Bordplader · Renovering · Tilpasning

Treat that list as a **hypothesis to confirm with the owner**, not as his service list
(VERDICT: UNVERIFIED). Nothing links him to tag/tagrenovering, vinduer, tilbygning,
altan or badeværelse in any source — do not invent those.

## 4. Existing web presence (most actionable finding)

| Item | Finding | Status |
|---|---|---|
| Domain | `jcleemannbyg.dk` **is registered** | FACT (DNS) |
| DNS | NS `ns1/ns2.dns-parking.com` (= Hostinger parking DNS) | FACT (dig) |
| A record | `72.60.81.210` for both apex and `www` (Hostinger shared hosting IP) | FACT (dig) |
| Website | **not live.** `http://` returns 308 → `https://`, but the TLS handshake fails (alert 80, "no peer certificate available") | FACT (curl + openssl) |
| Email | MX `mx1/mx2.titan.email` (Titan, Hostinger's mail partner), `v=spf1 include:spf.titan.email ~all` | FACT (dig) |
| Wayback Machine | **zero** captures for the domain → it has never served an archived public site | FACT (CDX API, empty result) |
| Other domains | `jcleemannbyg.com` and `jcleemann.dk` do not resolve | FACT (dig) |
| Google Business / Maps | could not be read (Google redirects to consent.google.com); no reviews found via any accessible source | UNKNOWN |
| Trustpilot | no profile found | FACT (404/403) |
| Other socials | none found; only Instagram is linked from the listings | FACT (krak, degulesider) |

**Practical read (INFERENCE):** he already owns the brand domain and runs email on it,
so a new site can be launched at `jcleemannbyg.dk` without buying anything — but the
DNS/hosting is in a half-configured state typical of a started-then-abandoned setup.
Anyone building the site needs his Hostinger login (or DNS delegation).

Search-footprint reality check: Bing returns **zero** organic results for the exact
name; Mojeek zero; DuckDuckGo blocks bots. The entire indexable web presence is Krak +
Degulesider + the two templated portals. SEO upside is large; starting point is zero.

## 5. Instagram — verified 2026-11-09 (public, no login needed for the embed endpoint)

- Handle **@jcleemann_byg**, display name **Johann Cleemann**, account is **public**.
- Counts: **20 posts, 89 followers, 45 following** (from the public `og:description` and the
  profile-embed payload).
- No bio, external URL, business category or contact fields are exposed publicly — it
  behaves like a personal account, not a business profile.
- The **public profile-embed endpoint** (`/jcleemann_byg/embed/` with a mobile user agent)
  returns the **6 newest posts** with captions and image URLs; older posts are not exposed.
- Captions confirm the actual craft (Danish original, abbreviated):
  - "Radiatorskjuler på mål — 2 hængslede låger og en på magneter" (made-to-measure
    radiator cover, two hinged doors + magnetic door) — 7-image carousel.
  - "…en bogreol jeg har bygget" (built-in bookcase around a door).
  - "Taget er saneret…" (roof cleaned, then insulation).
  - "Sådan sætter man limtræ op på 35 sekunder" (glulam/timber assembly).
  - Workshop shots: cutting timber, building the radiator cover.
- Collaborators mentioned in captions: `@rchaandvaerkservice` and `@charliey.o.j`
  (relationship not verified — not used in site copy).

**Consequence for the copy:** the site's services were rewritten around what the posts
actually show (built-in furniture, outdoor work, renovation/insulation, assembly). The
"kitchens" wording from the auto-generated affiliate portals was **not** confirmed and has
been removed from the site copy until Johann confirms it.

## 6. Instagram — what could not be confirmed

- Until Håndværkerregistret was provided, no CVR/phone/e-mail could be confirmed:
  `datacvr.virk.dk` is bot-blocked, `cvrapi.dk` returns quota exceeded, and Krak hides the
  phone behind a click. **All three are now resolved in §1–§2 via the registry.**

## 6b. Instagram — what could not be verified

- Handle `jcleemann_byg` is linked from the Krak **and** Degulesider profiles, so the
  account is known to Eniro's data (FACT, krak/degulesider).
- Direct fetch of `https://www.instagram.com/jcleemann_byg/` returns HTTP 200 but a
  JavaScript shell with no profile data (login wall). A rendering proxy (r.jina.ai)
  was redirected to `/accounts/login/`. Third-party viewers (imginn, picuki, greatfon)
  were blocked or returned no data. **Follower count, post count, caption language and
  content categories are UNKNOWN — do not guess them.**
- No indexed Instagram posts surfaced in any search engine, i.e. the account has no
  meaningful external footprint (INFERENCE: small/new/non-public content volume).

## 7. Competitive context (nearby comparable firms)

- **Tømrer-Snedkerfirmaet Jørgen Spange ApS**, Lyngby/Holte/Gentofte — `spange.dk`:
  the strongest local template. Positioning "over 30 års erfaring", trust via svende/
  apprentices and references; nav = Kompetencer, Referencer, Om, Svende, Kontakt;
  per-service pages (nyt tag, vinduer & døre, tilbygninger, kirker, boligselskaber,
  erhvervslejemål, forsikringsskader, hovedentrepriser, kontorindretning) + "Indhent
  et tilbud" CTA. (FACT, fetched)
- **Tømrer & Snedkermester Christian Overgaard ApS**, Holte — `christianovergaard.dk`
  resolves but serves a bare "One Photo" placeholder page, i.e. effectively no website. (FACT, fetched)
- **DT Byggeservice ApS**, Nærum Hovedgade 85 — `dtbyggeservice.dk` exists but returns a
  JS/bot-check interstitial; content not readable. Presence of a site is the fact. (FACT, fetched)
- **Ml Håndværk ApS**, Holte — appears as a "similar company" in Krak; no website found. (FACT for listing)

Baseline for a site in this niche: 5–8 pages, service pages with real project photos,
"referencer" page, about-the-craftsman page, phone visible on every screen, Danish copy,
and a simple quote-request form. Mobile-first is essential (all traffic will be local).

## 8. Open questions — content only the owner can supply

**Resolved via Håndværkerregistret (2026-11-09):** CVR 43 89 14 99, legal form
(enkeltmandsvirksomhed), founded 3 March 2023, branchekode 433200, full phone
42 58 11 01, e-mail kontakt@jcleemannbyg.dk.

**Still open:**

1. **Which services he actually sells and wants advertised** — the site now lists what the
   Instagram posts show (built-ins, outdoor work, renovation/insulation, assembly). Kitchen
   work from the auto-generated portals is *not* confirmed and was removed from the copy.
2. **Service area** — Nærum/Rudersdal only, or the wider north Copenhagen belt?
3. **Photos** — originals (the site currently uses Instagram-resolution images).
4. **Testimonials/references** + written permission, and whether he is in a guarantee
   scheme (Byg Garanti e.l.) and carries ansvarsforsikring.
5. **Pricing stance** — no prices, or "fra"-priser, or "få et tilbud" only.
6. **Domain/hosting access** — Hostinger account/DNS, to point `jcleemannbyg.dk` at the new
   site (email MX must be preserved).
7. **Google Business Profile** — biggest single local-SEO lever.
8. **Language** — Danish only, or Danish + English (both are built now).

## Not confirmed (summary)

Still unconfirmed: employees/financials, service area, real opening hours, Google Business
Profile and reviews, whether the templated portal service list is actually his, and whether
he wants kitchens advertised. Also unverified: the contradictory "Reklamebeskyttelse"
values on the registry page.

Now confirmed via Håndværkerregistret: CVR 43 89 14 99 · enkeltmandsvirksomhed · founded
03-03-2023 · branchekode 433200 (tømrerarbejde) · phone 42 58 11 01 · e-mail
kontakt@jcleemannbyg.dk. Instagram: 20 posts, 89 followers, public, 6 latest posts readable
without login.

## Sources

- https://håndværkerregistret.dk/j-cleemann-byg-v-johann-cleemann/ (CVR, phone, e-mail, founding date; fetched via punycode 2026-11-09)

- https://www.krak.dk/j+cleemann+byg+v%252fjohann+cleemann+n%c3%a6rum/171060879/firma
- https://www.degulesider.dk/j+cleemann+byg+v%252fjohann+cleemann+n%c3%a6rum/171060879/firma
- https://tomrer-oversigt-danamark.dk/profil/j-cleemann-byg-vjohann-cleemann-2850 (templated, low trust)
- https://dansk-service-hub.dk/profil/j-cleemann-byg-vjohann-cleemann-2850 (templated, low trust)
- https://datacvr.virk.dk/soegeresultater — JS-only, no data extractable without a browser
- https://nominatim.openstreetmap.org — address geocoding (55.818616, 12.530606)
- DNS/TLS: `dig` for NS/MX/TXT/A, `curl`/`openssl s_client` against jcleemannbyg.dk
- Wayback CDX API: http://web.archive.org/cdx/search/cdx?url=jcleemannbyg.dk (empty)
- https://www.instagram.com/jcleemann_byg/ — login wall, no data
- https://spange.dk/ ; https://christianovergaard.dk/ ; https://dtbyggeservice.dk/
