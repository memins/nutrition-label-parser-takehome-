"""Tests for the normalizer module — pure functions, no IO or mocking."""

import pytest

from source_code.normalizer import normalize_nutrient_name, normalize_unit, normalize_nutrients
from source_code.models import ExtractionResult, RawNutrient


# ---------------------------------------------------------------------------
# 1. Known exact names map correctly
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw, expected", [
    ("Vitamin C", "vitamin_c"),
    ("Ascorbic Acid", "vitamin_c"),
    ("Thiamine Mononitrate", "thiamine"),
    ("Total Fat", "total_fat"),
    ("Folate", "folate"),
])
def test_known_exact_names(raw: str, expected: str) -> None:
    assert normalize_nutrient_name(raw) == expected


# ---------------------------------------------------------------------------
# 2. Unknown names pass through as snake_case
# ---------------------------------------------------------------------------

def test_unknown_name_becomes_snake_case() -> None:
    assert normalize_nutrient_name("Some Unknown Nutrient") == "some_unknown_nutrient"


# ---------------------------------------------------------------------------
# 3. Parenthetical stripping works
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw, expected", [
    ("Vitamin C (Ascorbic Acid)", "vitamin_c"),
    ("Folate (as Folic Acid)", "folate"),
    ("Vitamin D (Cholecalciferol)", "vitamin_d"),
])
def test_parenthetical_stripping(raw: str, expected: str) -> None:
    assert normalize_nutrient_name(raw) == expected


# ---------------------------------------------------------------------------
# 4. Case insensitivity
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw", [
    "VITAMIN A",
    "vitamin a",
    "Vitamin A",
    "  Vitamin A  ",
])
def test_case_insensitivity(raw: str) -> None:
    assert normalize_nutrient_name(raw) == "vitamin_a"


# ---------------------------------------------------------------------------
# 5. German terms
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw, expected", [
    ("Kohlenhydrate", "total_carbohydrate"),
    ("Eiweiß", "protein"),
    ("Brennwert", "energy_kcal"),
    ("Ballaststoffe", "dietary_fiber"),
])
def test_german_terms(raw: str, expected: str) -> None:
    assert normalize_nutrient_name(raw) == expected


# ---------------------------------------------------------------------------
# 6. Unit normalization
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw_unit, expected", [
    ("milligrams", "mg"),
    ("mcg", "ug"),
    ("µg", "ug"),
    (None, ""),
    ("", ""),
    ("g", "g"),
    ("iu", "IU"),
])
def test_unit_normalization(raw_unit: str | None, expected: str) -> None:
    assert normalize_unit(raw_unit) == expected


# ---------------------------------------------------------------------------
# 7. Substring match works
# ---------------------------------------------------------------------------

def test_substring_match() -> None:
    # "total omega-3 fatty acids" is in the map; a name like
    # "omega-3 fatty acids from fish oil" contains the key "omega-3 fatty acids"
    result = normalize_nutrient_name("omega-3 fatty acids from fish oil")
    assert result == "omega_3"


# ---------------------------------------------------------------------------
# 8. Full normalize_nutrients pipeline
# ---------------------------------------------------------------------------

def test_normalize_nutrients_pipeline() -> None:
    extraction = ExtractionResult(
        product_image="test.jpg",
        has_nutrition_data=True,
        serving_size="1 tablet",
        nutrients=[
            RawNutrient(
                nutrient_name_raw="Vitamin C",
                amount=90.0,
                unit="mg",
                percent_reference=100.0,
            ),
            RawNutrient(
                nutrient_name_raw="Protein",
                amount=25.0,
                unit="grams",
                percent_reference=None,
                parent_nutrient=None,
            ),
            RawNutrient(
                nutrient_name_raw="Kohlenhydrate",
                amount=30.0,
                unit="g",
                percent_reference=None,
            ),
        ],
    )

    results = normalize_nutrients(extraction)

    assert len(results) == 3

    # First nutrient: Vitamin C
    assert results[0].product_image == "test.jpg"
    assert results[0].nutrient_name_raw == "Vitamin C"
    assert results[0].nutrient_name_standard == "vitamin_c"
    assert results[0].amount == 90.0
    assert results[0].unit == "mg"
    assert results[0].percent_reference == 100.0
    assert results[0].serving_size == "1 tablet"

    # Second nutrient: Protein with long-form unit
    assert results[1].nutrient_name_standard == "protein"
    assert results[1].unit == "g"
    assert results[1].amount == 25.0

    # Third nutrient: German term
    assert results[2].nutrient_name_standard == "total_carbohydrate"
    assert results[2].unit == "g"
    assert results[2].amount == 30.0
