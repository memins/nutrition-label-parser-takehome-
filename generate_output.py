"""One-time script to generate CSV output from pre-extracted nutrition data.

The extraction was performed using Claude Vision (via Claude Code agents) on all
13 product images.  This script feeds the extracted data through the normalization
and CSV-writing pipeline to produce the final output.

Usage:
    cd /Users/emin/www/nutrition-label-parser-takehome-
    python generate_output.py
"""

import sys
from pathlib import Path

# Ensure the project root is on the path.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from source_code.models import ExtractionResult, RawNutrient
from source_code.normalizer import normalize_nutrients
from source_code.csv_writer import write_csv
from source_code.config import OUTPUT_DIR, SAMPLE_OUTPUT_DIR, OUTPUT_FILENAME

# ---------------------------------------------------------------------------
# Pre-extracted data for all 13 images
# ---------------------------------------------------------------------------

EXTRACTIONS = [
    # ── product_01.png — MindGuard+ Nootropic Brain Formula ────────────────
    ExtractionResult(
        product_image="product_01.png",
        has_nutrition_data=True,
        product_name="MindGuard+ Nootropic Brain Formula",
        serving_size="2 capsules",
        language_detected="English",
        extraction_notes="Supplement Facts panel for a nootropic brain formula.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Vitamin B6 (as Pyridoxine HCl)", amount=10.0, unit="mg", percent_reference=588.0),
            RawNutrient(nutrient_name_raw="Vitamin B12 (as Methylcobalamin)", amount=250.0, unit="mcg", percent_reference=10417.0),
            RawNutrient(nutrient_name_raw="Bacopa Monnieri Extract", amount=300.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Lion's Mane Mushroom Extract", amount=250.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Phosphatidylserine", amount=150.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Ginkgo Biloba Extract", amount=120.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Rhodiola Rosea Extract", amount=100.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Alpha-GPC", amount=100.0, unit="mg"),
            RawNutrient(nutrient_name_raw="L-Theanine", amount=100.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Acetyl-L-Carnitine", amount=50.0, unit="mg"),
            RawNutrient(nutrient_name_raw="BioPerine (Black Pepper Extract)", amount=5.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Huperzine A", amount=200.0, unit="mcg"),
        ],
    ),
    # ── product_02.png — No nutrition data ─────────────────────────────────
    ExtractionResult(
        product_image="product_02.png",
        has_nutrition_data=False,
        product_name="Vital & Active - Ancient+Brave",
        extraction_notes="Back panel with description and directions only; no nutrition data.",
        language_detected="English",
    ),
    # ── product_03.png — Brave Immunity ────────────────────────────────────
    ExtractionResult(
        product_image="product_03.png",
        has_nutrition_data=True,
        product_name="Brave Immunity",
        serving_size="1.5ml",
        servings_per_container="approx 33",
        language_detected="English",
        extraction_notes="UK/EU-style Nutrition Information panel.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Shiitake Mushroom", amount=34.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Maitake Mushroom", amount=34.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Elderberry", amount=50.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Ginger", amount=47.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Thyme", amount=10.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Vitamin C", amount=75.0, unit="mg", percent_reference=94.0),
        ],
    ),
    # ── product_04.png — No nutrition data ─────────────────────────────────
    ExtractionResult(
        product_image="product_04.png",
        has_nutrition_data=False,
        product_name="Ancient+Brave Brave Immunity Selene",
        extraction_notes="Front panel; no nutrition data present.",
        language_detected="English",
    ),
    # ── product_05.png — No nutrition data ─────────────────────────────────
    ExtractionResult(
        product_image="product_05.png",
        has_nutrition_data=False,
        product_name="Ancient+Brave Brave Immunity",
        extraction_notes="Back panel with description and directions; no quantified nutrition data.",
        language_detected="English",
    ),
    # ── product_06.png — No nutrition data ─────────────────────────────────
    ExtractionResult(
        product_image="product_06.png",
        has_nutrition_data=False,
        product_name="PROMIX Kira Stokes Raw Greens",
        extraction_notes="Front of pouch; no nutrition data visible.",
        language_detected="English",
    ),
    # ── product_07.jpg — Together Health Women's Multi ─────────────────────
    ExtractionResult(
        product_image="product_07.jpg",
        has_nutrition_data=True,
        product_name="Together Health Women's Multi Vit & Mineral",
        serving_size="1 capsule",
        language_detected="English",
        extraction_notes="Inline text format rather than tabular nutrition facts panel.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Vitamin D3", amount=10.0, unit="ug", percent_reference=200.0),
            RawNutrient(nutrient_name_raw="Vitamin E", amount=2.5, unit="mg", percent_reference=21.0),
            RawNutrient(nutrient_name_raw="Vitamin K", amount=25.0, unit="ug", percent_reference=33.0),
            RawNutrient(nutrient_name_raw="Vitamin K2 (as menaquinone-7)", amount=30.0, unit="ug", percent_reference=27.0, parent_nutrient="Vitamin K"),
            RawNutrient(nutrient_name_raw="Vitamin B1", amount=3.0, unit="mg", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Vitamin B2", amount=0.7, unit="mg", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Vitamin B3", amount=8.0, unit="mg", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Vitamin B5", amount=3.0, unit="mg", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Vitamin B6", amount=0.7, unit="mg", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Folic Acid (as Folate)", amount=100.0, unit="ug", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Vitamin B12 (as methylcobalamin)", amount=5.0, unit="ug", percent_reference=200.0),
            RawNutrient(nutrient_name_raw="Biotin", amount=75.0, unit="ug", percent_reference=150.0),
            RawNutrient(nutrient_name_raw="Vitamin C", amount=30.0, unit="mg", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Beta Carotene", amount=500.0, unit="ug"),
            RawNutrient(nutrient_name_raw="Iron", amount=4.2, unit="mg", percent_reference=30.0),
            RawNutrient(nutrient_name_raw="Zinc", amount=5.0, unit="mg", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Copper", amount=0.25, unit="mg", percent_reference=25.0),
            RawNutrient(nutrient_name_raw="Manganese", amount=0.5, unit="mg", percent_reference=25.0),
            RawNutrient(nutrient_name_raw="Selenium", amount=55.0, unit="ug", percent_reference=100.0),
            RawNutrient(nutrient_name_raw="Chromium", amount=13.3, unit="ug", percent_reference=33.0),
            RawNutrient(nutrient_name_raw="Iodine", amount=75.0, unit="ug", percent_reference=50.0),
            RawNutrient(nutrient_name_raw="Molybdenum", amount=15.0, unit="ug", percent_reference=30.0),
        ],
    ),
    # ── product_08.jpg — No nutrition data ─────────────────────────────────
    ExtractionResult(
        product_image="product_08.jpg",
        has_nutrition_data=False,
        product_name="Together Health Women's Wholefood Multivitamin",
        extraction_notes="Front of pouch; no nutrition data visible.",
        language_detected="English",
    ),
    # ── product_09.png — Raw Greens supplement ─────────────────────────────
    ExtractionResult(
        product_image="product_09.png",
        has_nutrition_data=True,
        product_name="Raw Greens Food Supplement",
        serving_size="1 scoop (6.5g)",
        servings_per_container="30",
        language_detected="English",
        extraction_notes="Greens/superfood supplement with category groupings. Some values hard to read due to image resolution.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Energy", amount=84.0, unit="kJ", percent_reference=1.0),
            RawNutrient(nutrient_name_raw="Salt", amount=0.0375, unit="g", percent_reference=0.6),
            RawNutrient(nutrient_name_raw="Potassium", amount=120.0, unit="mg", percent_reference=6.0),
            RawNutrient(nutrient_name_raw="Organic Wheat Grass Powder", amount=3000.0, unit="mg", parent_nutrient="Organic Sprouted Greens"),
            RawNutrient(nutrient_name_raw="Organic Alfalfa Leaf Powder", amount=1000.0, unit="mg", parent_nutrient="Organic Sprouted Greens"),
            RawNutrient(nutrient_name_raw="Matcha Tea Leaf Powder", amount=750.0, unit="mg", parent_nutrient="Antioxidants And Recovery"),
            RawNutrient(nutrient_name_raw="Organic Jerusalem Artichoke Root Inulin", amount=500.0, unit="mg", parent_nutrient="Prebiotic Fibres"),
            RawNutrient(nutrient_name_raw="Ashwagandha Root Extract", amount=100.0, unit="mg", parent_nutrient="Adaptogens"),
        ],
    ),
    # ── product_10.png — MindGuard (rotated) ───────────────────────────────
    ExtractionResult(
        product_image="product_10.png",
        has_nutrition_data=True,
        product_name="MindGuard Nootropic Brain Formula",
        serving_size="2 capsules",
        language_detected="English",
        extraction_notes="Rotated 90 degrees. Same product as product_01 with slightly different values — treated as independent image per plan.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Vitamin B6 (as Pyridoxine HCl)", amount=10.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Vitamin B12 (as Methylcobalamin)", amount=500.0, unit="mcg"),
            RawNutrient(nutrient_name_raw="Bacopa Monnieri Extract", amount=300.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Lion's Mane Mushroom Extract", amount=250.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Phosphatidylserine", amount=100.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Ginkgo Biloba Extract", amount=120.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Rhodiola Rosea Extract", amount=200.0, unit="mg"),
            RawNutrient(nutrient_name_raw="L-Theanine", amount=150.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Alpha-GPC", amount=150.0, unit="mg"),
        ],
    ),
    # ── product_11.png — Omega-3 detailed ──────────────────────────────────
    ExtractionResult(
        product_image="product_11.png",
        has_nutrition_data=True,
        product_name="Omega-3 Fish Oil Supplement",
        serving_size="1 Softgel (1.2g)",
        servings_per_container="60",
        language_detected="English",
        extraction_notes="Omega-3 supplement with detailed sub-nutrient hierarchy. European NRV% format.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Energy", amount=42.0, unit="kJ", percent_reference=0.5),
            RawNutrient(nutrient_name_raw="Total Fat", amount=1.0, unit="g", percent_reference=1.6),
            RawNutrient(nutrient_name_raw="of which Saturates", amount=0.3, unit="g", parent_nutrient="Total Fat"),
            RawNutrient(nutrient_name_raw="of which Monounsaturates", amount=0.5, unit="g", parent_nutrient="Total Fat"),
            RawNutrient(nutrient_name_raw="of which Polyunsaturates", amount=0.5, unit="g", parent_nutrient="Total Fat"),
            RawNutrient(nutrient_name_raw="Concentrated Omega-3 Fatty Acids", amount=900.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Total Omega-3 Fatty Acids", amount=710.0, unit="mg", parent_nutrient="Concentrated Omega-3 Fatty Acids"),
            RawNutrient(nutrient_name_raw="EPA (Eicosapentaenoic Acid)", amount=500.0, unit="mg", parent_nutrient="Total Omega-3 Fatty Acids"),
            RawNutrient(nutrient_name_raw="DHA (Docosahexaenoic Acid)", amount=100.0, unit="mg", parent_nutrient="Total Omega-3 Fatty Acids"),
            RawNutrient(nutrient_name_raw="Other Omega-3s", amount=110.0, unit="mg", parent_nutrient="Total Omega-3 Fatty Acids"),
            RawNutrient(nutrient_name_raw="Vitamin E (as d-Alpha-Tocopherol)", amount=15.0, unit="mg", percent_reference=125.0, parent_nutrient="Antioxidant and Stability Matrix"),
            RawNutrient(nutrient_name_raw="Rosemary Extract", amount=5.0, unit="mg", parent_nutrient="Antioxidant and Stability Matrix"),
        ],
    ),
    # ── product_12.png — Circular/graphical layout ─────────────────────────
    ExtractionResult(
        product_image="product_12.png",
        has_nutrition_data=True,
        product_name="Omega-3 Fish Oil Softgel",
        serving_size="1 Softgel (1.2g)",
        servings_per_container="60",
        language_detected="English",
        extraction_notes="Concentric-ring/graphical layout. Successfully extracted despite non-standard visual format.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Energy", amount=15.0, unit="kcal"),
            RawNutrient(nutrient_name_raw="Total Fat", amount=1.2, unit="g", percent_reference=1.5),
            RawNutrient(nutrient_name_raw="Saturated Fat", amount=0.4, unit="g", parent_nutrient="Total Fat"),
            RawNutrient(nutrient_name_raw="Trans Fat", amount=0.0, unit="g", parent_nutrient="Total Fat"),
            RawNutrient(nutrient_name_raw="Polyunsaturated Fat", amount=0.9, unit="g", parent_nutrient="Total Fat"),
            RawNutrient(nutrient_name_raw="Monounsaturated Fat", amount=0.13, unit="g", parent_nutrient="Total Fat"),
            RawNutrient(nutrient_name_raw="Cholesterol", amount=5.0, unit="mg", percent_reference=1.7),
            RawNutrient(nutrient_name_raw="Total Omega-3 Fatty Acids", amount=900.0, unit="mg"),
            RawNutrient(nutrient_name_raw="EPA", amount=500.0, unit="mg", parent_nutrient="Total Omega-3 Fatty Acids"),
            RawNutrient(nutrient_name_raw="DHA", amount=250.0, unit="mg", parent_nutrient="Total Omega-3 Fatty Acids"),
            RawNutrient(nutrient_name_raw="Total Omega-6 Fatty Acids", amount=15.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Protein", amount=0.5, unit="g"),
            RawNutrient(nutrient_name_raw="Vitamin E", amount=5.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Rosemary Extract", amount=0.15, unit="mg"),
        ],
    ),
    # ── product_13.png — German label ──────────────────────────────────────
    ExtractionResult(
        product_image="product_13.png",
        has_nutrition_data=True,
        product_name="NordHerz OMEGA-3 1000 mg Fischöl",
        serving_size="Tagesdosis: 2 Kapseln",
        servings_per_container="30",
        language_detected="German",
        extraction_notes="German supplement label (Nahrungsergänzungsmittel). Nutrient names preserved in original German.",
        nutrients=[
            RawNutrient(nutrient_name_raw="Fischöl", amount=2000.0, unit="mg"),
            RawNutrient(nutrient_name_raw="Omega-3-Fettsäuren", amount=1800.0, unit="mg", parent_nutrient="Fischöl"),
            RawNutrient(nutrient_name_raw="EPA (Eicosapentaensäure)", amount=1000.0, unit="mg", parent_nutrient="Omega-3-Fettsäuren"),
            RawNutrient(nutrient_name_raw="DHA (Docosahexaensäure)", amount=500.0, unit="mg", parent_nutrient="Omega-3-Fettsäuren"),
            RawNutrient(nutrient_name_raw="Vitamin E", amount=12.0, unit="mg", percent_reference=100.0),
        ],
    ),
]


def main() -> None:
    all_nutrients = []
    images_with_data = 0

    for extraction in EXTRACTIONS:
        if extraction.has_nutrition_data:
            images_with_data += 1
            normalized = normalize_nutrients(extraction)
            all_nutrients.extend(normalized)
            print(
                f"  + {extraction.product_image}: "
                f"{len(normalized)} nutrient(s)"
            )
        else:
            print(f"  - {extraction.product_image}: no nutrition data")

    # Write to both output/ and sample_output/
    for out_dir in (OUTPUT_DIR, SAMPLE_OUTPUT_DIR):
        out_path = out_dir / OUTPUT_FILENAME
        write_csv(all_nutrients, out_path)
        print(f"  Written: {out_path}")

    print(
        f"\nDone — 13 images, {images_with_data} with data, "
        f"{len(all_nutrients)} total nutrients."
    )


if __name__ == "__main__":
    main()
