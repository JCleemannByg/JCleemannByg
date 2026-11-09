# Pages CMS — redigering af siden

Siden er bygget så **alt indhold** kan redigeres uden at røre kode, og så en
ikke-teknisk ejer kan gøre det fra telefonen. Værktøjet er
[Pages CMS](https://pagescms.org) — gratis, open source (MIT) og uden database.

## Sådan hænger det sammen

1. Indholdet ligger som markdown + frontmatter i `content/` og som data i `data/`.
2. `.pages.yml` i repoets rod beskriver, hvilke felter der kan redigeres.
3. Pages CMS læser den fil og viser en formular.
4. Ved **Gem** committer Pages CMS ændringen til repoet.
5. GitHub Actions bygger siden og publicerer den (~1–2 minutter).

Der er ingen server, database eller separat indholdsbase: **markdown og git er
fortsat sandheden**. Sletter man `.pages.yml`, virker siden uændret — så redigerer man
bare filerne direkte.

## Engangsopsætning

1. Repoet skal ligge på GitHub (offentligt er fint og kræves for gratis Pages).
2. Gå til [app.pagescms.org](https://app.pagescms.org) og log ind med GitHub.
3. Installér GitHub-app'en på det pågældende repo (kun det repo).
4. Vælg repoet. Menuen kommer fra `.pages.yml`.
5. **Settings → Actions → General → Workflow permissions → "Read and write permissions"**
   (så Instagram-workflowet må committe sin opdaterede liste).
6. Giv Johann adgang: enten som **collaborator** på repoet, eller via Pages CMS'
   collaborator-funktion. Han skal have en gratis GitHub-konto.

## Hvad kan redigeres

| Område | Hvor |
|---|---|
| Forside: hero, fakta, om-blok, brødtekst | `content/da/_index.md` / `content/en/_index.md` |
| Projekter: opret/slet, titel, kategori, år, rækkefølge, cover + galleri, tekst | `content/*/projekter/*.md` |
| Projekter (oversigtstekst) | `content/*/projekter/_index.md` |
| Ydelser: intro + liste af ydelser | `content/*/ydelser/index.md` |
| Om-siden | `content/*/om/index.md` |
| Kontakt-siden | `content/*/kontakt/index.md` |
| Alle billeder (upload, udskift) | `assets/images/**` via mediebiblioteket |
| SEO-titel og meta-beskrivelse pr. side | frontmatter (`titel`, `beskrivelse`) |
| Telefon, e-mail, CVR, adresse, Instagram, delebillede | `data/site.yaml` |
| Farver, typografi, mål og skygge (design-tokens) | `data/design.yaml` |
| Knap- og aria-tekster (dansk/engelsk) | `i18n/da.toml`, `i18n/en.toml` |

### Design-tokens

`data/design.yaml` indeholder de værdier, der bliver til CSS-variabler i
`assets/css/tokens.css` ved hvert build:

- **Farver** — 9 hex-farver (valideres med regex `^#[0-9a-fA-F]{6}$` i CMS'et).
- **Typografi** — serif-stak til overskrifter, sans-stak til brødtekst.
- **Mål og effekter** — maks. indholdsbredde, luft til siderne, hjørneradius på
  knapper og skygge.

Det er bevidst *tokens*, ikke layout: man kan gøre siden varmere, koldere, strammere
eller blødere — men ikke flytte sektioner eller ændre strukturen. Det holder designet
sammenhængende.

## Hvad kan **ikke** redigeres (med vilje)

- **Layout og skabeloner** (`layouts/`) — struktur, sektionsrækkefølge, HTML.
- **CSS-strukturen** (`assets/css/main.css`) — kun tokens er redigerbare.
- **Menupunkterne** — de ligger i `hugo.toml`.
- **Instagram-listerne** (`data/instagram_posts.json`, `data/instagram.yaml`) — de
  opdateres automatisk af `.github/workflows/instagram.yml`.
- **Workflows, scripts og konfiguration** — udvikleransvar.

## Forbehold

- **Ingen live-forhåndsvisning** i den gratis hosted version: gem → commit → genbyg.
- **Ingen granulære rettigheder endnu**: alle med adgang til repoet kan redigere alt.
- **Billeder lægges i repoet** — hold dem under ca. 2000 px og JPEG ~q80, ellers vokser
  repo og deploy-tid.
- **TOML-filerne med knaptekster** bliver skrevet af CMS'et ved gem; kommentarer i dem
  kan forsvinde.
- **Pages CMS er et lille projekt** (MIT). Skulle det forsvinde, er alt indhold stadig
  almindelige filer, og `.pages.yml` kan slettes uden konsekvenser for siden.

## Rollback

Hver gemning er en almindelig git-commit. En dårlig ændring rulles tilbage med
`git revert <commit>` — eller ved at rette den i CMS'et igen.
