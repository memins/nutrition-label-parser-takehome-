"""Nutrient-name matching and unit standardization.

Pure functions — no IO, no API calls.  Takes an ExtractionResult produced by
the extractor and returns a flat list of NormalizedNutrient objects with
canonical names and standardised units.
"""

from __future__ import annotations

import re

from .models import ExtractionResult, NormalizedNutrient, RawNutrient
from .nutrient_map import NUTRIENT_NAME_MAP, UNIT_MAP


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_PARENS_RE = re.compile(r"\s*\(.*?\)")
_SNAKE_RE = re.compile(r"[^a-z0-9]+")


def _to_snake_case(text: str) -> str:
    """Convert arbitrary text to a snake_case identifier.

    Replaces runs of non-alphanumeric characters with '_' and strips
    leading/trailing underscores.

    >>> _to_snake_case("Vitamin C (Ascorbic Acid)")
    'vitamin_c_ascorbic_acid_'  # (caller strips parens first)
    """
    return _SNAKE_RE.sub("_", text.lower()).strip("_")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def normalize_nutrient_name(raw_name: str) -> str:
    """Map a raw nutrient label string to a canonical snake_case name.

    Resolution order:
    1. Exact lookup (lowercase + stripped).
    2. Strip parenthetical content, retry exact lookup.
    3. Substring match — check whether any map key appears inside the
       cleaned name, or the cleaned name appears inside a map key.
       Prefer the longest matching key to avoid false positives.
    4. Fallback: convert raw name to snake_case as-is so no nutrient is
       silently dropped.
    """
    cleaned = raw_name.lower().strip()

    # 1) Exact lookup.
    if cleaned in NUTRIENT_NAME_MAP:
        return NUTRIENT_NAME_MAP[cleaned]

    # 2) Strip parenthetical content and retry.
    no_parens = _PARENS_RE.sub("", cleaned).strip()
    if no_parens and no_parens in NUTRIENT_NAME_MAP:
        return NUTRIENT_NAME_MAP[no_parens]

    # 3) Substring match (longest key wins to avoid partial false hits).
    #    Only attempt if we have a non-empty string to match against.
    target = no_parens or cleaned
    if target:
        best_key: str | None = None
        for key in NUTRIENT_NAME_MAP:
            if key in target or target in key:
                if best_key is None or len(key) > len(best_key):
                    best_key = key
        if best_key is not None:
            return NUTRIENT_NAME_MAP[best_key]

    # 4) Fallback — never drop a nutrient.
    return _to_snake_case(no_parens or cleaned)


def normalize_unit(raw_unit: str | None) -> str:
    """Standardise a unit string using UNIT_MAP.

    Returns "" for None/empty input.  Unrecognised units are passed through
    as-is (lowercased and stripped).
    """
    if raw_unit is None:
        return ""

    cleaned = raw_unit.lower().strip()
    if not cleaned:
        return ""

    if cleaned in UNIT_MAP:
        return UNIT_MAP[cleaned]

    # Unrecognised — return as-is rather than swallowing information.
    return cleaned


def normalize_nutrients(extraction: ExtractionResult) -> list[NormalizedNutrient]:
    """Transform an ExtractionResult into a flat list of NormalizedNutrient.

    Each RawNutrient is enriched with:
    - a canonical ``nutrient_name_standard``
    - a standardised ``unit``
    - the ``serving_size`` from the parent ExtractionResult

    No nutrient is silently dropped — even unrecognised names get a
    snake_case fallback.
    """
    results: list[NormalizedNutrient] = []

    for raw in extraction.nutrients:
        std_name = normalize_nutrient_name(raw.nutrient_name_raw)
        std_unit = normalize_unit(raw.unit)

        # Disambiguate energy: if the standard name is energy_kcal but the
        # unit is clearly kJ, correct the canonical name.
        if std_name == "energy_kcal" and std_unit == "kJ":
            std_name = "energy_kj"

        results.append(
            NormalizedNutrient(
                product_image=extraction.product_image,
                nutrient_name_raw=raw.nutrient_name_raw,
                nutrient_name_standard=std_name,
                amount=raw.amount,
                unit=std_unit,
                percent_reference=raw.percent_reference,
                parent_nutrient=raw.parent_nutrient,
                serving_size=extraction.serving_size,
            )
        )

    return results
