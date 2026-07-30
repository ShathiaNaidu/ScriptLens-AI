from __future__ import annotations

import base64
import json
import time
from dataclasses import dataclass
from typing import Callable, Iterable

from google import genai
from pydantic import ValidationError

from core.models import AnalysisReport
from core.prompts import SCREENPLAY_ANALYSIS_PROMPT


DEFAULT_MODEL = "gemini-3.6-flash"
MODEL_OPTIONS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
]


@dataclass
class AnalysisResult:
    report: AnalysisReport
    model_used: str
    raw_json: str


class GeminiAnalysisError(RuntimeError):
    pass


def _is_retryable(exc: Exception) -> bool:
    text = str(exc).lower()
    retry_markers = (
        "429",
        "resource_exhausted",
        "rate limit",
        "quota",
        "503",
        "unavailable",
        "deadline",
        "timeout",
        "temporarily",
    )
    return any(marker in text for marker in retry_markers)


def _friendly_error(exc: Exception) -> str:
    message = str(exc)
    lower = message.lower()
    if "api key" in lower or "unauthenticated" in lower or "401" in lower:
        return "The Gemini API key is missing or invalid. Create a key in Google AI Studio and try again."
    if "429" in lower or "resource_exhausted" in lower or "quota" in lower or "rate limit" in lower:
        return (
            "The Gemini project reached a quota or rate limit. Try a lower-cost model, "
            "wait for the quota window to reset, or use a Gemini project with billing enabled."
        )
    if "schema" in lower and ("invalid" in lower or "complex" in lower or "unsupported" in lower):
        return "Gemini rejected the structured analysis schema. Update google-genai and try the default model."
    if "pdf" in lower and ("invalid" in lower or "unsupported" in lower):
        return "Gemini could not read this PDF. Check that it is not encrypted or damaged."
    return f"Gemini could not complete the screenplay analysis: {message}"


def _candidate_models(selected_model: str, allow_fallback: bool) -> Iterable[str]:
    yield selected_model
    if allow_fallback:
        for model in MODEL_OPTIONS:
            if model != selected_model:
                yield model


def analyze_screenplay(
    pdf_bytes: bytes,
    api_key: str,
    selected_model: str = DEFAULT_MODEL,
    page_count: int | None = None,
    allow_fallback: bool = True,
    progress_callback: Callable[[str], None] | None = None,
    max_attempts_per_model: int = 2,
) -> AnalysisResult:
    if not api_key.strip():
        raise GeminiAnalysisError("A Gemini API key is required.")

    document_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    schema = AnalysisReport.model_json_schema()
    last_error: Exception | None = None

    for model in _candidate_models(selected_model, allow_fallback):
        if progress_callback:
            progress_callback(f"Reading the screenplay with {model}...")

        for attempt in range(1, max_attempts_per_model + 1):
            try:
                client = genai.Client(api_key=api_key.strip())
                interaction = client.interactions.create(
                    model=model,
                    input=[
                        {
                            "type": "document",
                            "data": document_b64,
                            "mime_type": "application/pdf",
                        },
                        {"type": "text", "text": SCREENPLAY_ANALYSIS_PROMPT},
                    ],
                    response_format={
                        "type": "text",
                        "mime_type": "application/json",
                        "schema": schema,
                    },
                )
                raw_json = interaction.output_text
                if not raw_json or not raw_json.strip():
                    raise GeminiAnalysisError("Gemini returned an empty analysis.")

                # Parsing once with json gives clearer messages for malformed output.
                json.loads(raw_json)
                report = AnalysisReport.model_validate_json(raw_json)
                if page_count is not None:
                    report.metadata.page_count = page_count
                report.metadata.scene_count = len(report.scenes) or report.metadata.scene_count
                return AnalysisResult(report=report, model_used=model, raw_json=raw_json)

            except (ValidationError, json.JSONDecodeError) as exc:
                last_error = exc
                # A schema-compliant call should not normally need a retry, but a second
                # attempt can recover from transient truncation.
                if attempt < max_attempts_per_model:
                    time.sleep(2)
                    continue
                break
            except Exception as exc:  # SDK exception types can change between releases.
                last_error = exc
                if _is_retryable(exc) and attempt < max_attempts_per_model:
                    time.sleep(2 ** attempt)
                    continue
                break

    if last_error is None:
        raise GeminiAnalysisError("Gemini did not return an analysis.")
    raise GeminiAnalysisError(_friendly_error(last_error)) from last_error
