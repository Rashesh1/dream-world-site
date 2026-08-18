# Findings & Blockers — read before building

## 🔴 Blocker 1: The product photos are NOT usable as-is (19 of 34)
The images are **sourced reference pictures**, not Dream World's own product shots. Problems found:
- **App/e-commerce screenshots** — phone status bars, "CANCEL", "Amazon detected this screenshot", thumbnail strips visible (e.g. sofas 060, 062; loungers 084, 086, 088).
- **Competitor watermarks** — "KHATICRAFT" (table 098), "PIZAP" (sofa 066), "MADE IN INDIA" (sofa 078), "LUXURY HOME" (bed 056).
- **Mismatched composites** — podcast-room renders with random chairs (sofas 066/068/070).
- **Inconsistent look** — mix of AI room renders, white-bg cutouts, and photos. No single visual language.

**Why it matters:** a premium, trustworthy site cannot show competitor-watermarked screenshots. It reads cheap and risks copyright issues. **15 of 34 are "OK-ish"; 19 need replacing.**

**Options (owner decides):**
- **A. Real photos** — owner shoots actual products on a plain backdrop (phone is fine with good light). Best for trust.
- **B. AI-regenerated clean images** — recreate each product as a consistent, watermark-free studio image. Fast, uniform, but not the literal item.
- **C. Launch with what's clean now** (~15 items) + add the rest as photos arrive via the CMS.

## 🔴 Blocker 2: No product names / sizes / colours
Dump has photo + price only. Site needs at least a name + size + colour per item. Owner must fill these (or approve our drafts). Placeholder names are in `catalog.csv` now.

## 🟡 Note 3: Logo says "SOFA"
Logo (image 033) = "DREAM WORLD **SOFA**" gold-on-black oval. Owner wants "SOFA" removed. We recreate it as a clean **DREAM WORLD** SVG (keeps the gold/black premium feel).

## 🟡 Note 4: Brand vs reality
Public name/socials say "mattress"; actual sellable catalog is furniture. Recommend positioning: **"Dream World — Beds, Sofas & Furniture, Dehradun"**, keep mattresses/pillows as a category to add later (they do sell neck pillows per Instagram/Linktree).

## Contacts captured
- **Owner:** Ramesh Chaturvedi — **+91 81263 34038** (number to show on site — confirm)
- **Catalog sender:** +91 90455 79391 (~Goku)
- **Store:** Near Wildlife Institute Rd, Chandrabani, Pitthuwala, Dehradun
- Socials: Instagram @dream_world_mattress, Facebook, Pinterest, WhatsApp
- Dead domain: dreamworldmattress.com (Shopify, expired)

## Open decisions still pending (from earlier)
Handoff CMS tool · Reviews (Google) approach · Hosting/domain · **Image strategy (Blocker 1)** — the image call is now the most important one.
