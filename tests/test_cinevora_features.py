from __future__ import annotations

from core.script_tools import export_docx, export_fdx, export_pdf, normalize_screenplay, read_script_file


SAMPLE = """FADE IN:\n\nINT. AUDITORIUM - NIGHT\n\nKARTHIK\nI heard something.\n\nVIJAY\n(quietly)\nStay behind me.\n\nCUT TO:\n"""


def test_screenplay_formatter_and_exports() -> None:
    cleaned = normalize_screenplay(SAMPLE)
    assert "INT. AUDITORIUM - NIGHT" in cleaned
    assert "KARTHIK" in cleaned
    assert len(export_docx(cleaned, "Test")) > 500
    assert len(export_pdf(cleaned, "Test")) > 500


def test_fdx_roundtrip() -> None:
    payload = export_fdx(SAMPLE, "Test")
    assert b"FinalDraft" in payload
    imported = read_script_file("test.fdx", payload)
    assert "INT. AUDITORIUM - NIGHT" in imported
    assert "KARTHIK" in imported
