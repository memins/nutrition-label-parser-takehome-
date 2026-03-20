"""CLI entry point — orchestrates the nutrition label parsing pipeline."""

import argparse
import logging
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

from .config import IMAGES_DIR, OUTPUT_DIR, SAMPLE_OUTPUT_DIR, OUTPUT_FILENAME, SUPPORTED_EXTENSIONS
from .extractor import extract_nutrition
from .normalizer import normalize_nutrients
from .csv_writer import write_csv

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the nutrition-label parsing pipeline."""
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    # ---- CLI arguments -------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Extract nutrition data from product label images."
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=IMAGES_DIR,
        help=f"Directory containing label images (default: {IMAGES_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Directory for CSV output (default: {OUTPUT_DIR})",
    )
    args = parser.parse_args()

    images_dir: Path = args.images_dir
    output_dir: Path = args.output_dir

    # ---- Discover images -----------------------------------------------------
    if not images_dir.is_dir():
        logger.error("Images directory does not exist: %s", images_dir)
        sys.exit(1)

    image_paths = sorted(
        path for path in images_dir.iterdir()
        if path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not image_paths:
        logger.warning("No supported images found in %s", images_dir)
        sys.exit(0)

    logger.info("Found %d image(s) in %s", len(image_paths), images_dir)

    # ---- Process each image --------------------------------------------------
    all_nutrients = []
    images_with_data = 0

    for image_path in image_paths:
        logger.info("Processing %s …", image_path.name)
        extraction = extract_nutrition(image_path)

        if extraction.has_nutrition_data:
            images_with_data += 1
            logger.info(
                "  ✓ %s — %d nutrient(s), product: %s",
                image_path.name,
                len(extraction.nutrients),
                extraction.product_name or "(unknown)",
            )
            normalized = normalize_nutrients(extraction)
            all_nutrients.extend(normalized)
        else:
            logger.info("  ✗ %s — no nutrition data found", image_path.name)

    # ---- Write CSV output ----------------------------------------------------
    output_path = output_dir / OUTPUT_FILENAME
    write_csv(all_nutrients, output_path)
    logger.info("CSV written to %s (%d rows)", output_path, len(all_nutrients))

    # Copy to sample_output/ as well.
    SAMPLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sample_path = SAMPLE_OUTPUT_DIR / OUTPUT_FILENAME
    shutil.copy2(output_path, sample_path)
    logger.info("Copy saved to %s", sample_path)

    # ---- Summary -------------------------------------------------------------
    print(
        f"\nDone — {len(image_paths)} image(s) processed, "
        f"{images_with_data} with nutrition data, "
        f"{len(all_nutrients)} total nutrient(s) extracted."
    )


if __name__ == "__main__":
    main()
