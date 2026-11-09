# J Cleemann Byg — hjemmeside

Statisk hjemmeside for **J Cleemann Byg v/ Johann Cleemann** (tømrer og snedker, Nærum).
Bygget med [Hugo](https://gohugo.io), **dansk på `/` og engelsk på `/en/`**, klar til
GitHub Pages når den skal ud.

Der er **ingen JavaScript, ingen web fonts og ingen database** — kun HTML, CSS, markdown
og billeder. Alt indhold er tekstfiler, som kan redigeres uden at røre koden.

> **Status:** lokal prototype. Alle telefonnumre, e-mails, CVR-numre, projekttekster og
> billeder er placeholder og skal erstattes med rigtige oplysninger (se "Placeholders").

---

## Kom i gang lokalt

Miljøet styres med [pixi](https://pixi.sh): Hugo, Python og Pillow kommer fra
conda-forge og låses i `pixi.lock`, så macOS, Linux og CI kører samme versioner.

```sh
pixi install          # opretter .pixi/ ud fra pixi.lock
pixi run dev          # lokal server → http://localhost:1313/  (engelsk: /en/)
pixi run check        # byg + verificér (det samme som CI gør)
```

Andre tasks (`se listen i pixi.toml`):

| Task | Gør |
|---|---|
| `pixi run build` | Bygger til `public/` (kan styres med `BASE_URL=…`) |
| `pixi run verify` | Tjekker oversættelser, links, billeder og stier |
| `pixi run instagram` | Opdaterer Instagram-liste + forhåndsbilleder |
| `pixi run placeholders` | Genererer placeholder-teksturer |

**Uden pixi:** installér Hugo 0.169+ (`brew install hugo`) og kør `./scripts/dev.sh`.
Scriptene bruger også en lokal `bin/hugo`, hvis den findes.

Hugo er låst til **0.169.0** i `pixi.toml` og i deploy-workflowet — opgrader bevidst.

---

## Rediger indhold

Alt indhold ligger i markdown-filer. **Hver side findes to gange** — én på dansk og én på
engelsk — med samme filnavn i `content/da/` og `content/en/`.

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

Engelsk: samme struktur under `content/en/`.

### Frontmatter på et projekt

```yaml
---
title: "Køkken i massiv eg"          # overskrift på siden
titel: "Køkken i massiv eg i Nærum"  # browserfanen / Google
beskrivelse: "Kort tekst til Google" # meta description
kategori: "Køkken"                   # vises over titlen
aar: 2025                            # årstal
weight: 10                           # rækkefølge (lav = først)
cover: "images/projekter/koekken-eg/01.jpg"
galleri:
  - "images/projekter/koekken-eg/02.jpg"
  - "images/projekter/koekken-eg/03.jpg"
resume: "Én-to linjer til projektkortet."
---
Brødteksten er almindelig markdown og vises under cover-billedet.
```

### Nyt projekt — fem trin

1. Læg billederne i `assets/images/projekter/<slug>/` (f.eks. `koekken-holte/`).
   Navngiv dem `01.jpg`, `02.jpg`, …
2. Kopiér et projekt i `content/da/projekter/` til `<slug>.md` og ret frontmatter.
3. Kopiér det samme til `content/en/projekter/<slug>.md` (samme filnavn, engelsk tekst,
   samme `cover`/`galleri`-stier).
4. `./scripts/build.sh` og `python3 scripts/verify.py --public public --base /`.
5. Committ og push — siden bygges automatisk, når GitHub Pages er sat op.

Rækkefølgen styres af `weight`: de tre laveste vægte vises som "Udvalgte projekter" på
forsiden.

---

## Billeder

- **Størrelse:** maks. 2000 px på den længste side, JPEG-kvalitet ca. 80 → 200–400 KB.
  Telefonbilleder skal skaleres ned først (fx i Fotos eller med `sips`).
- **Placering:** `assets/images/…`. Billeder refereres i frontmatter, aldrig i markdown —
  så bliver de automatisk skaleret og leveret som WebP i flere størrelser.
- **Alt-tekst** dannes ud fra projektets titel og billednummer; vil du have en bedre
  beskrivelse, kan `alt` tilføjes til galleri-objekterne senere.
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
forhåndsbillede og en dansk/engelsk tekst.
Baggrund, testresultater og de øvrige muligheder (LightWidget, SnapWidget, API):
[docs/instagram.md](docs/instagram.md).

Siden har også struktureret data (`sameAs` til Instagram og Krak), så Google kan knytte
profilen til virksomheden.

---

## Sprog

- Dansk er standardsprog og ligger i `/`.
- Engelsk ligger i `/en/`.
- UI-tekster (knapper, labels) står i `i18n/da.toml` og `i18n/en.toml`.
- Sprogskifteren på hver side bevarer den side, du står på, hvis oversættelsen findes.
- `hreflang` og `x-default` sættes automatisk (x-default peger altid på dansk).
- Oversættelser parres af **filnavnet**: `content/da/projekter/x.md` ↔ `content/en/projekter/x.md`.
  Mangler tvillingen, fejler `verify.py` og deploy stopper. Se
  [docs/pages-cms.md#sprog--dansk-og-engelsk](docs/pages-cms.md) for CMS-arbejdsgangen.

---

## Placeholders — skal erstattes

- **Telefon, e-mail og CVR er verificeret** mod Håndværkerregistret: `+45 42 58 11 01`,
  `kontakt@jcleemannbyg.dk` (offentliggørelse bekræftet), CVR 43 89 14 99, stiftet 3. marts 2023.
- **Adresse:** Nærum Hovedgade 15, 2850 Nærum (etage/dør er udeladt på siden).
- **Instagram:** `jcleemann_byg` (bekræftet via Krak).
- **Billeder:** nu Johanns egne opslag (bekræftet til brug). De er Instagram-opløsning —
  originalerne vil gøre hero og projektsider skarpere.
- **Projekter og tekster:** eksempler; de tre projekter er ikke rigtige opgaver.
- **Om-siden og kontakt-siden** indeholder `TODO(johann)`-noter i markdown.

Når de rigtige oplysninger er på plads, kan placeholder-linjerne i `hugo.toml` og
`content/` slettes.

---

## Publicering på GitHub Pages (ikke sat op endnu)

Workflowet ligger klar i `.github/workflows/deploy.yml` og gør ingenting, før repoet
findes og Pages er aktiveret.

1. Opret repo på GitHub (fx `JCleemannByg`) og push koden.
2. **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Push til `main` — siden bygges og publiceres på
   `https://<brugernavn>.github.io/JCleemannByg/`.
4. Workflowet bygger med `baseURL` ud fra repoets navn og kører `verify.py` før deploy.

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
- **CI og lokalt kan gøres helt ens** ved at skifte workflowet til `prefix-dev/setup-pixi` +
  `pixi run check`; det er ikke gjort endnu, da deploy-workflowet ikke er afprøvet på GitHub.
- Kør `scripts/verify.py` ved hver ændring (den ligger også i workflowet).
- Hold billeder under 400 KB, ellers vokser repoet og deploy-tiden.

---

## Struktur

```
hugo.toml                 sprog, menu, kontaktoplysninger
content/da|en/            alt indhold, to sprog
assets/css/main.css       design
assets/images/            billeder (hero, projekter, om, Instagram)
layouts/                  skabeloner
i18n/                     UI-tekster
scripts/                  dev, build, verify, placeholder-generator
docs/                     projektnotater (ikke en del af siden)
```
