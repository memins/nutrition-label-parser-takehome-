"""Canonical nutrient-name and unit mappings.

This module is pure data — no logic, no IO.  Every key is lowercase;
every value is snake_case.  The maps are consumed by normalizer.py.
"""

# ---------------------------------------------------------------------------
# NUTRIENT_NAME_MAP
# Maps lowercase raw label text -> canonical snake_case name.
# Organised by category so reviewers can scan quickly.
# ---------------------------------------------------------------------------

NUTRIENT_NAME_MAP: dict[str, str] = {
    # ── Energy ────────────────────────────────────────────────────────────
    "calories": "energy_kcal",
    "calorie": "energy_kcal",
    "energy": "energy_kcal",
    "energy (kcal)": "energy_kcal",
    "energy kcal": "energy_kcal",
    "kcal": "energy_kcal",
    "total calories": "energy_kcal",
    "calories (kcal)": "energy_kcal",
    "energy (kj)": "energy_kj",
    "energy kj": "energy_kj",
    "kilojoules": "energy_kj",
    "kj": "energy_kj",

    # ── Macronutrients — Fat ──────────────────────────────────────────────
    "total fat": "total_fat",
    "fat": "total_fat",
    "total lipid": "total_fat",
    "saturated fat": "saturated_fat",
    "saturated": "saturated_fat",
    "of which saturates": "saturated_fat",
    "saturates": "saturated_fat",
    "trans fat": "trans_fat",
    "trans": "trans_fat",
    "trans-fat": "trans_fat",
    "monounsaturated fat": "monounsaturated_fat",
    "monounsaturated": "monounsaturated_fat",
    "monounsaturates": "monounsaturated_fat",
    "of which monounsaturates": "monounsaturated_fat",
    "polyunsaturated fat": "polyunsaturated_fat",
    "polyunsaturated": "polyunsaturated_fat",
    "polyunsaturates": "polyunsaturated_fat",
    "of which polyunsaturates": "polyunsaturated_fat",
    "cholesterol": "cholesterol",

    # ── Macronutrients — Carbohydrate ─────────────────────────────────────
    "total carbohydrate": "total_carbohydrate",
    "total carbohydrates": "total_carbohydrate",
    "carbohydrate": "total_carbohydrate",
    "carbohydrates": "total_carbohydrate",
    "total carbs": "total_carbohydrate",
    "carbs": "total_carbohydrate",
    "dietary fiber": "dietary_fiber",
    "dietary fibre": "dietary_fiber",
    "fiber": "dietary_fiber",
    "fibre": "dietary_fiber",
    "soluble fiber": "soluble_fiber",
    "insoluble fiber": "insoluble_fiber",
    "total sugars": "total_sugars",
    "sugars": "total_sugars",
    "sugar": "total_sugars",
    "of which sugars": "total_sugars",
    "added sugars": "added_sugars",
    "includes added sugars": "added_sugars",
    "sugar alcohols": "sugar_alcohols",

    # ── Macronutrients — Protein & Sodium ─────────────────────────────────
    "protein": "protein",
    "proteins": "protein",
    "sodium": "sodium",
    "salt": "salt",

    # ── Vitamins — Fat-soluble ────────────────────────────────────────────
    "vitamin a": "vitamin_a",
    "vitamin d": "vitamin_d",
    "vitamin d3": "vitamin_d",
    "cholecalciferol": "vitamin_d",
    "vitamin e": "vitamin_e",
    "tocopherol": "vitamin_e",
    "alpha-tocopherol": "vitamin_e",
    "vitamin k": "vitamin_k",
    "vitamin k1": "vitamin_k",
    "vitamin k2": "vitamin_k2",

    # ── Vitamins — Water-soluble ──────────────────────────────────────────
    "vitamin c": "vitamin_c",
    "ascorbic acid": "vitamin_c",

    "vitamin b1": "thiamine",
    "thiamine": "thiamine",
    "thiamin": "thiamine",
    "thiamine mononitrate": "thiamine",

    "vitamin b2": "riboflavin",
    "riboflavin": "riboflavin",

    "vitamin b3": "niacin",
    "niacin": "niacin",
    "niacinamide": "niacin",
    "nicotinic acid": "niacin",

    "vitamin b5": "pantothenic_acid",
    "pantothenic acid": "pantothenic_acid",

    "vitamin b6": "vitamin_b6",
    "pyridoxine": "vitamin_b6",
    "pyridoxine hcl": "vitamin_b6",
    "pyridoxine hydrochloride": "vitamin_b6",

    "vitamin b7": "biotin",
    "biotin": "biotin",

    "vitamin b9": "folate",
    "folate": "folate",
    "folic acid": "folate",

    "vitamin b12": "vitamin_b12",
    "cobalamin": "vitamin_b12",
    "cyanocobalamin": "vitamin_b12",
    "methylcobalamin": "vitamin_b12",

    "choline": "choline",

    # ── Minerals ──────────────────────────────────────────────────────────
    "calcium": "calcium",
    "iron": "iron",
    "zinc": "zinc",
    "selenium": "selenium",
    "magnesium": "magnesium",
    "phosphorus": "phosphorus",
    "phosphorous": "phosphorus",
    "potassium": "potassium",
    "manganese": "manganese",
    "copper": "copper",
    "chromium": "chromium",
    "molybdenum": "molybdenum",
    "iodine": "iodine",
    "chloride": "chloride",
    "fluoride": "fluoride",

    # ── Omega fatty acids ─────────────────────────────────────────────────
    "omega-3": "omega_3",
    "omega 3": "omega_3",
    "omega-3 fatty acids": "omega_3",
    "total omega-3": "omega_3",
    "epa": "epa",
    "eicosapentaenoic acid": "epa",
    "dha": "dha",
    "docosahexaenoic acid": "dha",
    "ala": "ala",
    "alpha-linolenic acid": "ala",
    "omega-6": "omega_6",
    "omega 6": "omega_6",
    "omega-6 fatty acids": "omega_6",

    # ── Herbal / proprietary (from supplement labels in image set) ────────
    "ashwagandha": "ashwagandha",
    "ashwagandha extract": "ashwagandha",
    "shiitake": "shiitake",
    "shiitake mushroom": "shiitake",
    "reishi": "reishi",
    "reishi mushroom": "reishi",
    "lion's mane": "lions_mane",
    "lions mane": "lions_mane",
    "lion's mane mushroom": "lions_mane",
    "chaga": "chaga",
    "chaga mushroom": "chaga",
    "cordyceps": "cordyceps",
    "cordyceps mushroom": "cordyceps",
    "turkey tail": "turkey_tail",
    "turkey tail mushroom": "turkey_tail",
    "maitake": "maitake",
    "maitake mushroom": "maitake",

    # ── Common German nutrition-label terms ───────────────────────────────
    "brennwert": "energy_kcal",
    "energie": "energy_kcal",
    "fett": "total_fat",
    "davon gesättigte fettsäuren": "saturated_fat",
    "gesättigte fettsäuren": "saturated_fat",
    "gesattigte fettsauren": "saturated_fat",
    "kohlenhydrate": "total_carbohydrate",
    "davon zucker": "total_sugars",
    "zucker": "total_sugars",
    "eiweiß": "protein",
    "eiweiss": "protein",
    "ballaststoffe": "dietary_fiber",
    "salz": "salt",
    "fischöl": "fish_oil",
    "fischoel": "fish_oil",
    "omega-3-fettsäuren": "omega_3",
    "fettsäuren": "fatty_acids",
}


