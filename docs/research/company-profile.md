# J Cleemann Byg v/Johann Cleemann — evidence-based company profile

Research date: 2026-11-09. Method: public web only (no registry login, no browser JS).
Legend: **FACT** = observed on the cited source. **INFERENCE** = my reading, not stated by a source.
**UNKNOWN** = not found; verification path given. Sources listed at the bottom.

**Headline:** a genuine but almost invisible one-man joiner business. The only real
data source is the Eniro/Krak listing; the two "review portals" that mention him are
auto-generated affiliate sites and must not be used as fact. Domain is owned but no
site is live. No CVR number could be verified publicly.

## 1. Identity & registry

| Field | Value | Status |
|---|---|---|
| Trading name | "J Cleemann Byg V/Johann Cleemann" (exact wording on both Eniro brands) | FACT (krak, degulesider) |
| Person | **Johann Cleemann** — listed as the address/contact person name on the listing | FACT (krak, degulesider) |
| Person vs. business | "J Cleemann Byg" is the business; Johann Cleemann is the owner. The "J" is presumably Johann's initial | INFERENCE from naming convention |
| Legal form | Enkeltmandsvirksomhed ("V/" = "ved" is the Danish directory convention for sole traders) | INFERENCE — **not** registry-verified |
| CVR number | **UNKNOWN** | see §7 |
| Founded / registered date | **UNKNOWN** | see §7 |
| Industry code (branchekode) | **UNKNOWN**; category shown to users is "Snedker" (joiner) | FACT for category (krak) |
| Employees | none displayed ("Antal ansatte –"); gives no figures | FACT (krak) |
| Financials | none displayed ("Bruttofortjeneste –", "Afkastningsgrad –") | FACT (krak) |
| Eniro listing ID | 171060879 (identical ID on krak.dk and degulesider.dk) | FACT (krak, degulesider) |

Category inconsistency worth knowing: **Krak/Degulesider class it as "Snedker"**
(joiner/cabinetmaker), while the two auto-generated portals class it as **"Tømrer"**
(carpenter). Marketing copy has to pick one; the owner should decide (§7).

## 2. Contact data

| Field | Value | Status |
|---|---|---|
| Address | Nærum Hovedgade 15, 3. sal. tv-d, 2850 Nærum | FACT (krak, degulesider) |
| Coordinates | 55.818616, 12.530606 (OSM matches the Krak map pin 55.8186188, 12.5306101) | FACT (krak, OSM Nominatim) |
| Phone | shown only as "42 58 11..." (truncated behind "Vis nummer"); full 8 digits **UNKNOWN** | FACT for prefix (krak, degulesider) |
| Phone type | 42-series is a Danish mobile range → likely a mobile, consistent with a one-man firm | INFERENCE |
| Email | not published anywhere found. Domain has working mail infrastructure (§4) | UNKNOWN |
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

## 5. Instagram — could not be verified

- Handle `jcleemann_byg` is linked from the Krak **and** Degulesider profiles, so the
  account is known to Eniro's data (FACT, krak/degulesider).
- Direct fetch of `https://www.instagram.com/jcleemann_byg/` returns HTTP 200 but a
  JavaScript shell with no profile data (login wall). A rendering proxy (r.jina.ai)
  was redirected to `/accounts/login/`. Third-party viewers (imginn, picuki, greatfon)
  were blocked or returned no data. **Follower count, post count, caption language and
  content categories are UNKNOWN — do not guess them.**
- No indexed Instagram posts surfaced in any search engine, i.e. the account has no
  meaningful external footprint (INFERENCE: small/new/non-public content volume).

## 6. Competitive context (nearby comparable firms)

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

## 7. Open questions — content only the owner can supply

1. **CVR number + legal form + founded year** (from his CVR registration / virk.dk).
   Published CVR is expected on a Danish business site (and legally required in the
   footer / e-commerce contexts).
2. **Full phone number** and preferred channel (call, SMS, Instagram DM).
3. **Email to publish** — is `info@jcleemannbyg.dk` / `<name>@jcleemannbyg.dk` live on
   Titan? Who reads it?
4. **Which services he actually sells** — snedker vs tømrer; kitchens, built-ins,
   wardrobes, worktops, stairs, windows/doors, renovation, assembly, insurance jobs.
5. **Service area** — Nærum/Rudersdal only, or the wider north Copenhagen belt?
6. **Photos** — does he own rights to the Instagram photos? Needs a real project set
   (before/after, process, finished detail shots).
7. **Testimonials/references** + written permission to publish, and whether he is in a
   guarantee scheme (Byg Garanti e.l.) and carries ansvarsforsikring.
8. **Pricing stance** — no prices, or "fra"-prices, or "få et tilbud" only.
9. **Domain/hosting access** — Hostinger account and DNS control; decide whether to fix
   the current setup or move hosting.
10. **Google Business Profile** — does one exist? Claims/creates the local maps listing
    (biggest single SEO lever for a Nærum tradesman).
11. **Language** — Danish only, or Danish + English (large expat base in Rudersdal).

## Not confirmed (summary)

CVR, legal form, founding date, employees, financials, branchekode · full phone, email,
service area, hours · Instagram followers/posts/language · Google Business Profile and
reviews · whether the templated portal service list is actually his. Verification path
for the registry gaps: `datacvr.virk.dk` in a real browser (Cloudflare + JS block scripts),
or simply ask him for his CVR number — one question resolves items 1–3 above.

## Sources

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
