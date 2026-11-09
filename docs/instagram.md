# Instagram — hvordan siden håndterer det

**Kort version:** Siden viser et **kurateret galleri** af udvalgte billeder, gemt lokalt, med
links til Instagram og en tydelig "følg"-knap. Der hentes **ingen live-data** fra Instagram,
og der indlæses **ingen tredjeparts-scripts**. Det er et bevidst valg, ikke en mangel.

## Hvad der er bygget nu

| Element | Hvor |
|---|---|
| Galleri med 3–6 udvalgte billeder | `data/instagram.yaml` + `.ig`-sektionen på forsiden |
| Link til hvert opslag (eller profilen) | `url` pr. element i samme fil |
| Tosprogede billedtekster | `caption.da` / `caption.en` |
| "Følg @jcleemann_byg"-knap | Forside, kontakt og footer |
| `sameAs` til Instagram i struktureret data | `layouts/partials/jsonld.html` (hjælper Google med at knytte profilen til virksomheden) |
| Ingen cookies eller tredjeparts-kald | Hele siden er statisk |

### Sådan opdaterer du galleriet

1. Gem billedet fra Instagram (eller den originale fil) i `assets/images/instagram/`.
2. Ret `data/instagram.yaml`: `image`, `url` (link til opslaget) og `caption.da` / `caption.en`.
3. Byg og verificér: `./scripts/build.sh && python3 scripts/verify.py --public public --base /`

Billederne bliver automatisk skaleret og leveret som WebP i flere størrelser.

## Kan siden vise "alt fra Instagram" automatisk?

Ja — men ikke med én officiel indbygningsløsning, og ikke helt gratis uden afvejninger.
Verificeret 2026-11-09:

| Løsning | Opdateres | Pris | Vigtigt |
|---|---|---|---|
| **Instagram-embed af profilen** (iframe `instagram.com/<bruger>/embed/`) | — | — | **Umuligt:** Instagram svarer med `X-Frame-Options: DENY`, så profilen kan ikke indlejres. Officiel embed findes kun pr. opslag, ikke som grid. |
| **SnapWidget, gratis** | **hvert 15. minut** | 0 | 5 layouts, ubegrænsede widgets/visninger, foto-tilpasning. **Ulempe:** klik på et foto åbner en SnapWidget-side i stedet for Instagram-opslaget. Links til Instagram + 5-min opdatering kræver Lite (8 $/md). |
| **LightWidget, gratis** | hvert 24. time | 0 | **HTTPS er slået fra i gratisversionen** (deres egen sammenligningstabel), så den kan ikke bruges på GitHub Pages. |
| **LightWidget, upgraded** | **hvert 30. minut** | **15 $ én gang pr. widget** | HTTPS, CDN, ingen watermark, mail ved udløbet token. Token udløber ca. hver 3. måned og fornyes i deres dashboard. |
| **Egen pipeline (GitHub Actions + Instagram API)** | fx hvert 6.–24. time | 0 | Kræver Instagram **professionel konto** (Business/Creator), Meta-app, langlivet token (~60 dage) og et planlagt build. Ingen tredjeparts-kode på siden, fuld designkontrol. Mest vedligehold. |
| **Uofficielle scrapers** | — | — | **Nej.** Bryder Instagrams vilkår og holder op med at virke uden varsel. |

Bemærk: heller ikke en widget viser "alt" — den viser de nyeste N opslag (ofte 12–24 med
"load more"). Det er også det rigtige: porteføljen på siden skal være kurateret, ikke et
spejl af hele arkivet.

## Anbefaling

**LightWidget upgraded til 15 $ én gang** er den bedste kombination for denne side: klik
går til Instagram-opslaget, opdatering hvert 30. minut, ingen branding, HTTPS virker, og
der er ingen månedlig udgift. SnapWidget gratis er alternativet, hvis 0 kr. er et krav —
men så lander besøgende på en SnapWidget-side ved klik.

Den kuraterede sektion bevares som **fallback**: Hvis widgetten ikke kan indlæses, viser
siden stadig de udvalgte billeder fra `data/instagram.yaml`. Det er også det, der sker nu.

## Valgt løsning: en fil med links (ingen login)

Siden bruger Instagrams **officielle embeds pr. opslag**, styret af en liste i
`data/instagram.yaml`:

