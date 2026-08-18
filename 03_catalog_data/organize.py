#!/usr/bin/env python3
"""Organize Dream World WhatsApp catalog into categorized assets + structured data."""
import csv, json, shutil
from pathlib import Path

ROOT = Path.home() / "Business" / "Dreamworld Website"
RAW = ROOT / "01_catalog_raw"
ASSETS = ROOT / "02_assets_optimized"
DATA = ROOT / "03_catalog_data"

# id -> (category, price, specs, quality, notes)
# quality: OK | SCREENSHOT | WATERMARK | LOWRES
CATALOG = [
    # ---- BEDS (upholstered / storage) ----
    ("00000038", "beds",     22000, "Top 15mm ply, sides 12mm, down 9mm, plyboard work", "OK",        "Cream shell headboard, storage"),
    ("00000040", "beds",     23000, "Storage drawer bed",                                  "OK",        "Beige leatherette, tufted, drawer"),
    ("00000042", "beds",     18000, "Hydraulic/drawer storage, LED headboard",             "OK",        "Wood-tone, warm room render"),
    ("00000044", "beds",     26000, "Wingback, gold trim, diamond-quilt sides",            "OK",        "Cream, most premium bed"),
    ("00000046", "beds",     20000, "Wingback channel headboard, gold piping",             "OK",        "Cream+brown, arch window scene"),
    ("00000048", "beds",     22000, "Channel-tufted wing headboard, gold trim",            "OK",        "Grey, night scene"),
    ("00000050", "beds",     22000, "Vertical channel velvet headboard",                   "OK",        "Black velvet, classic room"),
    ("00000052", "beds",     18000, "Fluted fan headboard, gold legs",                     "OK",        "Grey velvet, bright room"),
    ("00000054", "beds",     17000, "Cushion wingback headboard",                          "OK",        "Cream, minimal beige room"),
    ("00000056", "beds",     18000, "Diamond-quilt headboard, gold frame",                 "WATERMARK", "Grey; 'LUXURY HOME' watermark"),
    ("00000058", "beds",     20000, "Fluted headboard, gold legs",                         "OK",        "Grey, white bright room"),
    # ---- SOFAS (sets / sectionals) ----
    ("00000060", "sofas",    35000, "40-density foam, leatherette, thick wood, 5yr warranty","SCREENSHOT","Cream sectional; app status bar"),
    ("00000062", "sofas",    30000, "Curved modular sectional",                            "SCREENSHOT","Cream curved; app status bar"),
    ("00000064", "sofas",    35000, "L-shape 6-seat set + 2 poufs + glass center table",   "OK",        "Blue; real showroom photo"),
    ("00000066", "sofas",    16000, "Accent tub-chair pair (sofa only)",                   "WATERMARK", "Green velvet; 'PIZAP' watermark"),
    ("00000068", "sofas",    18000, "Accent chair pair",                                   "LOWRES",    "Grey; composited room"),
    ("00000070", "sofas",    25000, "3-piece sofa set (1+2+... )",                          "LOWRES",    "Orange; composited room"),
    ("00000076", "sofas",    25000, "Office/parlour leatherette set (3+1+1)",              "OK",        "Beige; clean product photo"),
    ("00000078", "sofas",    30000, "L-shape fabric sectional",                            "WATERMARK", "Beige; 'MADE IN INDIA' watermark"),
    ("00000080", "sofas",    30000, "Sofa set 3+1+1 with center table",                    "OK",        "Beige leatherette; clean"),
    ("00000082", "sofas",    32000, "Leather sofa set 3+1+1 + wood center table",          "OK",        "Tan/brown; clean"),
    # ---- LOUNGERS / CHAISE / DIWAN ----
    ("00000084", "loungers", 17000, "Roll-arm chaise lounge",                              "SCREENSHOT","Cream; Amazon screenshot"),
    ("00000086", "loungers", 18000, "Shell-back chaise lounge, gold legs",                 "SCREENSHOT","Blue velvet; app status bar"),
    ("00000088", "loungers", 18000, "Chesterfield tufted chaise, turned legs",             "SCREENSHOT","Beige; app status bar"),
    ("00000090", "loungers", 18000, "Chesterfield tufted chaise (dup of 088 image)",       "LOWRES",    "Cream; same photo as 088"),
    ("00000092", "loungers", 20000, "Roll-arm storage chaise",                             "LOWRES",    "Mauve/pink"),
    ("00000094", "loungers", 16000, "Modern chaise lounge, bolster",                       "LOWRES",    "Teal/green"),
    ("00000096", "loungers", 16000, "Chesterfield chaise, turned legs",                    "LOWRES",    "Navy velvet"),
    # ---- TABLES (coffee / center) ----
    ("00000098", "tables",   18000, "Sheesham wood center table with shelf",               "WATERMARK", "'KHATICRAFT' watermark"),
    ("00000107", "tables",    5000, "Small wooden 4-leg table",                            "LOWRES",    "Plain, radiator scene"),
    ("00000109", "tables",    8000, "Carved wood glass-top coffee table",                  "LOWRES",    "Ornate carved base"),
    ("00000111", "tables",    8000, "Live-edge small coffee table, U legs",                "LOWRES",    "Acacia + black legs"),
    ("00000113", "tables",    6000, "Carved wood glass-top table frame",                   "LOWRES",    "Traditional carved"),
    ("00000115", "tables",    8000, "Sheesham slatted coffee table with shelf",            "OK",        "Honey sheesham"),
]

