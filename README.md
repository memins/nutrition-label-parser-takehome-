# Nutrition Label Parser

A system that extracts structured, normalised nutritional information from product label images using Claude Vision API.

**Input:** 13 product label images (varying layouts, languages, and formats)
**Output:** A flat CSV with canonical nutrient names, amounts, and units

---

## What I Built

### Architecture: Claude Vision API as the sole extraction engine

The core design decision was to use Claude's vision model as a single-pass extraction engine rather than building a traditional OCR + regex + table-structure-inference pipeline. This handles layout variation, rotation, foreign languages, circular layouts, and inline text natively — no preprocessing needed.

The system has three stages:

```
Image --> [Extractor] --> raw JSON --> [Normalizer] --> canonical names/units --> [CSV Writer] --> output
```

**Extractor** (`extractor.py` + `prompts.py`): Sends each image to Claude with a carefully crafted prompt. Returns structured JSON with raw nutrient names exactly as printed on the label.

**Normalizer** (`normalizer.py` + `nutrient_map.py`): Pure-function layer that maps raw names to canonical snake_case identifiers and standardises units. Uses a 4-step resolution: exact lookup, parenthetical stripping, substring matching, snake_case fallback. No nutrient is ever silently dropped.

**CSV Writer** (`csv_writer.py`): Flattens normalised nutrients into a sorted CSV.

### Project structure

```
source_code/
    main.py              # CLI entry point, orchestrates pipeline
    config.py            # Constants, paths, API settings
    models.py            # Pydantic models (RawNutrient, ExtractionResult, NormalizedNutrient)
    extractor.py         # Claude Vision API integration
    prompts.py           # Vision prompt template (separated for easy iteration)
    normalizer.py        # Nutrient name + unit standardisation logic
    nutrient_map.py      # Canonical name mapping dictionary (~150 entries)
    csv_writer.py        # DataFrame construction + CSV output
    test_normalizer.py   # 26 pytest cases for the pure-function normalizer
sample_output/
    nutrition_data.csv   # Pre-generated output (88 nutrients from 8 images)
```

### Schema extensions

I extended the suggested 5-column schema to 8 columns:

| Column | Why |
|--------|-----|
| `percent_reference` | Real data present on most labels (%DV, %NRV). Cheap to include, valuable for downstream analysis. |
| `parent_nutrient` | Preserves nutrient hierarchy (e.g., "Saturated Fat" under "Total Fat", "EPA" under "Total Omega-3"). A flat CSV can't represent trees, but a parent pointer recovers the structure. |
| `serving_size` | Amounts are meaningless without it. Different products use different serving sizes, so cross-product comparison requires this field. |

### Image analysis results

| Image | Has data? | Format | Notes |
|-------|-----------|--------|-------|
| product_01 | Yes | Supplement Facts panel | Nootropic brain formula, 12 nutrients |
| product_02 | No | Description only | Back panel, no nutrition data |
| product_03 | Yes | UK/EU Nutrition Info table | Mushroom tincture, 6 nutrients |
| product_04 | No | Front branding | No nutrition data |
| product_05 | No | Directions only | No nutrition data |
| product_06 | No | Front branding | No nutrition data |
| product_07 | Yes | Inline paragraph text | Women's multivitamin, 22 nutrients |
| product_08 | No | Front branding | No nutrition data |
| product_09 | Yes | Supplement Facts (white bg) | Raw greens, 8 nutrients with categories |
| product_10 | Yes | Supplement Facts (rotated 90 deg) | Same product as 01, rotated |
| product_11 | Yes | Detailed with sub-nutrients | Omega-3 with EPA/DHA hierarchy |
| product_12 | Yes | Circular/graphical layout | Concentric ring design, 14 nutrients |
| product_13 | Yes | German language | NordHerz Omega-3, 5 nutrients |

---

## What I Decided Not to Build

**No OCR or image preprocessing.** Traditional OCR (Tesseract, etc.) would require solving rotation detection, table structure inference, language detection, and text-region segmentation — each a hard subproblem. Claude Vision handles all of these natively. This is the highest-leverage decision in the project.

**No unit conversion.** "Vitamin E 5 mg" and "Vitamin E 7.5 IU" are kept in their original units. Converting between units (mg/IU/mcg) requires nutrient-specific conversion factors and assumptions about the chemical form. Getting this wrong silently corrupts data. Better to preserve what the label says and convert downstream when the use case is clear.

**No product deduplication.** Products 01 and 10 are the same supplement photographed differently. I treat each image independently because product identity resolution (matching across images) is a separate, harder problem. The plan explicitly calls this out.

**No full German translation.** German nutrient names are normalised where mappings exist (Kohlenhydrate -> total_carbohydrate, Eiweiß -> protein, Fischöl -> fish_oil), but I don't translate every term. Full translation is scope creep — the normaliser handles what it knows and passes through what it doesn't.

