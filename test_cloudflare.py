"""Small credential test for ScriptLens AI's Cloudflare Workers AI integration."""

from __future__ import annotations

from pathlib import Path

from config import ENV_CLOUDFLARE_ACCOUNT_ID, ENV_CLOUDFLARE_API_TOKEN
from core.image_generator import ImageGenerationError, generate_concept_art


def main() -> None:
    if not ENV_CLOUDFLARE_ACCOUNT_ID or not ENV_CLOUDFLARE_API_TOKEN:
        raise SystemExit(
            "Add CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN to the .env file first."
        )

    print("Generating a Cloudflare FLUX test image...")
    try:
        image = generate_concept_art(
            prompt=(
                "Cinematic storyboard concept art of an empty university auditorium at sunset, "
                "wide shot, warm window light, mysterious atmosphere"
            ),
            account_id=ENV_CLOUDFLARE_ACCOUNT_ID,
            api_token=ENV_CLOUDFLARE_API_TOKEN,
            aspect_ratio="16:9",
            steps=4,
        )
    except ImageGenerationError as exc:
        raise SystemExit(f"Cloudflare test failed: {exc}") from exc

    output = Path("cloudflare_test.jpg")
    output.write_bytes(image.data)
    print(f"Success. Image saved to: {output.resolve()}")


if __name__ == "__main__":
    main()
