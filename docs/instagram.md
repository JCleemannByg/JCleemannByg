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

## De fire muligheder, hvis "live" er et krav

| | Automatisk opdatering | Pris | Vedligehold | Vurdering |
|---|---|---|---|---|
| **A. Kurateret galleri (nu)** | Nej, du vælger billeder | 0 | Kopiér et billede når noget er værd at vise | **Anbefalet.** Hurtigst, ingen cookies, matcher designet, holder for evigt. |
| **B. Officiel embed pr. opslag** (`embed.js`) | Ja, pr. opslag | 0 | Indsæt embed-kode ved hvert nyt opslag; kan kræve klik-for-at-indlæse af hensyn til samtykke | God til 1–3 udvalgte opslag. Kræver klik-for-at-indlæse (GDPR) og kan give tomme felter, hvis et opslag slettes. |
| **C. Instagram Graph API** | Ja, automatisk feed | 0 (API) | Business/Creator-konto + Meta app-review + token, der skal fornyes senest hver 60. dag + planlagt genopbygning | **Frarådes** til denne type site. Bliver en vedligeholdelsesfælde. |
| **D. Tredjeparts-widget** (LightWidget, SnapWidget, Elfsight) | Ja | Gratis tier med branding, ellers ca. 15–120 $/år | Endnu en konto og leverandør at holde øje med; tredjeparts-cookies | Kun hvis et automatisk grid er et hårdt krav. |

## Anbefaling

Behold **A**, og tilføj eventuelt **B** til et enkelt eller to opslag, hvis der skal vises
"live"-indhold. C og D løser et problem, siden ikke har: Johann poster allerede på
Instagram, og de bedste billeder bliver kopieret ind i porteføljen — der er ingen grund til
at bygge en skrøbelig integration for at vise de samme billeder igen.

## Hvis B skal aktiveres

Det kræver konkrete opslags-URL'er (format `https://www.instagram.com/p/…/`) fra Johanns
konto. Så bygges en lille komponent, der først indlæser Metas `embed.js`, når besøgende selv
klikker "Vis opslag" — så er der ingen tredjeparts-cookies før samtykke.
