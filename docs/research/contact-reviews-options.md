# Google Business Profile, anmeldelser og kontaktformular — muligheder

Researched 2026-11-09 for J Cleemann Byg (Hugo on GitHub Pages, no backend, one-man carpenter/snedker in Nærum); facts checked against official docs, research only — no site files changed.

## TL;DR

1. **Create/verify a Google Business Profile** (free) as a **service-area business** if customers don't
   visit Nærum Hovedgade 15 — hides the home address and is what Google tells service trades to do.
   Verification is usually **video recording from the mobile app** (30 s+, live, unedited); phone/SMS,
   email, live video call or postcard may also be offered.
2. **Reviews:** get the review link/QR from *Read reviews → Get more reviews*, ask after every job, reply
   to everything, never incentivise. On the site show **2–3 quotes collected with written permission**
   + a "Se anmeldelser på Google" link. **Do not** add review/star JSON-LD for his own business.
3. **Contact form:** **Forminit free** (UK company, EU-AWS data, 100 submissions/month, file uploads,
   spam filters, DPA) as the primary choice; **Web3Forms** as the 10-minute fallback. Keep the existing
   `tel:`/`mailto:` links — the form is only for people who won't call. Danish review-request copy and
   the 4 FAQ answers are in §4 (the site already ships those FAQ items in `content/da/kontakt/index.md`).

## 1. Google Business Profile (Denmark)

