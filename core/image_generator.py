from __future__ import annotations

import base64
import binascii
import random
from dataclasses import dataclass
from typing import Any

import requests


CLOUDFLARE_IMAGE_MODEL = "@cf/black-forest-labs/flux-1-schnell"
IMAGE_MODEL_OPTIONS = [CLOUDFLARE_IMAGE_MODEL]
DEFAULT_IMAGE_MODEL = CLOUDFLARE_IMAGE_MODEL
CLOUDFLARE_API_BASE = "https://api.cloudflare.com/client/v4"


@dataclass
class GeneratedImage:
    data: bytes
    mime_type: str
    model_used: str


class ImageGenerationError(RuntimeError):
    """Raised when Cloudflare Workers AI cannot create an image."""


def _friendly_error(status_code: int | None, message: str) -> str:
    lower = message.lower()

    if status_code in {401, 403} or any(
        phrase in lower
        for phrase in (
            "authentication error",
            "invalid api token",
            "permission denied",
            "not authorized",
            "unauthorized",
            "forbidden",
        )
    ):
        return (
            "Cloudflare authentication failed. Check that the Account ID is correct and that the API token "
            "has Workers AI Read and Edit permissions."
        )

    if status_code == 404 or "not found" in lower:
        return (
            "Cloudflare could not find the account or image model. Check the Account ID and confirm that "
            "Workers AI is enabled for that Cloudflare account."
        )

    if status_code == 429 or any(
        phrase in lower
        for phrase in ("rate limit", "quota", "too many requests", "neurons")
    ):
        return (
            "Cloudflare Workers AI reached its current free usage or rate limit. The storyboard details and "
            "image prompt are still available. Try again after the daily free allocation resets."
        )

    if status_code is not None and status_code >= 500:
        return "Cloudflare Workers AI is temporarily unavailable. Please try the image again shortly."

    clean_message = message.strip() or "Unknown Cloudflare Workers AI error."
    return f"Cloudflare could not generate the concept art: {clean_message}"


def _error_message(payload: Any, fallback: str) -> str:
    if isinstance(payload, dict):
        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            parts: list[str] = []
            for error in errors:
                if isinstance(error, dict):
                    code = error.get("code")
                    message = error.get("message")
                    if code and message:
                        parts.append(f"{code}: {message}")
                    elif message:
                        parts.append(str(message))
                    else:
                        parts.append(str(error))
                else:
                    parts.append(str(error))
            if parts:
                return "; ".join(parts)

        messages = payload.get("messages")
        if isinstance(messages, list) and messages:
            return "; ".join(str(item) for item in messages)

    return fallback


def _decode_image(value: str | bytes) -> bytes:
    if isinstance(value, bytes):
        return value

    encoded = value.strip()
    if encoded.startswith("data:") and "," in encoded:
        encoded = encoded.split(",", 1)[1]

    try:
        return base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ImageGenerationError("Cloudflare returned invalid image data.") from exc


def _normalise_prompt(prompt: str, aspect_ratio: str) -> str:
    cleaned = " ".join(prompt.split())
    composition = {
        "16:9": "Compose as a cinematic widescreen 16:9 storyboard frame.",
        "2:3": "Compose as a vertical 2:3 cinematic poster.",
        "1:1": "Compose as a square 1:1 concept-art image.",
    }.get(aspect_ratio, f"Compose the image for a {aspect_ratio} aspect ratio.")

    combined = f"{cleaned} {composition} No text, no captions, no watermarks."
    return combined[:2048]


def generate_concept_art(
    prompt: str,
    account_id: str,
    api_token: str,
    selected_model: str = DEFAULT_IMAGE_MODEL,
    aspect_ratio: str = "16:9",
    steps: int = 4,
    timeout_seconds: int = 120,
) -> GeneratedImage:
    """Generate concept art with Cloudflare Workers AI FLUX.1 Schnell."""
    account_id = account_id.strip()
    api_token = api_token.strip()
    prompt = prompt.strip()

    if not account_id:
        raise ImageGenerationError("A Cloudflare Account ID is required to generate concept art.")
    if not api_token:
        raise ImageGenerationError("A Cloudflare API token is required to generate concept art.")
    if not prompt:
        raise ImageGenerationError("A concept-art prompt is required.")
    if selected_model not in IMAGE_MODEL_OPTIONS:
        raise ImageGenerationError(f"Unsupported Cloudflare image model: {selected_model}")

    safe_steps = max(1, min(int(steps), 8))
    url = f"{CLOUDFLARE_API_BASE}/accounts/{account_id}/ai/run/{selected_model}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": _normalise_prompt(prompt, aspect_ratio),
        "steps": safe_steps,
        "seed": random.randint(1, 2_147_483_647),
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=timeout_seconds,
        )
    except requests.Timeout as exc:
        raise ImageGenerationError(
            "Cloudflare image generation timed out. Check your internet connection and try again."
        ) from exc
    except requests.RequestException as exc:
        raise ImageGenerationError(
            f"Could not connect to Cloudflare Workers AI: {exc}"
        ) from exc

    try:
        data = response.json()
    except ValueError:
        data = None

    if not response.ok:
        message = _error_message(data, response.text)
        raise ImageGenerationError(_friendly_error(response.status_code, message))

    if not isinstance(data, dict):
        raise ImageGenerationError("Cloudflare returned an unexpected non-JSON response.")

    if data.get("success") is False:
        message = _error_message(data, "Cloudflare reported that image generation failed.")
        raise ImageGenerationError(_friendly_error(response.status_code, message))

    result = data.get("result")
    image_value = result.get("image") if isinstance(result, dict) else None
    if not image_value:
        raise ImageGenerationError("Cloudflare returned no image data.")

    return GeneratedImage(
        data=_decode_image(image_value),
        mime_type="image/jpeg",
        model_used=selected_model,
    )
