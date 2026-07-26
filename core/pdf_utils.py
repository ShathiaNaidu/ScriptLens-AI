from __future__ import annotations

import hashlib
from io import BytesIO

from pypdf import PdfReader


class PDFValidationError(ValueError):
    pass


def validate_pdf(pdf_bytes: bytes, filename: str, max_size_mb: int = 50) -> None:
    if not filename.lower().endswith(".pdf"):
        raise PDFValidationError("Only PDF screenplay files are supported.")
    if not pdf_bytes:
        raise PDFValidationError("The uploaded PDF is empty.")
    if len(pdf_bytes) > max_size_mb * 1024 * 1024:
        raise PDFValidationError(f"The PDF exceeds the {max_size_mb} MB limit.")
    if not pdf_bytes.startswith(b"%PDF"):
        raise PDFValidationError("The uploaded file does not appear to be a valid PDF.")
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        if len(reader.pages) == 0:
            raise PDFValidationError("The PDF contains no readable pages.")
        if reader.is_encrypted:
            try:
                unlocked = reader.decrypt("")
            except Exception as exc:  # pragma: no cover - library-specific
                raise PDFValidationError("Password-protected PDFs are not supported.") from exc
            if unlocked == 0:
                raise PDFValidationError("Password-protected PDFs are not supported.")
    except PDFValidationError:
        raise
    except Exception as exc:
        raise PDFValidationError("The PDF could not be opened. It may be damaged or encrypted.") from exc


def get_page_count(pdf_bytes: bytes) -> int:
    reader = PdfReader(BytesIO(pdf_bytes))
    return len(reader.pages)


def extract_text_preview(pdf_bytes: bytes, max_pages: int = 4, max_chars: int = 8000) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    text_parts: list[str] = []
    for page in reader.pages[:max_pages]:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            text_parts.append("")
    text = "\n\n".join(text_parts).strip()
    if not text:
        return "No selectable text was extracted. Gemini can still inspect scanned PDF pages visually."
    if len(text) > max_chars:
        return text[:max_chars].rstrip() + "\n\n[Preview truncated]"
    return text


def file_sha256(pdf_bytes: bytes) -> str:
    return hashlib.sha256(pdf_bytes).hexdigest()
