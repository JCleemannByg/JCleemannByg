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
5. Giv Johann adgang: enten som **collaborator** på repoet, eller via Pages CMS'
   collaborator-funktion. Han skal have en gratis GitHub-konto.

> Der kræves **ingen** "Read and write permissions" i Actions-indstillingerne: deploy
> henter Instagram-snapshot og optimerer billeder i build-runneren i stedet for at committe.

## Hvad kan redigeres

| Område | Hvor |
|---|---|
| Forside: hero, fakta, om-blok, brødtekst | `content/da/_index.md` |
| Projekter: opret/slet, titel, kategori, år, rækkefølge, cover + galleri, før/efter-billeder, tekst | `content/da/projekter/*.md` |
| Projekter (oversigtstekst) | `content/da/projekter/_index.md` |
| Ydelser: intro + liste af ydelser | `content/da/ydelser/index.md` |
| Om-siden | `content/da/om/index.md` |
| Kontakt-siden | `content/da/kontakt/index.md` |
| Alle billeder (upload, udskift) | `assets/images/**` via mediebiblioteket |
| SEO-titel og meta-beskrivelse pr. side | frontmatter (`titel`, `beskrivelse`) |
| Telefon, e-mail, CVR, adresse, Instagram, delebillede | `data/site.yaml` |
| Farver, typografi, mål og skygge (design-tokens) | `data/design.yaml` |
| Knap- og aria-tekster | `i18n/da.toml` |

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

## Sprog

Siden er **kun på dansk** lige nu: ét indholdstræ (`content/da/`), én i18n-fil
(`i18n/da.toml`), én gruppe i Pages CMS (“Indhold”) og ingen sprogskifter i designet.

Det betyder også, at `verify.py` selv registrerer, at der kun er ét sprog, og derfor
**ikke** kræver oversættelser. I CMS'et er der ingen tomme engelske felter eller
dublerede sider at vedligeholde.

### Hvis engelsk skal tilbage senere

Alt er forberedt til det — indholdet ligger i git-historikken, og værktøjerne tjekker
automatisk, når sproget dukker op:

1. Genopret `content/en/` (samme filnavne/slugs som `content/da/`) og `i18n/en.toml`
   (samme nøgler).
2. Tilføj `[languages.en]` i `hugo.toml` med `contentDir = 'content/en'` og engelske
   menupunkter.
3. Genskab `layouts/partials/lang-switch.html` og `hreflang.html` (de ligger i
   git-historikken) og indsæt dem i header og head.
4. Tilføj gruppen “Engelsk indhold” og `tekster_en` i `.pages.yml`.
5. Kør `pixi run check` — `verify.py` tjekker nu automatisk, at hver dansk side har en
   engelsk tvilling, og at begge i18n-filer har samme nøgler.

## Hvad kan **ikke** redigeres (med vilje)

- **Layout og skabeloner** (`layouts/`) — struktur, sektionsrækkefølge, HTML.
- **CSS-strukturen** (`assets/css/main.css`) — kun tokens er redigerbare.
- **Menupunkterne** — de ligger i `hugo.toml`.
- **Instagram-listerne** (`data/instagram_posts.json`, `data/instagram.yaml`) — de hentes
  automatisk ved deploy og redigeres derfor ikke i CMS'et.
- **Workflows, scripts og konfiguration** — udvikleransvar.

## Branches (main og develop)

Pages CMS har en branch-vælger, fordi den læser repoets branches. Opsætningen er:

| Branch | Rolle | Hvad sker der ved push |
|---|---|---|
| `main` | Produktion | `deploy.yml` bygger og publicerer på `/` |
| `develop` | Udkast/eksperimenter | `deploy.yml` bygger preview på `/preview/` (noindex); `check.yml` verificerer ekstra |

Sådan bruges det: vælg `develop` i Pages CMS, rediger frit, og se resultatet på
**<https://jcleemannbyg.github.io/JCleemannByg/preview/>** (eller lokalt med
`git checkout develop && pixi run dev`). Når du er tilfreds, flettes `develop` ind i `main`
(gerne via pull request), og ændringerne går live.

Preview-siden bygges fra `develop` ind i samme deployment som produktionen, får
`noindex` og en synlig preview-bar. GitHub Pages kræver at begge branches er tilladt under
**Settings → Environments → github-pages → Deployment branches and tags**.

## Knapper i Pages CMS (actions)

`actions` i `.pages.yml` tilføjer knapper, der dispatcher GitHub-workflows med et
`payload`-input. I dette projekt:

- **"Genbyg og publicér"** → `cms-action.yml` → `deploy.yml` på `main`.
  Knappen er nyttig, når man vil tvinge et genbyg (fx efter manuelt at have ændret noget
  uden for CMS'et).

Workflowet, der trigges, skal have `workflow_dispatch` med et `payload`-input; det er derfor
`cms-action.yml` findes som en lille mellemstation i stedet for at pege direkte på
`deploy.yml`.

## Forbehold

- **Ingen live-forhåndsvisning** i den gratis hosted version: gem → commit → genbyg.
- **Ingen granulære rettigheder endnu**: alle med adgang til repoet kan redigere alt.
- **Billeder lægges i repoet**, men behøver ikke at være optimeret på forhånd: deploy
  nedskalerer automatisk alt over 2000 px og rekomprimerer **i build-runneren**. Det gør
  den publicerede side let, men ændrer ikke originalen i repoet. Lokalt: `pixi run images`.
- **TOML-filerne med knaptekster** bliver skrevet af CMS'et ved gem; kommentarer i dem
  kan forsvinde.
- **Pages CMS er et lille projekt** (MIT). Skulle det forsvinde, er alt indhold stadig
  almindelige filer, og `.pages.yml` kan slettes uden konsekvenser for siden.

## Rollback

Hver gemning er en almindelig git-commit. En dårlig ændring rulles tilbage med
`git revert <commit>` — eller ved at rette den i CMS'et igen.
