#!/usr/bin/env python3
"""Append Sofa-cum-bed, Mattress and Pillow&Cushion products to catalog.json (additive, no touch to existing rows)."""
import json
from pathlib import Path

DATA = Path.home() / "Business" / "Dreamworld Website" / "03_catalog_data"
CAT = DATA / "catalog.json"

SCB_DESC = "64x72 foam size, total size 78x72, Theek wood ply, 18mm plywood, 40 density foam"
SCB = [(1,25000),(2,25000),(3,25000),(4,25000),(5,25000),(6,25000),(7,25000),(8,25000),
       (9,25000),(10,25000),(11,25000),(12,25000),(13,25000),(14,25000),(15,20000),(16,20000)]

MATTRESS = [
    (1,"Ultimate Comfort Mattress","Rebonded 100mm, Natural Latex 50mm, Memory Foam 100mm, Milanche fabric, 10\" thick, 10yr warranty"),
    (2,"Rest Full Dreams Mattress","Rebonded 100mm, HR Foam 50mm, Natural Latex 50mm, Milanche fabric, 8\" thick, 10yr warranty"),
    (3,"Elegence Mattress","Bonded 100mm, HR Foam 50mm, Memory Foam 50mm, Milanche fabric, 8\"/10\" thick, 7yr warranty"),
    (4,"Night King Mattress","50mm Memory Foam, 25mm 040 Density HR Foam, 75mm Rebonded, Knitted fabric, 6\" thick, 7yr warranty"),
    (5,"Jump on Plus Mattress","Premium Foam 50mm/10mm 32 Density, Bonnell Spring, Knitted Jacquard fabric, 8\"/10\"/12\" thick, 7yr warranty"),
    (6,"Pecific Eurotop Mattress","Rebonded 90mm, 40 Density 30mm HR Foam, Milanche Visco Spunn fabric, 5\" thick, 12yr warranty"),
    (7,"Eco Bond Mattress","Rebonded 115mm, Knitted Jacquard fabric, 5\" thick, 9yr warranty, orthopedic support"),
    (8,"Euro Night Mattress","32 Density 35mm Super Premium Foam, White Block Sheet 40mm, Rebonded 35mm, Knitted Jacquard, 5\" thick, 5yr warranty"),
    (9,"Lotus Mattress","Rebonded 30mm, White Block Sheet 50mm, Rebonded 30mm, American Knitted fabric, 5\" thick, 4yr warranty"),
    (10,"Ortho Plus Mattress","32 Density 40mm Super Premium Foam, White Block Sheet 70mm, Rebonded 30mm, Half Knitted fabric, 6\" thick, 3yr warranty"),
    (11,"Gold Mattress","28 Density 115mm Super Premium Foam, Half Knitted fabric, 5\"/6\" thick, 3yr warranty"),
    (12,"Silver Mattress","28 Density 100mm Foam, Drill Cloth fabric, 4\"/5\" thick, 2yr warranty"),
]

PILLOW = [
    (1,"Two Fold Pillow","Soft two-fold pillow, breathable cover, everyday comfort"),
    (2,"Comfort Cool Pillow","Cooling-touch pillow with contrast piped edge, extra support"),
]

def main():
    data = json.loads(CAT.read_text())
    rows = data["products"]

    for n, price in SCB:
        rows.append({
            "sku": f"DW-SCB-{n:02d}", "category": "sofa-cum-bed",
            "draft_name": f"Sofa-cum-Bed Design {n:02d}",
            "price_inr": price, "specs": SCB_DESC,
            "image_file": f"scb-{n:02d}.jpg",
            "source_image": "", "image_quality": "OK",
            "needs": "name confirm", "notes": "batch2 sofa-cum-bed",
        })

    for n, name, specs in MATTRESS:
        rows.append({
            "sku": f"DW-MAT-{n:02d}", "category": "mattress",
            "draft_name": name,
            "price_inr": None, "specs": specs,
            "image_file": f"mat-{n:02d}-{name.lower().replace(' mattress','').replace(' ','-')}.jpg",
            "source_image": "", "image_quality": "OK",
            "needs": "price (enquire-only)", "notes": "batch2 mattress catalog",
        })

    for n, name, specs in PILLOW:
        rows.append({
            "sku": f"DW-PIL-{n:02d}", "category": "pillow-cushion",
            "draft_name": name,
            "price_inr": None, "specs": specs,
            "image_file": ["pillow-01-two-fold.jpg","pillow-02-comfort-cool.jpg"][n-1],
            "source_image": "", "image_quality": "OK",
            "needs": "price (enquire-only)", "notes": "batch2 pillow catalog",
        })

    CAT.write_text(json.dumps(data, indent=2))
    print("total products now:", len(rows))
    for c in ("sofa-cum-bed","mattress","pillow-cushion"):
        print(" ", c, len([r for r in rows if r["category"]==c]))

if __name__ == "__main__":
    main()
