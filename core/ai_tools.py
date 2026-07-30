from __future__ import annotations

import time
from typing import Iterable

import streamlit as st
from google import genai
from google.genai import types

from config import DEFAULT_GEMINI_MODEL, ENV_GEMINI_API_KEY
from core.gemini_client import MODEL_OPTIONS


class CinevoraAIError(RuntimeError):
    pass


def get_gemini_api_key() -> str:
    """Resolve a Gemini key from session state, environment, or Streamlit Secrets."""
    session_key = str(st.session_state.get("api_key", "") or "").strip()
    if session_key:
        return session_key
    if ENV_GEMINI_API_KEY.strip():
        return ENV_GEMINI_API_KEY.strip()
    try:
        return str(st.secrets.get("GEMINI_API_KEY", "") or "").strip()
    except Exception:
        return ""


def _candidate_models(selected_model: str | None = None) -> Iterable[str]:
    model = selected_model or DEFAULT_GEMINI_MODEL
    yield model
    for candidate in MODEL_OPTIONS:
        if candidate != model:
            yield candidate


def _friendly_error(exc: Exception) -> str:
    message = str(exc)
    lower = message.lower()
    if "api key" in lower or "401" in lower or "unauthenticated" in lower:
        return "Gemini API authentication failed. Check the Gemini API key in Streamlit Secrets or the Upload page."
    if "429" in lower or "quota" in lower or "rate limit" in lower or "resource_exhausted" in lower:
        return "Gemini reached a quota or rate limit. Try again later or select another available Gemini project/model."
    return f"Gemini could not complete this request: {message}"


def generate_text(
    prompt: str,
    *,
    model: str | None = None,
    temperature: float = 0.7,
    max_attempts_per_model: int = 1,
) -> str:
    api_key = get_gemini_api_key()
    if not api_key:
        raise CinevoraAIError("A Gemini API key is required. Add it on Upload & Analyse or in Streamlit Secrets.")
    if not prompt.strip():
        raise CinevoraAIError("The AI request was empty.")

    last_error: Exception | None = None
    for candidate in _candidate_models(model):
        for attempt in range(max_attempts_per_model):
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model=candidate,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=float(max(0.0, min(temperature, 2.0))),
                    ),
                )
                text = getattr(response, "text", None)
                if not text:
                    # SDK responses may expose parts instead of .text.
                    parts = []
                    for candidate_item in getattr(response, "candidates", []) or []:
                        content = getattr(candidate_item, "content", None)
                        for part in getattr(content, "parts", []) or []:
                            part_text = getattr(part, "text", None)
                            if part_text:
                                parts.append(part_text)
                    text = "\n".join(parts)
                if text and text.strip():
                    return text.strip()
                raise RuntimeError("Gemini returned an empty response.")
            except Exception as exc:
                last_error = exc
                if attempt + 1 < max_attempts_per_model:
                    time.sleep(1.5)
    raise CinevoraAIError(_friendly_error(last_error or RuntimeError("Unknown Gemini error")))


def report_context(report, max_chars: int = 45000) -> str:
    """Compact current analysis into text for downstream feature prompts."""
    raw = report.model_dump_json(indent=2)
    if len(raw) <= max_chars:
        return raw
    # Keep metadata, characters, acts, scenes, scores and pitch when the full JSON is huge.
    compact = {
        "metadata": report.metadata.model_dump(),
        "characters": [item.model_dump() for item in report.characters],
        "acts": [item.model_dump() for item in report.acts],
        "scenes": [item.model_dump() for item in report.scenes],
        "scores": report.scores.model_dump(),
        "main_recommendation": report.main_recommendation,
        "top_strengths": report.top_strengths,
        "priority_improvements": report.priority_improvements,
        "producer_pitch": report.producer_pitch.model_dump(),
    }
    import json
    return json.dumps(compact, ensure_ascii=False, indent=2)[:max_chars]
