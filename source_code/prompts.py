"""Vision prompt template for nutrition label extraction via the Claude API."""

EXTRACTION_PROMPT = """\
Analyze the provided image of a product label. Your goal is to extract all \
nutrition information into structured JSON.

## Step 1: Determine if Nutrition Data Exists

Check whether the image contains ANY form of nutrition data. This includes:
- Standard "Nutrition Facts" or "Supplement Facts" panels
- European/international "Nutritional Information" tables
- Inline paragraph text listing nutrient amounts (e.g., "Each serving contains \
Vitamin C 60mg, Iron 8mg...")
- Circular, graphical, or non-standard visual layouts showing nutrient values
- Non-English nutrition labels (e.g., "Nahrwertangaben", "Informations nutritionnelles")

If the image is rotated or at an angle, read it as best you can. Orientation \
should not prevent extraction.

If NO nutrition data is present, return JSON with `has_nutrition_data: false` and \
leave nutrients as an empty list.

## Step 2: Extract All Nutrients

For each nutrient found, capture:
- **nutrient_name_raw**: The name exactly as printed on the label (preserve \
original language and casing).
- **amount**: The numeric value. Apply these rules:
  - For "less than" values like `<1g` or `<0.5mg`: return **0.5** times the \
stated threshold (e.g., `<1g` -> `0.5`, `<0.5mg` -> `0.25`). This is a \
documented simplification.
  - For ranges like `1-2g`: return the **midpoint** (e.g., `1.5`).
  - For missing or truly unparseable amounts: return `null`.
- **unit**: The unit of measure (`g`, `mg`, `mcg`, `kcal`, `kJ`, `IU`, `mL`, etc.).
- **percent_reference**: The %DV, %NRV, or %RI value if shown (as a number, not \
a string). `null` if not listed.
- **parent_nutrient**: If this nutrient is a sub-component of another (e.g., \
"Saturated Fat" is under "Total Fat", or "of which Sugars" is under \
"Total Carbohydrate"), set this to the parent nutrient's raw name. Otherwise `null`.

### Special cases:
- **Proprietary blends**: Extract individual ingredients that have amounts listed, \
even within a blend. If only the blend total is shown with no per-ingredient \
breakdown, extract the blend as a single nutrient.
- **Sub-nutrients**: Indented or prefixed items (e.g., "of which Saturated Fat", \
"  Dietary Fiber", "dont Sucres") are sub-nutrients. Identify their parent from \
context (the preceding non-indented nutrient).
- **Calories / Energy**: Extract these like any other nutrient. If both kcal and \
kJ are listed, extract both as separate entries.

## Step 3: Return Structured JSON

Return ONLY valid JSON (no markdown fences, no commentary outside the JSON). \
Use this exact schema:

{{
  "product_image": "{image_filename}",
  "has_nutrition_data": true,
  "product_name": "product name if visible, otherwise null",
  "serving_size": "serving size as printed (e.g., '1 cup (240mL)'), or null",
  "servings_per_container": "as printed (e.g., 'About 8'), or null",
  "nutrients": [
    {{
      "nutrient_name_raw": "exactly as on label",
      "amount": 25.0,
      "unit": "mg",
      "percent_reference": 50.0,
      "parent_nutrient": null
    }}
  ],
  "extraction_notes": "any issues, ambiguities, or observations (null if none)",
  "language_detected": "English"
}}

Important:
- All numeric fields (amount, percent_reference) must be numbers or null, never strings.
- Do NOT invent nutrients that are not on the label.
- If the label is partially obscured, extract what is visible and note the issue \
in extraction_notes.
"""
