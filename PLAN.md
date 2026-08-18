# Dream World — Website Plan & Framework

## Context

Dream World Mattress (Dehradun, Uttarakhand) is a young sleep-products brand (IG @dream_world_mattress, ~360 followers, joined Nov 2024) expanding from **mattresses → pillows → broader furniture**. Their old Shopify store (dreamworldmattress.com) is **dead/unavailable** — clean slate, they own the domain.

Goal: a **premium, trustworthy, non-"AI-shop"** catalog website. Visitors browse products → contact via **WhatsApp** to negotiate/close (no online checkout). Two audiences: **retail buyers** + **distributors** (they run a dealer program).

**Hard requirement — HANDOFF:** the brand adds new products/designs *weekly*. The owner/marketing team must add products, photos, prices, categories **themselves** without coming back to the builder, while the **design, structure, and premium feel stay locked**. This is the single most important architectural constraint. No build happens until catalog + this plan are approved.

---

## Competitor research synthesis (Indian sleep/furniture leaders)

Analyzed: **Wakefit**, **The Sleep Company**, **Duroflex**, **SleepyCat**, WoodenStreet (furniture IA).

**Recurring premium patterns (what to adopt):**
- **Trust bar** repeated across page: customer count, warranty, free delivery/installation, rating. (Wakefit "25 Lakhs+", SleepyCat "6L+ / 10yr / 100 nights").
- **Category-first architecture** built to grow: Sleep / Sit / Relax (Sleep Company), or Mattress→Furniture→Rooms (Wakefit). Never hardcoded to one product.
- **Founder / brand story** for authenticity (Sleep Company, SleepyCat) — critical for a *young* brand with low social proof.
- **Real branded photography + short benefit callouts**, not stock or long paragraphs. Specific claims ("Sleep 4–6° cooler", "8/10 back-pain relief").
- **Named product lines / feel tags** ("Duropedic", "SmartGRID", "Best Seller / New" badges) = signals of range and expertise.
- **Omnichannel CTAs**: WhatsApp + Call + Store locator, WhatsApp-first (matches Dream World exactly).
- **B2B / bulk path** ("Wakefit for Business", Duroflex institutional) = our **Distributorship** page.
- Generous whitespace, minimal chrome, one accent color, editorial type.

**What makes them look generic/AI (to avoid):** aggressive countdown timers everywhere, purple/blue gradients, stock "happy family" photos, cluttered mega-menus, inflated fake stats, wall-of-text.

**Positioning gap for Dream World:** leaders are big/impersonal. Dream World wins on **local Dehradun trust + personal WhatsApp service + honest, uncluttered premium look** — a boutique feel the giants can't match.

---

## Proposed design system (research-backed, to refine on approval)

**Register:** brand/editorial (design *is* the product). Soothing, premium, trustworthy — not clinical, not loud.

**Color strategy — "Committed warm-neutral" (one hero color carries the brand):**
- Base: warm ivory / off-white `#F6F1E9` (never pure white)
- Ink: deep midnight indigo `#1C2438` (restful "night/sleep" hue, not tech-blue)
- Accent (≤10%): muted brass / ochre `#B08D57` — premium, warm, "quality craft"
- Secondary calm: soft sage `#8CA098` for support surfaces
- All neutrals tinted toward the warm base. No pure #000/#fff. No gradients.

**Type (distinctive pairing, not Inter/Arial):** Display serif with character (e.g. **Fraunces** / **Hanken Grotesk** headings) + clean grotesque body (e.g. **General Sans / Satoshi**). Load only needed weights, `display=swap`.

**Shape/space:** one radius, subtle warm shadows, one spacing scale with varied section rhythm. Restrained motion (fade/rise on scroll, no gimmicks).

*(Alt directions if rejected: "Clean & modern" soft-white/charcoal/sage; "Bold luxe" near-black/deep-green/gold. Recommendation = warm-neutral above.)*

---

## Information architecture (sitemap)

Built category-driven so new products/categories drop in without redesign.

- **Home** — hero + trust bar + category grid + featured/new products + why-us + reviews snippet + store/WhatsApp CTA + distributor teaser
- **Category pages** (data-driven, auto-generated): `/mattresses`, `/pillows`, `/furniture`, + any future category the CMS creates
- **Product detail** (single JS template `?id=` or generated per product): gallery, short benefit pointers (not paragraphs), sizes/variants, price + "Enquire on WhatsApp for best price" (deep-link prefilled with product name), warranty/care, related products
- **Reviews** — dedicated page, tied to **Google Business Profile** reviews so new visitors see real experiences
- **About / Our Story** — founder + brand trust, Dehradun roots
- **Distributorship / Dealer** — B2B enquiry path, own WhatsApp/form
- **Contact / Visit Us** — address (Chandrabani, Pitthuwala, Dehradun), map, WhatsApp, phone, hours
- Persistent **floating WhatsApp CTA** on every page + click-to-call

