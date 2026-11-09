# Custom domain: jcleemannbyg.dk

Siden skal flyttes fra `https://jcleemannbyg.github.io/JCleemannByg/` til
`https://jcleemannbyg.dk/` (og `www.jcleemannbyg.dk`).

## Nuværende status (verificeret 2026-11-09)

| | |
|---|---|
| Domæne | `jcleemannbyg.dk`, registreret til 2027-09-02 |
| DNS | Hostinger-navneservere: `ns1.dns-parking.com`, `ns2.dns-parking.com` |
| A-record i dag | `72.60.81.210` (**skal ændres**) |
| `www` | peger i dag på samme A-record |
| E-mail | MX `mx1.titan.email` + `mx2.titan.email` og SPF (`v=spf1 include:spf.titan.email ~all`) — **må ikke slettes** |

DNS redigeres i **Hostinger hPanel → Domains → jcleemannbyg.dk → DNS Zone**
(navneserverne er Hostingers, så det er der, zonen ligger).

## 1. Skift DNS-records (Hostinger)

Behold alle MX-, SPF-, DKIM- og autodiscover-records. Ændr kun web-records:

| Type | Navn | Værdi | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 300–3600 |
| A | `@` | `185.199.109.153` | 300–3600 |
| A | `@` | `185.199.110.153` | 300–3600 |
| A | `@` | `185.199.111.153` | 300–3600 |
| AAAA (valgfrit) | `@` | `2606:50c0:8000::153`, `...:8001::153`, `...:8002::153`, `...:8003::153` | 300–3600 |
| CNAME | `www` | `jcleemannbyg.github.io` | 300–3600 |

**Slet** den gamle A-record `72.60.81.210` på `@` og den gamle `www`-record, når de nye er
lagt ind. Hvis TTL kan sættes lavt (fx 300) før skiftet, går ændringen hurtigere igennem, og
en tilbagerulning er nemmere.

Kontroller udefra:

```sh
dig +short jcleemannbyg.dk A       # forventer de fire 185.199.x.x-adresser
dig +short www.jcleemannbyg.dk CNAME
dig +short jcleemannbyg.dk MX      # skal stadig vise mx1/mx2.titan.email
```

DNS kan tage fra få minutter til et par timer (sjældent op til 24–48 t).

## 2. GitHub Pages

1. Repo → **Settings → Pages → Custom domain**: skriv `jcleemannbyg.dk` → **Save**.
2. Vent på *DNS check successful* (grøn).
3. Slå **Enforce HTTPS** til, når certifikatet er udstedt (kan tage minutter til et døgn;
   GitHub ordner Let's Encrypt automatisk). Tjek både `jcleemannbyg.dk` og
   `www.jcleemannbyg.dk` — GitHub redirecter normalt `www` til apex-domenet.

**Vigtigt:** Sæt først custom domain i GitHub, når DNS-records er lagt ind (eller samtidig).
Sættes det før, kan GitHub begynde at redirecte `github.io`-adressen til det nye domæne,
mens DNS stadig peger på den gamle host.

## 3. Fortæl buildet om domænet

Deploy-workflowet bruger automatisk `https://jcleemannbyg.github.io/JCleemannByg/`, med
mindre repository-variablen `SITE_URL` er sat. Når DNS er klar:

```sh
gh variable set SITE_URL --body "https://jcleemannbyg.dk" -R JCleemannByg/JCleemannByg
gh workflow run deploy.yml -R JCleemannByg/JCleemannByg
```

Workflowet bygger så med `baseURL = https://jcleemannbyg.dk/` og verificerer med base `/`,
så canonical, sitemap, Open Graph og alle links peger på domænet. Variablen kan sættes i
**Settings → Secrets and variables → Actions → Variables** i stedet for CLI'et.

## 4. Efter skiftet

- Tjek `https://jcleemannbyg.dk/`, en projektside og `/kontakt/`; tjek at `/sitemap.xml`
  og canonical peger på det nye domæne.
- Opdatér Google Business Profile (hvis den oprettes), Instagram-bio, e-mail-signatur og
  de eksisterende fortegnelser (Krak, Håndværkerregistret, Inno-aps m.fl.) med den nye URL.
- Tilføj domænet som property i Google Search Console og indsend sitemap.
- E-mailen er upåvirket: MX- og TXT-records er urørte.

## Tilbagerulning

Hvis noget går galt: genskab A `72.60.81.210` og fjern `SITE_URL`-variablen, så bygger
workflowet igen mod GitHub Pages-adressen.