# ---------------------------------------------------------------------------
# UNIT_MAP
# Maps lowercase long-form or variant unit strings -> standard abbreviation.
# ---------------------------------------------------------------------------

UNIT_MAP: dict[str, str] = {
    # Mass
    "milligrams": "mg",
    "milligram": "mg",
    "mg": "mg",
    "grams": "g",
    "gram": "g",
    "g": "g",
    "micrograms": "ug",
    "microgram": "ug",
    "mcg": "ug",
    "µg": "ug",
    "ug": "ug",

    # Energy
    "kilocalories": "kcal",
    "kilocalorie": "kcal",
    "kcal": "kcal",
    "cal": "kcal",
    "kilojoules": "kJ",
    "kilojoule": "kJ",
    "kj": "kJ",

    # International units
    "iu": "IU",
    "international units": "IU",
    "international unit": "IU",

    # Volume (liquid supplements)
    "milliliters": "mL",
    "milliliter": "mL",
    "ml": "mL",
    "liters": "L",
    "liter": "L",
    "l": "L",
    "fl oz": "fl oz",

    # Percent
    "%": "%",
    "percent": "%",

    # Dietary folate equivalents / retinol activity equivalents
    "mcg dfe": "ug DFE",
    "µg dfe": "ug DFE",
    "mcg rae": "ug RAE",
    "µg rae": "ug RAE",

    # Colony-forming units (probiotics)
    "cfu": "CFU",
    "billion cfu": "billion CFU",
}
