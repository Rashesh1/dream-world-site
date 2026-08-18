#!/usr/bin/env python3
"""Generate assets/js/data.js + copy product images into the build."""
import json, shutil
from pathlib import Path

ROOT = Path.home() / "Business" / "Dreamworld Website"
CAT = ROOT / "03_catalog_data" / "catalog.json"
SRC_IMG = ROOT / "02_assets_optimized"
BUILD = ROOT / "05_build"
IMG_OUT = BUILD / "assets" / "img" / "products"

# Draft names (I draft, owner confirms) — in SKU order per category
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
# categories whose real product names come straight from catalog.json (manufacturer-named), not drafted here
NAMED_FROM_CATALOG = {"mattress", "pillow-cushion", "tv-cabinet"}
CAT_LABELS = {"beds":"Beds","sofas":"Sofas","loungers":"Loungers","tables":"Center Tables",
              "sofa-cum-bed":"Sofa-cum-Bed","mattress":"Mattress","pillow-cushion":"Pillow & Cushion",
              "dining-table":"Dining Table","tv-cabinet":"TV Cabinet"}
# category slug -> actual folder name under 02_assets_optimized (some have spaces/typos as given)
CAT_FOLDER = {"beds":"beds","sofas":"sofas","loungers":"loungers","tables":"tables",
              "sofa-cum-bed":"sofa cum bed","mattress":"mattress","pillow-cushion":"pillow and cusions ",
              "dining-table":"dining table ","tv-cabinet":"tv cabinates "}

# Feedback edits
SKIP = {"DW-LOU-05", "DW-TAB-01"}    # remove Rosa Storage Chaise + Heritage Center Table
PRICE_OVERRIDE = {"DW-LOU-04": 20000}  # Isabella Chaise Lounge -> Rs.20,000

def main():
    data = json.loads(CAT.read_text())
    IMG_OUT.mkdir(parents=True, exist_ok=True)
    counters = {}
    products = []
    for r in data["products"]:
        if r["sku"] in SKIP:
            continue
        cat = r["category"]
        counters[cat] = counters.get(cat, 0) + 1
        i = counters[cat] - 1
        name = r["draft_name"] if cat in NAMED_FROM_CATALOG else NAMES[cat][i]
        price = PRICE_OVERRIDE.get(r["sku"], r["price_inr"])
        # copy image
        folder = CAT_FOLDER.get(cat, cat)
        src = SRC_IMG / folder / r["image_file"]
        if src.exists():
            shutil.copy2(src, IMG_OUT / r["image_file"])
        products.append({
            "sku": r["sku"], "name": name, "category": cat,
            "categoryLabel": CAT_LABELS[cat], "price": price,
            "specs": r["specs"], "img": f"assets/img/products/{r['image_file']}",
            "quality": r["image_quality"],
        })
    # config
    config = {
        "brand": "Dream World",
        "tagline": "Beds, Sofas & Furniture — Handcrafted in Dehradun",
        "whatsapp": "918126334038",
        "phone": "+918126334038",
        "address": "Near Wildlife Institute Rd, Chandrabani, Pitthuwala, Dehradun, Uttarakhand",
        "instagram": "https://www.instagram.com/dream_world_mattress",
        "instagramPosts": ["DNXbKJuxARY","DL6oPcuNN2i","DG5NQJfKlrx","DFzzyjBqfIn","DFVGehQvZ2i","DFP8xfJKYI7"],
        "googleMaps": "https://maps.app.goo.gl/jaTr3mSMJ7ZKJaKEA",
        "mapEmbed": "https://www.google.com/maps?q=30.2840005,77.9763792&z=16&output=embed",
        "googleReviews": "",  # paste Google reviews link (for 'read all reviews')
        "reviewCount": "",    # e.g. "120+" once known
        "owner": {"name":"Ramesh Chaturvedi","role":"Founder, Dream World","img":"assets/img/brand/owner.jpg"},
        "categories": [
            {"slug":"beds","label":"Beds","tag":"Upholstered & storage"},
            {"slug":"sofas","label":"Sofas","tag":"Sets & sectionals"},
            {"slug":"sofa-cum-bed","label":"Sofa-cum-Bed","tag":"Space-saving convertibles"},
            {"slug":"loungers","label":"Loungers","tag":"Chaise & diwan"},
            {"slug":"tables","label":"Center Tables","tag":"Solid wood"},
            {"slug":"mattress","label":"Mattress","tag":"Memory foam & spring"},
            {"slug":"pillow-cushion","label":"Pillow & Cushion","tag":"Comfort essentials"},
            {"slug":"dining-table","label":"Dining Table","tag":"Solid wood dining sets"},
            {"slug":"tv-cabinet","label":"TV Cabinet","tag":"Wall units & entertainment units"},
        ],
        "categoriesComingSoon": [
            {"slug":"interior","label":"Interior","tag":"Custom carpentry & wall units"},
        ],
        "categoryDescriptions": {
            "beds": "Every bed is made to order — top 15mm ply, sides 12mm, down 9mm, plyboard work. Choose any size, material and finish to fit your budget.",
            "sofas": "Every sofa is made to order — 40-density foam, leatherette or fabric, thick wood work, 5-year warranty. Choose any size, material and finish to fit your budget.",
            "sofa-cum-bed": "Every sofa-cum-bed is made to order — 64x72 foam size, 78x72 total size, 18mm plywood, 40-density foam. Choose any size, material and finish to fit your budget.",
            "loungers": "Every lounger is made to order — solid wood frame, high-density foam, your choice of upholstery. Choose any size, material and finish to fit your budget.",
            "tables": "Every table is made to order in solid wood — sheesham, acacia or your preferred timber, any size and finish.",
            "mattress": "A range of memory foam, latex and spring mattresses, each with a genuine spec sheet. Enquire on WhatsApp for current pricing — size and firmness can be tailored to you.",
            "pillow-cushion": "Comfort essentials to match your new furniture. Enquire on WhatsApp for current pricing and options.",
            "dining-table": "Solid wood dining sets, made to order — any seating capacity, wood tone and upholstery to match your dining room.",
            "tv-cabinet": "Custom-built TV units and wall panelling, carpentered to your room. Every design shown is a real job we've built — enquire with your room size for a quote.",
        },
    }
    js = "// Auto-generated by build_site_data.py — content layer.\n"
    js += "window.DW_CONFIG = " + json.dumps(config, indent=2, ensure_ascii=False) + ";\n\n"
    js += "window.DW_PRODUCTS = " + json.dumps(products, indent=2, ensure_ascii=False) + ";\n"
    (BUILD / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (BUILD / "assets" / "js" / "data.js").write_text(js)
    print("products:", len(products), "| images copied to", IMG_OUT)

if __name__ == "__main__":
    main()