# logo + extras (not priced products)
SPECIAL = [
    ("00000033", "brand", "LOGO: 'DREAM WORLD SOFA' gold-on-black oval. Remove word SOFA -> 'DREAM WORLD'. Recreate as SVG."),
    ("00000013", "unpriced", "Sofa-cum-bed (convertible) - front + open views. NO PRICE YET - ask owner."),
    ("00000014", "unpriced", "Clean white-bg bed cutout (usable catalog image)."),
]

def find(idp):
    for f in RAW.glob(f"{idp}-*.jpg"):
        return f
    return None

def slug_counts():
    return {}

def main():
    counts = {}
    rows = []
    for cat in ("beds","sofas","loungers","tables","brand"):
        (ASSETS / cat).mkdir(parents=True, exist_ok=True)
    for idp, cat, price, specs, quality, notes in CATALOG:
        counts[cat] = counts.get(cat, 0) + 1
        n = counts[cat]
        src = find(idp)
        slug = f"{cat[:-1] if cat.endswith('s') else cat}-{n:02d}"
        dstname = f"{slug}.jpg"
        if src:
            shutil.copy2(src, ASSETS / cat / dstname)
        rows.append({
            "sku": f"DW-{cat[:3].upper()}-{n:02d}",
            "category": cat,
            "draft_name": f"{cat[:-1].title()} Design {n:02d}",
            "price_inr": price,
            "specs": specs,
            "image_file": dstname,
            "source_image": src.name if src else "MISSING",
            "image_quality": quality,
            "needs": "name, size, colours, material, warranty",
            "notes": notes,
        })
    # special
    for idp, kind, notes in SPECIAL:
        src = find(idp)
        if src:
            shutil.copy2(src, ASSETS / "brand" / f"{kind}-{idp}.jpg")
    # write CSV
    with open(DATA / "catalog.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    # write JSON (site-ready shape)
    with open(DATA / "catalog.json", "w") as fh:
        json.dump({"currency": "INR", "products": rows}, fh, indent=2)
    # summary
    print("Products:", len(rows))
    for c in ("beds","sofas","loungers","tables"):
        cr = [r for r in rows if r["category"] == c]
        pr = [r["price_inr"] for r in cr]
        print(f"  {c}: {len(cr)}  price Rs.{min(pr)}-{max(pr)}")
    qbad = [r for r in rows if r["image_quality"] != "OK"]
    print("Images needing replacement (not OK):", len(qbad), "/", len(rows))

if __name__ == "__main__":
    main()
