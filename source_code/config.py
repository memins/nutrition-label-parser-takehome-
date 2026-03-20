from pathlib import Path

# Project root is the parent of the source_code directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Model configuration
MODEL_NAME = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096

# Directory paths (resolved relative to project root)
IMAGES_DIR = PROJECT_ROOT / "Sample_images"
OUTPUT_DIR = PROJECT_ROOT / "output"
SAMPLE_OUTPUT_DIR = PROJECT_ROOT / "sample_output"

# Output configuration
OUTPUT_FILENAME = "nutrition_data.csv"

# Supported image extensions
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
