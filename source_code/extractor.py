"""Claude Vision API integration for nutrition label extraction."""

import anthropic
import base64
import json
import logging
import time
from pathlib import Path

from .config import MODEL_NAME, MAX_TOKENS
from .models import ExtractionResult
from .prompts import EXTRACTION_PROMPT

logger = logging.getLogger(__name__)

# Map file extensions to MIME types for the Claude Vision API.
_MEDIA_TYPES: dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def _encode_image(image_path: Path) -> tuple[str, str]:
    """Read an image file and return its base64 encoding and media type.

    Raises:
        ValueError: If the file extension is not a supported image format.
        FileNotFoundError: If the image file does not exist.
    """
    suffix = image_path.suffix.lower()
    media_type = _MEDIA_TYPES.get(suffix)
    if media_type is None:
        raise ValueError(
            f"Unsupported image format '{suffix}'. "
            f"Supported: {', '.join(_MEDIA_TYPES)}"
        )

    image_bytes = image_path.read_bytes()
    b64_data = base64.standard_b64encode(image_bytes).decode("utf-8")
    return b64_data, media_type


def _parse_response(raw_text: str, image_filename: str) -> ExtractionResult:
    """Parse the Claude API response text into an ExtractionResult.

    If the response is not valid JSON, returns a fallback ExtractionResult with
    has_nutrition_data=False and the parse error noted in extraction_notes.
    """
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        logger.error(
            "Malformed JSON from API for '%s': %s\nRaw response:\n%s",
            image_filename,
            exc,
            raw_text,
        )
        return ExtractionResult(
            product_image=image_filename,
            has_nutrition_data=False,
            extraction_notes=f"JSON parse failure: {exc}",
        )

    # Ensure the product_image field matches the actual filename we processed.
    data["product_image"] = image_filename
    return ExtractionResult.model_validate(data)


def extract_nutrition(image_path: Path) -> ExtractionResult:
    """Extract nutrition data from a product label image using Claude Vision.

    Sends the image to the Claude API with a carefully crafted prompt, then
    parses the structured JSON response into an ExtractionResult.

    Includes a single retry with 2-second backoff on transient API errors.

    Args:
        image_path: Path to the image file (.png, .jpg, .jpeg, or .webp).

    Returns:
        An ExtractionResult containing the extracted nutrition data, or a
        result with has_nutrition_data=False if extraction failed.
    """
    image_filename = image_path.name
    b64_data, media_type = _encode_image(image_path)

    # Format the prompt with the actual image filename.
    prompt = EXTRACTION_PROMPT.format(image_filename=image_filename)

    client = anthropic.Anthropic()

    # Build the message payload with an image content block.
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": b64_data,
                    },
                },
                {
                    "type": "text",
                    "text": prompt,
                },
            ],
        }
    ]

    # Attempt the API call with a single retry on transient errors.
    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(
                "Sending '%s' to Claude API (attempt %d/%d)",
                image_filename,
                attempt,
                max_attempts,
            )
            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=MAX_TOKENS,
                messages=messages,
            )
            break  # Success — exit retry loop.
        except anthropic.APIError as exc:
            logger.warning(
                "API error for '%s' (attempt %d/%d): %s",
                image_filename,
                attempt,
                max_attempts,
                exc,
            )
            if attempt < max_attempts:
                time.sleep(2)
            else:
                # Exhausted retries — return a failure result.
                return ExtractionResult(
                    product_image=image_filename,
                    has_nutrition_data=False,
                    extraction_notes=f"API error after {max_attempts} attempts: {exc}",
                )

    # Extract the text content from the API response.
    raw_text = response.content[0].text
    logger.debug("Raw API response for '%s':\n%s", image_filename, raw_text)

    result = _parse_response(raw_text, image_filename)

    # If the model determined there's no nutrition data, ensure nutrients is empty.
    if not result.has_nutrition_data:
        result.nutrients = []

    return result