```yaml
posts:
  - url: "https://www.instagram.com/p/ABC123/"
    image: "images/instagram/01.jpg"   # valgfrit forhåndsbillede (anbefales)
    caption:
      da: "Køkken i massiv eg"
      en: "Kitchen in solid oak"
```

- Hvert opslag vises som et felt med (valgfrit) forhåndsbillede og teksten "Vis opslag".
- **Først når besøgende klikker, indlæses Instagrams `embed.js`** og opslaget vises —
  ingen tredjeparts-cookies eller scripts ved sideindlæsning. Er `posts` tom, er der
  stadig 0 bytes JavaScript på siden.
- "Åbn på Instagram" og luk-knap hører til panelet; Escape lukker det.
- Er `posts` tom, vises det kuraterede galleri (`items`) i stedet — det er den nuværende
  tilstand, indtil de første links er lagt ind.

**Testet 2026-11-09** med offentlige opslag: embeddet renderer uden login, og panelet
indlæses korrekt i sidens design (se `docs/preview/ig-tiles.png` og
`docs/preview/ig-embed.png`).

**Begrænsning, som er værd at sige højt:** listen opdaterer sig ikke af sig selv. Nye
opslag kræver, at der lægges et link ind — 30 sekunders arbejde pr. opslag, ingen login,
ingen tokens, intet der kan udløbe. Det er byttet for at slippe for API-vedligehold.

## Hvordan de første opslag blev fundet (uden login)

Profilens **offentlige embed-endpoint** (`https://www.instagram.com/jcleemann_byg/embed/`,
åbnet med en mobil browser-UA) returnerer profilens kontekst som JSON — inklusive de
**6 nyeste opslag** med shortcodes, billed-URL'er og tekst. Det blev brugt én gang manuelt
til at hente:

- 6 post-links → `data/instagram.yaml`
- 6 forhåndsbilleder (skaleret til 900 px) → `assets/images/instagram/posts/`
- de originale danske tekster (kortet ned) + engelsk oversættelse til alt/aria

Johann har bekræftet, at opslagene og billederne må bruges på siden.

Regnskabet for kontoen: **@jcleemann_byg (J Cleemann Byg / Johann Cleemann)**,
20 opslag, 89 følgere. Embed-endpointet viser kun de nyeste 6; ældre opslag lægges ind ved
at kopiere linket i Instagram-appen.

Vigtigt: **siden skraber ikke**. Den viser kun de links, der står i filen, plus lokale
forhåndsbilleder. Endpointet kan ændre sig uden varsel — derfor er det kun brugt som
engangs-hjælp, ikke som en afhængighed.

## Automatisk opdatering (GitHub Actions)

Ja — det er relativt enkelt, og det er bygget. To filer:

| Fil | Gør |
|---|---|
| `scripts/fetch_instagram.py` | Henter det offentlige embed-endpoint, udtrækker de nyeste opslag, downloader manglende forhåndsbilleder (900 px) og skriver `data/instagram_posts.json`. Oversættelser og rækkefølge bevares. |
| `.github/workflows/instagram.yml` | Kører scriptet **dagligt kl. 03:17 UTC** (og manuelt), committer kun hvis noget ændrede sig, og lader deploy-workflowet genbygge siden. |

Sådan hænger det sammen:

- Siden læser **kun** `data/instagram_posts.json` + de lokale billeder. Instagram kaldes
  aldrig fra browseren.
- Workflowet fejler ikke siden: kan endpointet ikke nås, eller ændrer Instagram sin
  embed-side, bliver den forrige snapshot bare liggende (scriptet afslutter med fejl, men
  jobbet fortsætter, og intet committes).
- Billeder hentes kun, hvis de mangler — så et dagligt kør ikke skaber støjende diffs.
- Engangsopsætning i repoet: **Settings → Actions → General → Workflow permissions →
  "Read and write permissions"**, ellers må jobbet ikke committe.
- Fordi commits lavet med det indbyggede `GITHUB_TOKEN` ikke udløser andre workflows, har
  `deploy.yml` også et `workflow_run`-trigger, så siden genbygges efter hver opdatering.

**Forbehold:** endpointet er offentligt og kræver ingen login, men det er ikke en officiel
API. Det kan rate-limite, ændre struktur eller blive lukket. Derfor er kadencen daglig
(lav belastning), og hele anlægget kan slås fra ved at slette workflow-filen — så holder
den manuelle links-fil bare ved. Til en lille håndværksside er det en rimelig afvejning.

