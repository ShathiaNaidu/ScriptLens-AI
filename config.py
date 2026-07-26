from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "ScriptLens AI"
MAX_PDF_SIZE_MB = 50
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
ENV_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ENV_CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
ENV_CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
