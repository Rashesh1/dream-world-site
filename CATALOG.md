# Dream World — Catalog (from WhatsApp dump, 31 Jul–01 Aug 2026)

Source: WhatsApp chat with ~Goku (+91 90455 79391). Owner: **Ramesh Chaturvedi, +91 81263 34038**.
Parsed 51 images → **34 priced products** + logo + a few duplicates/extras.
Structured data: [`03_catalog_data/catalog.csv`](03_catalog_data/catalog.csv) · [`catalog.json`](03_catalog_data/catalog.json)
Renamed images: [`02_assets_optimized/`](02_assets_optimized/) (by category). Originals kept in `01_catalog_raw/`.

## Headline: this is a FURNITURE catalog, not mattresses
Brand name is "Dream World Mattress" but **every priced item is furniture** — beds, sofas, loungers, tables. **Zero mattresses, zero pillows** in the dump. Matches the plan to launch as **"Dream World"** (drop "Mattress"). Logo they sent literally says "DREAM WORLD **SOFA**" and they asked to remove "SOFA".

## Categories & price bands

| Category | Count | Price band (₹) | Notes |
|---|---|---|---|
| **Beds** (upholstered / storage) | 11 | 17,000 – 26,000 | Wingback, channel, quilted; some with storage drawers + LED |
| **Sofas** (sets / sectionals) | 10 | 16,000 – 35,000 | L-shape, modular, office sets; one has "40-density foam, 5yr warranty" |
| **Loungers / Chaise / Diwan** | 7 | 16,000 – 20,000 | Single-seat lounges, Chesterfield + modern |
| **Coffee / Center Tables** | 6 | 5,000 – 18,000 | Sheesham + carved wood + live-edge |
| **TOTAL** | **34** | 5,000 – 35,000 | |

## Only spec/warranty details the owner gave
- **Bed 038 (₹22,000):** Top 15mm ply, sides 12mm, down 9mm, plyboard work.
- **Sofa 060 (₹35,000):** 40-density foam, leatherette, thick wood work, **5-year warranty**.
- **Sofa 066 (₹16,000):** "only sofa" (poufs/table extra).
- Everything else = photo + a bare price. **No names, no sizes, no colour options, no materials, no warranty.**

## Missing per product (owner must supply for a good site)
1. **Product name** (all are placeholder "Bed Design 01" etc. right now)
2. **Sizes** (Queen/King, dimensions) + which sizes available
3. **Colour / fabric options** per model
4. **Material** (leatherette / fabric / velvet; wood type)
5. **Warranty** per category
6. **Sofa-cum-bed (image 013): no price given** — flagged, ask owner.

See [`FINDINGS.md`](FINDINGS.md) for the image-quality blocker.
