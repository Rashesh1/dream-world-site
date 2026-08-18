#!/usr/bin/env python3
"""One-time migration: catalog.json -> content/products/<sku>.md (one file per product,
frontmatter only). This becomes the CMS-editable source of truth going forward.
Run build_from_cms.py afterwards (and on every future edit) to regenerate data.js."""
import json, shutil
from pathlib import Path

def to_frontmatter(d):
    lines = []
    for k, v in d.items():
        if v is None:
            lines.append(f"{k}: null")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            s = str(v).replace('\\', '\\\\').replace('"', '\\"')
            lines.append(f'{k}: "{s}"')
    return "\n".join(lines)

ROOT = Path.home() / "Business" / "Dreamworld Website"
CAT = ROOT / "03_catalog_data" / "catalog.json"
SRC_IMG = ROOT / "02_assets_optimized"
CONTENT = ROOT / "content" / "products"
UPLOADS = ROOT / "05_build" / "assets" / "img" / "uploads"

CAT_FOLDER = {"beds":"beds","sofas":"sofas","loungers":"loungers","tables":"tables",
              "sofa-cum-bed":"sofa cum bed","mattress":"mattress","pillow-cushion":"pillow and cusions ",
              "dining-table":"dining table ","tv-cabinet":"tv cabinates "}
NAMED_FROM_CATALOG = {"mattress", "pillow-cushion", "tv-cabinet"}

# same draft-name lists as build_site_data.py (frozen at migration time)
NAMES = {
    "beds": ["Camellia Storage Bed","Milano Drawer Bed","Aspen Storage Bed","Regalia Wingback Bed",
             "Verona Wingback Bed","Onyx Channel Bed","Noir Velvet Bed","Celeste Fluted Bed",
             "Serene Cushion Bed","Sterling Quilted Bed","Halcyon Fluted Bed"],
    "sofas": ["Cloud Sectional Sofa","Arc Modular Sofa","Azure L-Shape Set","Emerald Lounge Pair",
              "Ash Lounge Pair","Sienna Sofa Set","Bianca Sofa Set","Dune Sectional Sofa",
              "Cortland Sofa Set","Cognac Leather Set"],
    "loungers": ["Juliet Chaise Lounge","Sapphire Chaise Lounge","Windsor Chaise Lounge",
                 "Isabella Chaise Lounge","Jade Chaise Lounge","Marine Chaise Lounge"],
    "tables": ["Petite Coffee Table","Nawab Glass-Top Table",
               "Timber Live-Edge Table","Darbar Carved Table","Rustic Sheesham Table",
               "Amber Nesting Table","Willow Side Table","Copper-Leg Coffee Table","Birch Coffee Table",
               "Sundar Coffee Table","Marigold Coffee Table","Ivory Coffee Table",
               "Kanha Coffee Table","Teak Coffee Table","Meadow Coffee Table"],
    "sofa-cum-bed": ["Walnut Daybed","Blue Trundle Sofa-Bed","Sage Trundle Sofa-Bed","Mosaic Carved Daybed",
                      "Sheesham Carved Daybed","Terracotta Tile-Inlay Daybed","Ivory Geometric Daybed",
                      "Hexagon Wood-Arm Daybed","Heritage Cross-Panel Daybed","Indigo Console Sofa-Bed",
                      "Merlot Velvet Pull-Out","Azure Fabric Pull-Out","Rajwada Lattice Diwan",
                      "Slate Corner Sofa-Bed","Blossom Cross-Panel Daybed","Cloud Pull-Out Sofa"],
    "dining-table": ["Windsor 6-Seater Dining Set","Kanhaiya 8-Seater Dining Set","Bramha 6-Seater Dining Set",
                      "Rani 6-Seater Dining Set","Sundari 6-Seater Dining Set","Meera 6-Seater Dining Set",
                      "Ganga 6-Seater Dining Set","Yamuna 6-Seater Dining Set","Ashoka 6-Seater Dining Set",
                      "Vedika 6-Seater Dining Set","Raunak 8-Seater Dining Set","Kaveri 8-Seater Dining Set",
                      "Narmada 6-Seater Dining Set"],
}
SKIP = {"DW-LOU-05", "DW-TAB-01"}
PRICE_OVERRIDE = {"DW-LOU-04": 20000}

CATEGORY_THUMB_OVERRIDE = {
    "sofa-cum-bed": "assets/img/categories/sofa-cum-bed.jpg",
    "mattress": "assets/img/categories/mattress.jpg",
    "dining-table": "assets/img/categories/dining-table.jpg",
    "tv-cabinet": "assets/img/categories/tv-cabinet.jpg",
}

def main():
    data = json.loads(CAT.read_text())
    CONTENT.mkdir(parents=True, exist_ok=True)
    UPLOADS.mkdir(parents=True, exist_ok=True)
    counters = {}
    n_written = 0
    for r in data["products"]:
        if r["sku"] in SKIP:
            continue
        cat = r["category"]
        counters[cat] = counters.get(cat, 0) + 1
        i = counters[cat] - 1
        name = r["draft_name"] if cat in NAMED_FROM_CATALOG else NAMES[cat][i]
        price = PRICE_OVERRIDE.get(r["sku"], r["price_inr"])

        folder = CAT_FOLDER.get(cat, cat)
        src = SRC_IMG / folder / r["image_file"]
        dest_name = f"{r['sku'].lower()}.jpg"
        if src.exists():
            shutil.copy2(src, UPLOADS / dest_name)
        img_path = f"/assets/img/uploads/{dest_name}"

        entry = {
            "sku": r["sku"],
            "name": name,
            "category": cat,
            "price": price,  # null = "Enquire for price"
            "specs": r["specs"],
            "image": img_path,
        }
        out = CONTENT / f"{r['sku'].lower()}.md"
        out.write_text("---\n" + to_frontmatter(entry) + "\n---\n")
        n_written += 1

    print("migrated products:", n_written, "->", CONTENT)
    print("uploaded images:", len(list(UPLOADS.glob('*.jpg'))))

if __name__ == "__main__":
    main()
