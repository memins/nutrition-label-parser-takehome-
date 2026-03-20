from pydantic import BaseModel


class RawNutrient(BaseModel):
    nutrient_name_raw: str  # Exactly as on label
    amount: float | None = None  # None if unparseable
    unit: str | None = None
    percent_reference: float | None = None  # %NRV / %DV
    parent_nutrient: str | None = None  # For "of which Saturates" under "Total Fat"


class ExtractionResult(BaseModel):
    product_image: str
    has_nutrition_data: bool
    product_name: str | None = None
    serving_size: str | None = None
    servings_per_container: str | None = None
    nutrients: list[RawNutrient] = []
    extraction_notes: str | None = None
    language_detected: str | None = None


class NormalizedNutrient(BaseModel):
    product_image: str
    nutrient_name_raw: str
    nutrient_name_standard: str
    amount: float | None = None
    unit: str
    percent_reference: float | None = None
    parent_nutrient: str | None = None
    serving_size: str | None = None