**Create or claim** (free, one Google account; use the business email, not a personal Gmail): new profile
via [business.google.com/add](https://support.google.com/business/answer/2911778), or, if an unverified
profile exists, Google Maps → search the name → *Claim this business → Manage now*. A verified profile
owned by someone else can only be requested via [ownership request](https://support.google.com/business/answer/4566671).

**Storefront vs service-area business (SAB).** Google's rule: "If you don't serve customers at your business
location, do not add your business address to your Business Profile"
([SAB guidance](https://support.google.com/business/answer/9157481)). For a carpentry business run from a
Nærum address, SAB is the right and privacy-friendly classification — address hidden, service area (Nærum,
Rudersdal, northern Copenhagen) shown instead.

**Verification options today** — Google assigns the available methods automatically and they can't be
chosen ([verification doc](https://support.google.com/business/answer/7107242)); one profile may need more
than one method, and review takes **up to 5 business days** afterwards.

| Method | What it involves | Practical note |
|---|---|---|
| **Video recording** (recommended) | Record live in the mobile app, unedited, ≥30 s, one take; cannot upload a pre-recorded file | Best fit for a trade: for an SAB show neighbourhood street signs/landmarks, van/tools/workspace, branded workwear, plus an invoice/permit/utility bill matching the profile name; no faces, no bank/ID/tax numbers. Video can be deleted afterwards ([doc](https://support.google.com/business/answer/14271705)) |
| **Live video call** | Video call with a Google rep during business hours; show location, tools, proof of management | May not be offered for all businesses |
| **Phone / SMS** | Code by call or text to the business number (no IVR) | Fast when offered |
| **Email** | Code to the business email address | Fast when offered |
| **Postcard** | 5-digit code by mail; most arrive within 14 days, code expires after 30 days | Slowest; don't edit name/address/category while waiting |
| **Instant** | Possible when the website is verified in Search Console | Worth doing *before* starting: verify the domain in Search Console |

**Profile fields worth filling** (Danish, matching the site): exact name `J Cleemann Byg` (no keywords),
primary category **Tømrer** (+ secondary e.g. Snedker), service area, phone 42 58 11 01, website, hours only
if actually kept, services list (køkkenmontage, indbygning, renovering, udvendigt træarbejde), Danish
description, and photos of van/workshop/tools/projects, refreshed regularly. Monitor and answer Q&A.

**Review link / QR / replying.** *Read reviews → Get more reviews* gives a short review link plus a
downloadable QR code; **QR generation only works in a desktop browser** (right-click → *Save image as*)
([doc](https://support.google.com/business/answer/16816815)). Put it on receipts, invoice PDFs, SMS/email
signatures and a small printed card. Reply to every review under *Read reviews* — replies are public, Google
moderates them (usually ≤10 min, worst case 30 days), the owner's personal name is never shown, and replies
can be edited or deleted ([manage reviews](https://support.google.com/business/answer/3474050)). A single
review can be shared as a direct link from Maps (*Share review*). Nothing may be offered in exchange for
reviews — that is **fake engagement** and prohibited
([policy](https://support.google.com/contributionpolicy/answer/7400114), [tips](https://support.google.com/business/answer/3474122)).
Google notes reviews are only available in certain countries/categories and may change; in Denmark they are
live for trades today, so no blocker.

## 2. Showing Google reviews on a static site

| Option | How it works | Cost/limits | Trade-offs | Verdict |
|---|---|---|---|---|
| **Places API (official)** | Client JS calls Place Details, gets **up to 5 reviews** | Google Cloud billing account; free monthly call allowance per product, review fields are a paid Place Details SKU | Policy: **no caching/storing**, Google logo/attribution, author avatar+name+profile link, link back to the source review on Maps, ordering notice ([policies](https://developers.google.com/maps/documentation/places/web-service/policies)); one request per page view; API key exposure on a static site | Not worth it for 5 reviews |
| **Business Profile API** | `accounts.locations.reviews` | Requires access request/approval + OAuth | Management API for own profile, not a website display product; storing reviews conflicts with Maps content terms ([API ref](https://developers.google.com/my-business/reference/rest/v4/accounts.locations.reviews/get)) | No |
| **Third-party widget** (Elfsight, EmbedSocial, Taggbox, SociableKIT…) | Vendor hosts a JS embed that pulls the reviews | Elfsight free = 200 views/month, 1 widget; Basic $6/mo for 5,000 views ([pricing](https://help.elfsight.com/article/938-pricing)) | Relies on unofficial access/scraping (breaks when Google changes), third-party JS + cookies (Danish cookie-consent + privacy-policy burden), low free view cap, Google-ToS grey zone | Only if he insists on live reviews |
| **Manual testimonials with permission** | Ask the customer; quote 2–3 sentences with first name + job/area; link to the Google profile | Free | Needs a consent trail (keep the email/SMS); no stars | **Recommended** |

**JSON-LD rules.** Review snippets are **ineligible for star results when the reviewed business controls the
reviews about itself** — explicitly including a Google Business reviews widget embedded on its own site;
ratings must come directly from users and must not be compiled by editors
([review snippet guidelines](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)).
Fake or undisclosed incentivised reviews, or marking up review text that isn't visible, can trigger a
**structured-data manual action** ([general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)).
So: keep `LocalBusiness` schema (name, address, phone, area, services, hours) — **without**
`review`/`aggregateRating` — and render quotes as plain HTML. Don't re-publish Google review text verbatim
without permission: Maps content may not be copied out, the text belongs to the author, the name is personal
data.

**Simplest compliant path:** after each job ask "må jeg bruge et par ord fra dig på hjemmesiden?", keep the
yes, show 2–3 short quotes with first name and job type, and put a button "Se alle anmeldelser på Google"
next to them. If he ever wants live reviews, Elfsight Basic (~$6/month) is the cheapest widget route — but
accept the consent banner, privacy-policy entry and silent breakage.

## 3. Contact forms for GitHub Pages

GitHub Pages serves static files only; every option below is a third party (or his own Worker). The site
currently uses `tel:` and `mailto:` only ([layouts/kontakt/single.html](../../layouts/kontakt/single.html)) —
keep those as primary CTAs; the form is only for people who won't call.

| Option | Free tier | File uploads | Spam protection | GDPR / data location | Setup for a non-technical owner |
|---|---|---|---|---|---|
| **Forminit** (formerly Getform) | 100 submissions/month, 1 form ([pricing](https://forminit.com/pricing/)) | Yes, 100 MB storage, 25 MB/submission | Built-in filters (CleanTalk) + optional Turnstile/reCAPTCHA/hCaptcha + honeypot ([docs](https://forminit.com/docs/)) | UK company (UXPLUS LTD), **EU AWS data centres**, DPA agreed via ToS ([GDPR page](https://forminit.com/gdpr/)) | Low: create form, paste form ID into the HTML/Hugo form, done |
| **Web3Forms** | 250 submissions/month ([site](https://web3forms.com/)) | Paid plans only | Honeypot + free captcha | Company operates from **India**; AWS/Cloudflare/Hetzner; SCCs, DPA, retention up to 3 years ([privacy](https://web3forms.com/privacy), [DPA](https://web3forms.com/dpa)) | Lowest: hidden `access_key` field, no dashboard needed |
| **Formspree** | 50 submissions/month, unlimited forms, 30-day archive ([limits](https://help.formspree.io/articles/account-management/account-limits/), [plans](https://formspree.io/plans)) | Paid only (1 GB on Personal) | Formshield ML + reCAPTCHA + domain restriction | US company; DPA available; data in US | Low: form action URL + email verification |
| **Basin** | 50 submissions/month, 1 form, 100 MB files, 30-day retention ([plans](https://docs.usebasin.com/plan-comparison/)) | Yes | Filtering + captcha + domain restriction | US company; AWS US / DigitalOcean Canada / Hetzner EU; DPA + EU representative ([GDPR](https://usebasin.com/gdpr)) | Low: HTML form endpoint |
| **Netlify Forms** | Form submissions included on current credit-based plans; legacy free tier = 100/month + 10 MB uploads ([billing](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-legacy-plans/billing-faq-for-legacy-plans/)) | Yes | Honeypot + reCAPTCHA ([setup](https://docs.netlify.com/manage/forms/setup/)) | Netlify Inc., US | **High: requires hosting on Netlify** — moving off GitHub Pages for one form is not worth it |
| **Cloudflare Worker + Resend** | Worker: 100,000 requests/day free ([limits](https://developers.cloudflare.com/workers/platform/limits/)); Resend: 3,000 emails/month, 100/day ([pricing](https://resend.com/pricing)) | Needs R2/KV work | Turnstile only, must be wired by hand | Cloudflare global network; own DPAs | **High: code, secrets, DNS records, ongoing maintenance** — only if a developer maintains it |

**GDPR basics for any choice:** the owner is data controller, the provider is a processor → accept the DPA,
name the provider in the privacy policy, collect only name/phone-or-email/message, and delete old submissions
(Forminit free keeps them until deleted; set a retention or clean up yearly). A form is not a legal problem;
an undisclosed third-party processor is.

**Recommendation: Forminit free.** It is the only listed provider that combines a free tier large enough for
a one-man business, **EU data hosting with a UK company and a DPA**, file uploads (customers often want to
send a photo of the job), and spam protection, at the lowest owner effort — one form, form ID pasted in,
email notifications on. Fallbacks: **Web3Forms** if he wants zero dashboard and 250 submissions/month more
than EU-only processing; **Formspree** if a familiar brand matters more than file uploads. **Avoid** Netlify
Forms (hosting migration) and a hand-rolled Worker (maintenance). Keep `tel:`/`mailto:` as the primary CTAs
and add one line under the form: "Oplysninger bruges kun til at besvare din henvendelse."

## 4. Danish copy

**Review request — email** (send 1–3 days after the job; link from *Get more reviews*):

> **Emne:** Tak for opgaven – vil du dele din oplevelse?
>
> Hej [navn],
> Tak fordi jeg måtte hjælpe med [opgaven] i [område]. Jeg er glad for, at vi fandt en løsning, du er
> tilfreds med. Hvis du har lyst, må du meget gerne skrive et par ord om samarbejdet på min Google-profil.
> Det tager et minut, og det hjælper andre med at finde en tømrer, de kan stole på: [link]
> Du er ikke forpligtet – og du kan altid ændre eller slette din anmeldelse igen.
> Mange hilsner · Johann Cleemann · J Cleemann Byg · 42 58 11 01

**Review request — SMS** (keep ≤160 characters, or split in two messages):

> Hej [navn]. Tak for opgaven. Har du lyst, må du gerne skrive et par ord om mig på Google – det
> hjælper andre med at finde en tømrer: [link]. Mvh Johann, J Cleemann Byg

Rules: only to customers he actually worked for; ask in person first where possible; **never** offer a
discount, gift or free work (Google prohibition, see §1); one friendly reminder at most; no bulk sends
(electronic marketing to consumers needs consent under markedsføringsloven §10).

**FAQ — 4 conservative answers, no invented numbers.** The site already renders these four questions from
`faq:` in `content/da/kontakt/index.md`; wording below is the tightened version (same claims, no prices, no
lead times, no municipality list beyond what's stated):

1. **Hvad koster det?** — "Prisen afhænger af opgaven, materialerne og hvor meget der skal tilpasses.
   Du får et tilbud, inden arbejdet går i gang, så vi er enige om både pris og indhold."
2. **Hvor arbejder du?** — "Jeg arbejder i Nærum og det øvrige Rudersdal. Ligger opgaven uden for
   området, så skriv alligevel – så aftaler vi, om det giver mening."
3. **Hvor lang tid tager det?** — "Det afhænger af opgavens størrelse og de materialer, der skal
   skaffes. Vi laver en tidsplan sammen, inden arbejdet begynder, så du ved, hvad der sker hvornår."
4. **Hvordan kommer vi i gang?** — "Ring eller skriv med en kort beskrivelse og gerne et par billeder.
   Så aftaler vi et besøg, hvor vi ser på opgaven og taler om mål, materialer og næste skridt."

## Sources

- Google Business Profile Help: [add/claim](https://support.google.com/business/answer/2911778) · [verify](https://support.google.com/business/answer/7107242) · [video verification](https://support.google.com/business/answer/14271705) · [service-area businesses](https://support.google.com/business/answer/9157481) · [manage reviews](https://support.google.com/business/answer/3474050) · [review tips](https://support.google.com/business/answer/3474122) · [review link/QR](https://support.google.com/business/answer/16816815) · [ownership request](https://support.google.com/business/answer/4566671) · [contribution policy](https://support.google.com/contributionpolicy/answer/7400114)
- Google Search Central & Maps Platform: [review snippet guidelines](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) · [structured data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) · [Places API policies](https://developers.google.com/maps/documentation/places/web-service/policies) · [Business Profile reviews API](https://developers.google.com/my-business/reference/rest/v4/accounts.locations.reviews/get)
- Forms & widgets: [Forminit pricing](https://forminit.com/pricing/) · [Forminit GDPR](https://forminit.com/gdpr/) · [Forminit docs](https://forminit.com/docs/) · [Formspree limits](https://help.formspree.io/articles/account-management/account-limits/) · [Formspree plans](https://formspree.io/plans) · [Web3Forms](https://web3forms.com/) · [Web3Forms privacy](https://web3forms.com/privacy) · [Web3Forms DPA](https://web3forms.com/dpa) · [Basin plans](https://docs.usebasin.com/plan-comparison/) · [Basin GDPR](https://usebasin.com/gdpr) · [Netlify Forms setup](https://docs.netlify.com/manage/forms/setup/) · [Netlify legacy billing limits](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-legacy-plans/billing-faq-for-legacy-plans/) · [Cloudflare Workers limits](https://developers.cloudflare.com/workers/platform/limits/) · [Resend pricing](https://resend.com/pricing) · [Elfsight pricing](https://help.elfsight.com/article/938-pricing)