## Uden Instagram-login? — efterprøvet 2026-11-09

Kort svar: **Nej, ikke for en automatisk feed.** Instagram kræver, at ejeren af kontoen
logger ind og giver tilladelse, før nogen må læse opslagene. Vi har prøvet de anonyme veje:

| Forsøg | Resultat |
|---|---|
| `instagram.com/api/v1/users/web_profile_info?username=…` | **404** (login-væg) |
| `api.instagram.com/oembed/?url=…` uden token | **302** til login |
| Profilens HTML uden login | 511 KB login-side, **0 opslag** i markup |
| Læse-proxy (`r.jina.ai`) på profilen | Omdirigeret til `/accounts/login/` |
| Indlejre profilen i iframe | Blokeret: `X-Frame-Options: DENY` |
| SnapWidget: skrive et brugernavn | Ifølge deres docs **umuligt**: "You cannot show an Instagram account by typing in its username… only after the owner… signs in and gives permission." |
| SnapWidget hashtag-widget | Kræver business/creator-konto **linket til en Facebook-side** + Pro-plan → stadig login |
| LightWidget gratis | 24 t opdatering og **HTTPS slået fra** → kan ikke bruges på GitHub Pages |

SnapWidget har dog en "Send For Auth"-model på betalte planer: man sender ejeren et link,
og **ejeren logger selv ind** — man deler aldrig adgangskode. LightWidget kræver tilsvarende,
at kontoen forbindes én gang.

**Konklusion:** den eneste legitime vej til en automatisk feed er **én enkelt, frivillig
login fra Johanns side** (2 minutter), hvorefter widgetten opdaterer sig selv. Uden den er
de ærlige muligheder:

1. **Kurateret galleri** (nuværende) — 0 kr, ingen login, ingen cookies, bedst design.
2. **Officielle indlejringer pr. opslag** — kræver ingen login, kun at Johann sender 2–3
   opslagslinks; men det er manuelt pr. opslag og indlæser Metas script.

Alt andet (scrapere, "vis bare brugernavn"-services) bryder vilkårene og holder op med at
virke uden varsel.

## Testet lokalt (2026-11-09)

En offentlig LightWidget-demo (masonry) blev sat i `instagram_widget` og bygget lokalt:

- **Widgetten virker:** den indlæses via iframe, viser et levende grid med links til
  Instagram og har hverken logo eller reklamer.
- **Den arver ikke sidens typografi.** Farver, kolonner, captions, mellemrum og
  billedformat justeres i LightWidgets widget-creator. Sættes den i `instagram_widget`,
  får den automatisk fuld bredde under teksten (`.ig__inner--widget`), hvilket ser langt
  bedre ud end den smalle højrekolonne.
- **Testet over både HTTP og HTTPS** (selvsigneret certifikat lokalt): demowidgetten vises
  i begge. Det beviser mekanismen — men **ikke** gratisniveauet, fordi demo-widgets på
  lightwidget.com er opgraderede.
- **Gratisniveauet kan ikke testes uden at forbinde en Instagram-konto.** LightWidgets
  egen side siger eksplicit *"Works on HTTPS websites: No"* for Free, mens Upgraded
  tilføjer HTTPS, 30-minutters opdatering, CDN, redigerbare indstillinger og mails ved
  udløbet token. GitHub Pages er altid HTTPS → gratisniveauet er ikke brugbart i
  produktion.
- **14 dages gratis prøve** på upgrade (uden kort) gør det muligt at teste den rigtige
  opsætning med Johanns konto, før de 15 $ betales.
- SnapWidgets gratisplan oplyser 15-minutters opdatering og nævner ingen
  HTTPS-begrænsning; det er det gratis alternativ, der bør testes på samme måde.

## Sådan sætter du en widget ind

1. Opret widgetten hos udbyderen, og forbind Johanns Instagram-konto (han skal logge ind
   og godkende adgangen — det kan ikke gøres uden ham).
2. Kopiér widget-koden.
3. Sæt den ind i `hugo.toml`:

```toml
[params]
  instagram_widget = '<script src="…"></script><div class="…">…</div>'
```

4. Genopbyg. Er `instagram_widget` tom, vises det kuraterede galleri i stedet.

Widget-koden indsættes uændret, så udbyderens opdateringer af koden kan kopieres ind på
samme måde senere.
