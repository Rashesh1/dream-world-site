#!/usr/bin/env python3
"""Canonical build script (runs on every Netlify deploy).
Reads content/products/*.md (CMS-editable) -> generates assets/js/data.js.
This REPLACES build_site_data.py as the source of truth going forward —
once the CMS is live, all product edits happen as .md files here, not in catalog.json."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "products"
BUILD = ROOT / "05_build"

CAT_LABELS = {"beds":"Beds","sofas":"Sofas","loungers":"Loungers","tables":"Center Tables",
              "sofa-cum-bed":"Sofa-cum-Bed","mattress":"Mattress","pillow-cushion":"Pillow & Cushion",
              "dining-table":"Dining Table","tv-cabinet":"TV Cabinet","interior":"Interior"}
CAT_TAGS = {"beds":"Upholstered & storage","sofas":"Sets & sectionals","loungers":"Chaise & diwan",
            "tables":"Solid wood","sofa-cum-bed":"Space-saving convertibles","mattress":"Memory foam & spring",
            "pillow-cushion":"Comfort essentials","dining-table":"Solid wood dining sets",
            "tv-cabinet":"Wall units & entertainment units","interior":"Custom carpentry & wall units"}
CATEGORY_ORDER = ["beds","sofas","sofa-cum-bed","loungers","tables","mattress","pillow-cushion","dining-table","tv-cabinet","interior"]
CATEGORY_THUMB = {
    "beds":"assets/img/products/bed-04.jpg", "sofas":"assets/img/products/sofa-03.jpg",
    "loungers":"assets/img/products/lounger-07.jpg", "tables":"assets/img/products/table-06.jpg",
    "sofa-cum-bed":"assets/img/categories/sofa-cum-bed.jpg", "mattress":"assets/img/categories/mattress.jpg",
    "pillow-cushion":"assets/img/products/pillow-02-comfort-cool.jpg",
    "dining-table":"assets/img/categories/dining-table.jpg", "tv-cabinet":"assets/img/categories/tv-cabinet.jpg",
}
CATEGORY_DESCRIPTIONS = {
    "beds": "Every bed is made to order — top 15mm ply, sides 12mm, down 9mm, plyboard work. Choose any size, material and finish to fit your budget.",
    "sofas": "Every sofa is made to order — 40-density foam, leatherette or fabric, thick wood work, 5-year warranty. Choose any size, material and finish to fit your budget.",
    "sofa-cum-bed": "Every sofa-cum-bed is made to order — 64x72 foam size, 78x72 total size, 18mm plywood, 40-density foam. Choose any size, material and finish to fit your budget.",
    "loungers": "Every lounger is made to order — solid wood frame, high-density foam, your choice of upholstery. Choose any size, material and finish to fit your budget.",
    "tables": "Every table is made to order in solid wood — sheesham, acacia or your preferred timber, any size and finish.",
    "mattress": "A range of memory foam, latex and spring mattresses, each with a genuine spec sheet. Enquire on WhatsApp for current pricing — size and firmness can be tailored to you.",
    "pillow-cushion": "Comfort essentials to match your new furniture. Enquire on WhatsApp for current pricing and options.",
    "dining-table": "Solid wood dining sets, made to order — any seating capacity, wood tone and upholstery to match your dining room.",
    "tv-cabinet": "Custom-built TV units and wall panelling, carpentered to your room. Every design shown is a real job we've built — enquire with your room size for a quote.",
    "interior": "Custom carpentry and wall units, built to your room. Enquire on WhatsApp with your space and requirements for a quote.",
}

def parse_frontmatter(fm_text):
    """Minimal parser for the flat scalar frontmatter this CMS collection produces
    (no lists/nesting) — avoids depending on pyyaml being present at build time."""
    d = {}
    for line in fm_text.splitlines():
        line = line.rstrip()
        if not line.strip() or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith('"') and val.endswith('"') and len(val) >= 2:
            val = val[1:-1].replace('\\"', '"')
        elif val.startswith("'") and val.endswith("'") and len(val) >= 2:
            val = val[1:-1]
        if val == "" or val.lower() == "null" or val == "~":
            d[key] = None
        elif re.fullmatch(r"-?\d+", val):
            d[key] = int(val)
        elif re.fullmatch(r"-?\d+\.\d+", val):
            d[key] = float(val)
        else:
            d[key] = val
    return d

def load_products():
    products = []
    for f in sorted(CONTENT.glob("*.md")):
        text = f.read_text()
        if not text.startswith("---"):
            continue
        _, fm, _ = text.split("---", 2)
        d = parse_frontmatter(fm)
        cat = d.get("category")
        if not cat:
            continue
        products.append({
            "sku": d.get("sku", f.stem.upper()),
            "name": d.get("name", "Untitled"),
            "category": cat,
            "categoryLabel": CAT_LABELS.get(cat, cat.title()),
            "price": d.get("price"),
            "specs": d.get("specs", ""),
            "img": (d.get("image") or "").lstrip("/"),
        })
    return products

def main():
    products = load_products()
    present_cats = [c for c in CATEGORY_ORDER if any(p["category"] == c for p in products)]
    categories = [{"slug": c, "label": CAT_LABELS[c], "tag": CAT_TAGS[c]} for c in present_cats]

    config = {
        "brand": "Dream World",
        "tagline": "Beds, Sofas & Furniture — Handcrafted in Dehradun",
        "whatsapp": "918126334038",
        "phone": "+918126334038",
        "address": "Near Wildlife Institute Rd, Chandrabani, Pitthuwala, Dehradun, Uttarakhand",
        "instagram": "https://www.instagram.com/dream_world_mattress",
        "googleMaps": "https://maps.app.goo.gl/jaTr3mSMJ7ZKJaKEA",
        "mapEmbed": "https://www.google.com/maps?q=30.2840005,77.9763792&z=16&output=embed",
        "googleReviews": "",
        "reviewCount": "",
        "owner": {"name": "Ramesh Chaturvedi", "role": "Founder, Dream World", "img": "assets/img/brand/owner.jpg"},
        "categories": categories,
        "categoriesComingSoon": [
            c for c in [
                {"slug": "interior", "label": "Interior", "tag": "Custom carpentry & wall units"},
            ] if c["slug"] not in present_cats
        ],
        "categoryDescriptions": CATEGORY_DESCRIPTIONS,
    }

    js = "// Auto-generated by build_from_cms.py from content/products/*.md — DO NOT hand-edit.\n"
    js += "window.DW_CONFIG = " + json.dumps(config, indent=2, ensure_ascii=False) + ";\n\n"
    js += "window.DW_PRODUCTS = " + json.dumps(products, indent=2, ensure_ascii=False) + ";\n"
    (BUILD / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (BUILD / "assets" / "js" / "data.js").write_text(js)
    print("products:", len(products), "| categories:", [c["slug"] for c in categories])

if __name__ == "__main__":
    main()
