"""Convert normalized nutrient data to CSV output."""

import pandas as pd
from pathlib import Path

from .models import NormalizedNutrient

# Column order for the output CSV.
_COLUMN_ORDER = [
    "product_image",
    "nutrient_name_raw",
    "nutrient_name_standard",
    "amount",
    "unit",
    "percent_reference",
    "parent_nutrient",
    "serving_size",
]


def write_csv(nutrients: list[NormalizedNutrient], output_path: Path) -> None:
    """Write a list of NormalizedNutrient objects to a CSV file.

    The rows are sorted by product_image while preserving the original
    extraction order of nutrients within each product.  Parent directories
    are created automatically if they don't exist.
    """
    rows = [n.model_dump() for n in nutrients]
    df = pd.DataFrame(rows, columns=_COLUMN_ORDER)

    # Stable sort by product_image — kind="mergesort" preserves the
    # within-group order so nutrients stay in their extraction sequence.
    df = df.sort_values(by="product_image", kind="mergesort").reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