**No async/parallel API calls.** The pipeline processes images sequentially. For 13 images this takes ~2 minutes. At scale, you'd want asyncio with a rate limiter, but that's premature optimisation for this volume.

---

## The Hardest Part

### 1. Substring matching false positives

The normaliser uses substring matching as step 3 (after exact lookup and parenthetical stripping fail). This caused "of which Monounsaturates" to incorrectly match "saturates" -> `saturated_fat`, because "saturates" is literally a substring of "monounsaturates".

**Resolution:** Added explicit map entries for all "of which" EU-style fat sub-categories. The fix is data, not logic — the normaliser's algorithm is sound, it just needed a more complete dictionary. The "longest key wins" heuristic helps here, but explicit entries are more reliable.

### 2. Energy disambiguation (kcal vs kJ)

Many labels just say "Energy" and list the value in either kcal or kJ (or both). The normaliser maps names without considering units, so "Energy" always became `energy_kcal`. But when the unit is kJ, that's wrong.

**Resolution:** Added a post-normalisation correction in `normalize_nutrients()`: if the standard name is `energy_kcal` but the unit is `kJ`, flip it to `energy_kj`. This is the only place the normaliser considers the unit — it's a targeted fix for a specific ambiguity rather than a general redesign.

### 3. How much hierarchy to preserve in a flat CSV

Product 11 has 3 levels: "Concentrated Omega-3 Fatty Acids" > "Total Omega-3 Fatty Acids" > "EPA". A flat CSV can't represent this directly.

**Resolution:** The `parent_nutrient` column stores the immediate parent's raw name. This recovers the full tree with a simple self-join while keeping the CSV flat and tool-friendly. It adds one column but avoids the complexity of nested output formats.

### 4. What counts as "nutrition data"

Product 05 mentions "Vitamin C, Shiitake and Maitake mushrooms" in its description text — but as ingredient names without amounts. Product 07 lists nutrients with amounts in inline paragraph text (not a table).

**Resolution:** The rule is: if there are quantified amounts, it's nutrition data. Mentioning a nutrient by name without a number is marketing copy, not data. The prompt explicitly instructs Claude to look for amounts, not just names.

### 5. The `<1` amount problem

Labels use `<1g` to mean "some nonzero amount less than 1 gram." Storing `null` loses the "nonzero" information. Storing `1` overstates.

**Resolution:** Store 0.5x the threshold (`<1g` -> `0.5g`, `<0.5mg` -> `0.25mg`). This is documented, predictable, and preserves the "nonzero" signal. The prompt instructs Claude to apply this rule.

---

## Running the Pipeline

### Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Option 1: With Anthropic API Key

This is the production path — each image is sent to the Claude Vision API for extraction.

```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=sk-ant-your-key-here

python -m source_code.main
```

The pipeline discovers images in `Sample_images/`, sends each to Claude Vision, normalises the results, and writes CSV to both `output/` and `sample_output/`.

CLI options:
```bash
python -m source_code.main --images-dir path/to/images --output-dir path/to/output
```

### Option 2: Without API Key (pre-extracted data)

The sample output was generated using Claude Code's built-in vision capabilities to read all 13 images. The `generate_output.py` script contains the pre-extracted data and runs it through the normalisation + CSV pipeline — no API key required.

```bash
python generate_output.py
```

This writes the same CSV to `output/` and `sample_output/`. Useful for reviewing the normalisation logic and output format without spending API credits.

### Running Tests

```bash
python -m pytest source_code/test_normalizer.py -v
```

26 tests covering name resolution, unit standardisation, parenthetical stripping, German terms, and the full normalisation pipeline. All pure-function tests — no API calls or mocking.

---

## What I'd Do Next

**Confidence scores per extraction.** Claude could return a confidence estimate for each nutrient. Low-confidence extractions get flagged for human review — useful for catching hallucinations or misreads.

**Async API calls.** Process images in parallel with `asyncio` and `httpx`, with a semaphore to respect rate limits. At 100+ images, sequential processing becomes the bottleneck.

**Value range validation.** Flag physiologically implausible values (e.g., "200,000 mg Vitamin C") as likely parse errors. A simple min/max range per nutrient catches gross mistakes.

**Cross-product deduplication.** Products 01 and 10 are the same supplement. At scale, you'd want to group images by product (using brand name, ingredient fingerprint, or image similarity) and merge their data.

**Multi-image product correlation.** A front image (product_08) and back image (product_07) belong to the same product. Correlating them would produce a more complete product record.

**Unit conversion layer.** Convert all values to a common base unit per nutrient (e.g., all Vitamin E to mg alpha-tocopherol equivalents) for cross-product comparison. This requires nutrient-specific conversion tables and chemical form assumptions — significant effort but high value for analytics.
