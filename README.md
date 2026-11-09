# J Cleemann Byg — hjemmeside

Statisk hjemmeside for **J Cleemann Byg v/ Johann Cleemann** (tømrer og snedker, Nærum).
Bygget med [Hugo](https://gohugo.io), **kun på dansk**, klar til GitHub Pages når den skal ud.

Der er **ingen JavaScript, ingen web fonts og ingen database** — kun HTML, CSS, markdown
og billeder. Alt indhold er tekstfiler, som kan redigeres uden at røre koden.

> **Status:** lokal prototype, klar til gennemsyn. Kontaktoplysninger og CVR er verificeret
> mod Håndværkerregistret, og porteføljen er bygget på Johanns egne Instagram-opslag.
> Resterende punkter står under "Placeholders".

---

## Kom i gang lokalt

Miljøet styres med [pixi](https://pixi.sh): Hugo, Python og Pillow kommer fra
conda-forge og låses i `pixi.lock`, så macOS, Linux og CI kører samme versioner.

```sh
pixi install          # opretter .pixi/ ud fra pixi.lock
pixi run dev          # lokal server → http://localhost:1313/
pixi run check        # byg + verificér (det samme som CI gør)
```

Andre tasks (`se listen i pixi.toml`):

| Task | Gør |
|---|---|
| `pixi run build` | Bygger til `public/` (kan styres med `BASE_URL=…`) |
| `pixi run verify` | Tjekker oversættelser, links, billeder og stier |
| `pixi run instagram` | Opdaterer Instagram-liste + forhåndsbilleder |
| `pixi run images` | Nedskalerer store billeder i `assets/images/` |
| `pixi run placeholders` | Genererer placeholder-teksturer |

**Uden pixi:** installér Hugo 0.169+ (`brew install hugo`) og kør `./scripts/dev.sh`.
Scriptene bruger også en lokal `bin/hugo`, hvis den findes.

Hugo er låst til **0.169.0** i `pixi.toml` og i deploy-workflowet — opgrader bevidst.

---

## Rediger indhold

Alt indhold ligger i markdown-filer under `content/da/`.

Indholdet kan redigeres direkte i filerne **eller** via [Pages CMS](https://pagescms.org),
som giver en dansk formular på telefonen og committer ændringerne til repoet. Opsætning,
hvad der kan redigeres (inkl. farver og typografi) og hvad der bevidst ikke kan:
[docs/pages-cms.md](docs/pages-cms.md).

| Fil | Side |
|---|---|
| `content/da/_index.md` | Forsiden (hero, fakta, om-blok, Instagram) |
| `content/da/projekter/_index.md` | Projektoversigt |
| `content/da/projekter/*.md` | Én fil pr. projekt |
| `content/da/ydelser/index.md` | Ydelser |
| `content/da/om/index.md` | Om værkstedet |
| `content/da/kontakt/index.md` | Kontakt |


### Frontmatter på et projekt

```yaml
---
title: "Radiatorskjuler på mål"                  # overskrift på siden
titel: "Radiatorskjuler på mål i Nærum"          # browserfanen / Google
beskrivelse: "Kort tekst til Google"             # meta description
kategori: "Indbygning"                           # vises over titlen
aar: 2026                                        # årstal
weight: 10                                       # rækkefølge (lav = først)
cover: "images/projekter/radiatorskjuler/01.jpg"
foer: "images/projekter/radiatorskjuler/07.jpg"    # valgfrit: før/efter-sektion
efter: "images/projekter/radiatorskjuler/01.jpg"
galleri:
  - "images/projekter/radiatorskjuler/02.jpg"
  - "images/projekter/radiatorskjuler/03.jpg"
resume: "Én-to linjer til projektkortet."
---
Brødteksten er almindelig markdown og vises under cover-billedet.
```

### Nyt projekt — fire trin

1. Læg billederne i `assets/images/projekter/<slug>/` (f.eks. `radiatorskjuler/`).
   Navngiv dem `01.jpg`, `02.jpg`, …
2. Kopiér et projekt i `content/da/projekter/` til `<slug>.md` og ret frontmatter.
   Vil du vise en før/efter-sammenligning, udfyld `foer` og `efter` med to billedstier.
3. `pixi run check` (eller `./scripts/build.sh` + `python3 scripts/verify.py`).
4. Committ og push — siden bygges automatisk, når GitHub Pages er sat op.

Rækkefølgen styres af `weight`: de tre laveste vægte vises som "Udvalgte projekter" på
forsiden.

---

## Billeder

- **Størrelse:** maks. 2000 px på den længste side, JPEG-kvalitet ca. 80 → 200–400 KB.
  Telefonbilleder skal skaleres ned først (fx i Fotos eller med `sips`).
- **Placering:** `assets/images/…`. Billeder refereres i frontmatter, aldrig i markdown —
  så bliver de automatisk skaleret og leveret som WebP i flere størrelser.
- **Alt-tekst** dannes ud fra projektets titel og billednummer.
- **Store uploads håndteres automatisk:** workflowet `.github/workflows/images.yml`
  nedskalerer alt over 2000 px og rekomprimerer, når der pushes billeder. Lokalt kan samme
  script køres med `pixi run images`.
- Hugo laver selv `srcset` og `width`/`height`, så der ikke sker layoutskift.

---

## Design og kode

| Fil | Gør |
|---|---|
| `assets/css/main.css` | Al CSS. Farver, typografi og afstande står i `:root` øverst. |
| `layouts/baseof.html` | Fælles HTML-skelet (header, main, footer) |
| `layouts/index.html` | Forsiden |
| `layouts/projekter/` | Projektoversigt + projektside |
| `layouts/ydelser/`, `om/`, `kontakt/` | De øvrige sider |
| `layouts/partials/` | Header, footer, sprogskifter, responsivt billede, projektkort |
| `hugo.toml` | Sprog, menu, adresse, telefon, e-mail, CVR |

Designet er bevidst enkelt: varm papirfarve, eg som accent, serif-overskrifter. Der er
ingen JavaScript; mobilmenuen er almindelig HTML/CSS.

**Design-tokens** (farver, typografi, bredde, hjørner, skygge) ligger i `data/design.yaml`
og bliver ved hvert build til CSS-variabler i `assets/css/tokens.css`. Strukturen i
`main.css` og `layouts/` er kode og ændres ikke via CMS'et.

---

## Instagram

Der er to måder at vise Instagram på, begge i `data/instagram.yaml`:

- **`posts`** (anbefalet): en liste af **links til konkrete opslag**. Hvert opslag vises
  som et felt; først ved klik indlæses Instagrams officielle embed — ingen login, ingen
  token, ingen cookies før klikket. Filen er nu fyldt med Johanns **6 nyeste opslag**
  (billeder og tekster hentet fra hans egen Instagram); ældre opslag tilføjes ved at
  kopiere linket i appen.
- **`items`**: kuraterede lokale billeder. Bruges automatisk som fallback når `posts` er
  tom (det er den nuværende tilstand).

**Opdatering sker automatisk:** `.github/workflows/instagram.yml` kører dagligt,
henter de nyeste opslag via `scripts/fetch_instagram.py`, gemmer nye forhåndsbilleder og
committer `data/instagram_posts.json` (kun hvis noget er ændret). Siden genbygges derefter
af deploy-workflowet. Fejler hentningen, bliver den forrige snapshot bare liggende.

Nye eller ældre opslag kan stadig tilføjes manuelt i `data/instagram.yaml` — kopiér linket
fra Instagram-appen ("⋯ → Kopiér link") og indsæt det sammen med et valgfrit
forhåndsbillede og en dansk tekst.
Baggrund, testresultater og de øvrige muligheder (LightWidget, SnapWidget, API):
[docs/instagram.md](docs/instagram.md).

Siden har også struktureret data (`sameAs` til Instagram og Krak), så Google kan knytte
profilen til virksomheden.

---

## Sprog

Siden er **kun på dansk** lige nu. Indholdet ligger i `content/da/`, knap- og
arialabels i `i18n/da.toml`, og der er ingen sprogskifter i designet.

Hvis engelsk skal tilbage, er det en genopretning fra git-historikken plus en ekstra
sproggruppe i CMS'et — fremgangsmåden står i
[docs/pages-cms.md](docs/pages-cms.md#sprog). `verify.py` registrerer automatisk, når der
kommer et sprog mere, og kræver så oversættelser og matchende i18n-nøgler.

---

## Placeholders — skal erstattes

- **Telefon, e-mail og CVR er verificeret** mod Håndværkerregistret: `+45 42 58 11 01`,
  `kontakt@jcleemannbyg.dk` (offentliggørelse bekræftet), CVR 43 89 14 99, stiftet 3. marts 2023.
- **Adresse:** Nærum Hovedgade 15, 2850 Nærum (etage/dør er udeladt på siden).
- **Instagram:** `jcleemann_byg` (bekræftet via Krak).
- **Billeder:** nu Johanns egne opslag (bekræftet til brug). De er Instagram-opløsning —
  originalerne vil gøre hero og projektsider skarpere.
- **Projekter og tekster:** de tre projekter er bygget på Johanns Instagram-opslag
  (radiatorskjuler med 7-billeders galleri, bogreol, skur). Teksterne er korte resuméer,
  som Johann bør godkende.
- **Om-siden** har `TODO(johann)`-noter i markdown (uddannelse, årstal, garanti).
- **Instagram-listen** opdateres automatisk og viser de nyeste 6 opslag.

Når teksterne er godkendt, kan `TODO(johann)`-kommentarerne i `content/` slettes.

---

## Publicering på GitHub Pages (ikke sat op endnu)

Workflowet ligger klar i `.github/workflows/deploy.yml` og gør ingenting, før repoet
findes og Pages er aktiveret.

1. Opret repo på GitHub (fx `JCleemannByg`) og push koden.
2. **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push til `main` — siden bygges og publiceres på
   `https://<brugernavn>.github.io/JCleemannByg/`.
4. Workflowet bygger med `baseURL` ud fra repoets navn og kører `verify.py` før deploy.

### Workflows

| Workflow | Gør |
|---|---|
| `deploy.yml` | Bygger med pixi og publicerer til Pages; kører `verify.py` før upload |
| `instagram.yml` | Dagligt: opdaterer Instagram-liste + forhåndsbilleder og committer |
| `images.yml` | Ved billedpushes: nedskalerer store fotos og committer |

De to sidste committer med `GITHUB_TOKEN`, og derfor lytter `deploy.yml` også på
`workflow_run`, så siden genbygges bagefter.

### Eget domæne senere

`jcleemannbyg.dk` ejes allerede. Når den skal pege på siden:

1. Ret A-records hos Hostinger til GitHubs fire IP'er, og `www` CNAME til
   `<brugernavn>.github.io` — **MX/SPF må ikke ændres**, ellers holder mail op.
2. Sæt `baseURL` til `https://jcleemannbyg.dk/` i `.github/workflows/deploy.yml`.
3. Settings → Pages → Custom domain + Enforce HTTPS.

---

## Vedligehold

- **Hugo-versionen er låst** til `0.169.0` i `pixi.toml`, `pixi.lock` og deploy-workflowet.
  Opgrader bevidst — Hugo omdøber jævnligt config-nøgler.
- **CI og lokalt er nu ens**: workflowene bruger `prefix-dev/setup-pixi` + `pixi.lock`, så
  deploy bygger med præcis samme Hugo/Python som lokalt.
- Kør `scripts/verify.py` ved hver ændring (den ligger også i workflowet).
- Hold billeder under 400 KB, ellers vokser repoet og deploy-tiden.

---

## Struktur

```
pixi.toml / pixi.lock     værktøjer: Hugo 0.169, Python, Pillow + tasks
hugo.toml                 sprog og menu
content/da/               alt indhold (markdown + frontmatter)
data/                     kontaktoplysninger, design-tokens, Instagram-lister
assets/css/main.css       design (struktur)
assets/css/tokens.css     design-tokens (genereret fra data/design.yaml)
assets/images/            billeder (hero, projekter, om, Instagram)
layouts/                  skabeloner
i18n/da.toml              knap- og aria-tekster
scripts/                  dev, build, verify, Instagram- og placeholder-scripts
.pages.yml                redigeringsfladen til Pages CMS
docs/                     projektnotater (ikke en del af siden)
```