**Pricing display (confirmed):** show price/MRP on every product + "Enquire on WhatsApp for best price" CTA.

---

## Handoff architecture (THE key decision)

Custom premium front-end + a **content layer the marketing team edits themselves**. Design/structure are locked in code; only *content* is editable. Recommended stack:

**Recommendation: Vanilla static site + Sveltia CMS (git-based admin) on Netlify.**
- Custom-designed static site (HTML/CSS/JS, DRY shell). Products live as data/markdown files, not hardcoded.
- **Sveltia CMS** = free, open-source admin UI at `/admin`. Marketing logs in (GitHub/Netlify Identity), fills a **form** (product name, category, price, sizes, photos via upload, benefit pointers, badges New/Bestseller) → commits to git → Netlify auto-rebuilds. **No code, no calls back to us.** Design cannot break — they only fill fields.
- Add a new category? One dropdown field. New product weekly? 2-minute form. Locked layout renders it premium automatically.
- Cost: **₹0** (Netlify free tier + open-source CMS). Successor to Netlify/Decap CMS.

**Alternatives (in plan for the decision):**
- **Google Sheet as CMS** — team edits a Sheet, site pulls JSON. Simplest for very non-technical users, but image handling is clumsy. Good fallback.
- **Builder-only I maintain** — cheapest to build, fails the handoff requirement. Rejected.
- **Shopify/Webflow** — recurring cost + harder to keep the bespoke non-AI look; old Shopify already died. Not recommended.

**Reviews handoff:** dedicated Reviews page pulling **Google Business Profile** reviews via a free widget (EmbedSocial/Jotform free tier ≈10 reviews) or self-hosted via Google Places API. Note free tiers cap review count — may need a small paid tier or Places API for "all reviews, auto-updating."

---

## Features checklist

- Mobile-first, fast on mid-range Android (WebP, lazy-load, no heavy JS)
- Sticky header + floating WhatsApp; every CTA deep-links WhatsApp prefilled with product context
- Category filter/sort within category pages; search optional phase 2
- Trust bar (warranty, years, Dehradun store, rating) near CTAs
- Google reviews on dedicated page + snippet on home
- Distributor enquiry path (separate WhatsApp/form)
- Store locator / map + click-to-call
- **SEO:** unique title/meta per page, clean URLs, sitemap.xml, robots.txt, OG images, semantic HTML, alt text (CMS-enforced field)
- **Schema (AEO/GEO):** `LocalBusiness` (Dehradun NAP), `Product` + `Offer` + `AggregateRating`, `BreadcrumbList`, `FAQPage`, `Organization`. Makes products eligible for rich results + AI Overviews/ChatGPT citations
- **GEO:** clear factual product specs, FAQ blocks, llms.txt, crawlable content (no JS-only rendering of key info)
- Accessibility: ≥44px tap targets, contrast, focus states

---

## Build phasing (after approval + catalog)

0. Business intake finalize (catalog dump → structured product data)
1. PLAN approval (this doc) + design token lock
2. Assets: localize/optimize photos to WebP; recreate logo as clean SVG if needed
3. DRY scaffold (shell, header/footer/floating CTA injected once; data schema)
4. Home first → shared components → category template → product template → About/Reviews/Distributor/Contact
5. Wire CMS (Sveltia) + seed catalog + write 1-page "how to add a product" guide for marketing team
6. SEO/schema pass + lean verification (mobile 375px, no horiz scroll, WhatsApp links, console clean)
7. Deploy to Netlify, point dreamworldmattress.com, HANDOFF.md + admin walkthrough

---

## Verification (at build time, lean)

- Local preview: small JSON check `{horizontalScroll, navToggle, cardCount, consoleErrors}`; mobile 375px pass
- WhatsApp deep-links open with correct prefilled product text
- CMS: add a test product via `/admin` → confirm it renders on site with locked design
- Schema validated (Rich Results test); Lighthouse mobile perf/SEO
- Reviews widget loads real Google profile reviews

## Open questions (see AskUserQuestion)
1. Handoff mechanism: Sveltia admin UI (recommended) vs Google Sheet vs other
2. Reviews: live Google widget (may need small paid tier for all reviews) vs curated
3. Hosting/domain: Netlify + point existing dreamworldmattress.com — confirm
4. Logo/photo assets: real high-res available, or placeholders for now
