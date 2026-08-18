#!/usr/bin/env python3
"""Append Dining Table, TV Cabinet and 9 more Center Table products."""
import json
from pathlib import Path

DATA = Path.home() / "Business" / "Dreamworld Website" / "03_catalog_data"
CAT = DATA / "catalog.json"

TABLE_DESC = "Made to order in solid wood — sheesham, acacia or your preferred timber, any size and finish."
NEW_TABLES = [(7,17000),(8,7000),(9,8000),(10,9000),(11,16000),(12,17000),(13,9000),(14,8000),(15,9000)]

DINING_DESC = "Solid wood dining set, made to order — any seating capacity, wood tone and upholstery to match your dining room."
DINING = [(1,75000),(2,55000),(3,55000),(4,65000),(5,65000),(6,55000),(7,60000),
          (8,55000),(9,55000),(10,55000),(11,80000),(12,75000),(13,55000)]

TVC_DESC = "Custom-built TV units and wall panelling, designed and carpentered to your room. Every job shown here was built to order — enquire with your room size for a quote."
TVC_PICKS = [1,5,7,10,13,16]  # curated indices from tvcab-01..tvcab-18

def main():
    data = json.loads(CAT.read_text())
    rows = data["products"]

    for n, price in NEW_TABLES:
        rows.append({
            "sku": f"DW-TAB-{n:02d}", "category": "tables",
            "draft_name": f"Table Design {n:02d}",
            "price_inr": price, "specs": TABLE_DESC,
            "image_file": f"table-{n:02d}.jpg",
            "source_image": "", "image_quality": "OK",
            "needs": "name confirm", "notes": "batch3 tables",
        })

    for n, price in DINING:
        rows.append({
            "sku": f"DW-DIN-{n:02d}", "category": "dining-table",
            "draft_name": f"Dining Set Design {n:02d}",
            "price_inr": price, "specs": DINING_DESC,
            "image_file": f"dining-{n:02d}.jpg",
            "source_image": "", "image_quality": "OK",
            "needs": "name confirm", "notes": "batch3 dining table",
        })

    for i, n in enumerate(TVC_PICKS, 1):
        rows.append({
            "sku": f"DW-TVC-{i:02d}", "category": "tv-cabinet",
            "draft_name": f"Custom TV Unit — Design {i:02d}",
            "price_inr": None, "specs": TVC_DESC,
            "image_file": f"tvcab-{n:02d}.jpg",
            "source_image": "", "image_quality": "OK",
            "needs": "price (enquire-only)", "notes": "batch3 tv cabinet/interior carpentry",
        })

    CAT.write_text(json.dumps(data, indent=2))
    print("total products now:", len(rows))
    for c in ("tables","dining-table","tv-cabinet"):
        print(" ", c, len([r for r in rows if r["category"]==c]))

if __name__ == "__main__":
    main()
