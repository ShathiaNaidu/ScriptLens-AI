from __future__ import annotations

import streamlit as st

from core.script_tools import export_docx, export_fdx, export_pdf, normalize_screenplay, read_script_file
from core.ui import hero


hero(
    "Screenplay Writing, Formatting & Script Files",
    "Write inside Cinevora AI, clean the screenplay into a consistent Fountain-friendly format, and import/export common script files.",
)

upload_tab, write_tab, export_tab = st.tabs(["Import", "Write & Format", "Export"])

with upload_tab:
    uploaded = st.file_uploader(
        "Import screenplay",
        type=["pdf", "docx", "txt", "fountain", "fdx", "md"],
        help="PDF text extraction works best on text-based PDFs. Use Upload & Analyse for Gemini's native visual PDF reading.",
    )
    if uploaded:
        try:
            imported = read_script_file(uploaded.name, uploaded.getvalue())
            st.session_state.screenplay_editor = imported
            st.success(f"Imported {uploaded.name} into the writing workspace.")
            st.text_area("Preview", imported[:12000], height=300, disabled=True)
        except Exception as exc:
            st.error(f"Could not import this file: {exc}")

with write_tab:
    title = st.text_input("Working title", value=st.session_state.get("writer_title", "Untitled Screenplay"))
    st.session_state.writer_title = title
    screenplay = st.text_area(
        "Screenplay editor",
        value=st.session_state.get("screenplay_editor", ""),
        height=650,
        placeholder="FADE IN:\n\nINT. UNIVERSITY AUDITORIUM - NIGHT\n\nKARTHIK enters the dark hall...",
    )
    st.session_state.screenplay_editor = screenplay
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Professional format cleanup", type="primary", use_container_width=True, icon=":material/format_align_left:"):
            st.session_state.screenplay_editor = normalize_screenplay(screenplay)
            st.success("Formatting cleanup applied without changing story content.")
            st.rerun()
    with c2:
        if st.button("Clear editor", use_container_width=True):
            st.session_state.screenplay_editor = ""
            st.rerun()
    st.caption(
        "The formatter normalises scene headings, character cues, transitions, spacing, and Fountain-compatible plain text. "
        "It is a writing aid rather than a substitute for a dedicated studio delivery specification."
    )

with export_tab:
    text = st.session_state.get("screenplay_editor", "")
    if not text.strip():
        st.info("Write or import a screenplay first.")
    else:
        safe_title = (st.session_state.get("writer_title") or "cinevora_screenplay").strip().replace(" ", "_")
        st.download_button("Download TXT", text.encode("utf-8"), f"{safe_title}.txt", "text/plain", use_container_width=True)
        st.download_button("Download Fountain", normalize_screenplay(text).encode("utf-8"), f"{safe_title}.fountain", "text/plain", use_container_width=True)
        st.download_button(
            "Download DOCX",
            export_docx(normalize_screenplay(text), st.session_state.get("writer_title", "Cinevora Screenplay")),
            f"{safe_title}.docx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
        st.download_button(
            "Download PDF",
            export_pdf(normalize_screenplay(text), st.session_state.get("writer_title", "Cinevora Screenplay")),
            f"{safe_title}.pdf",
            "application/pdf",
            use_container_width=True,
        )
        st.download_button(
            "Download Final Draft FDX",
            export_fdx(normalize_screenplay(text), st.session_state.get("writer_title", "Cinevora Screenplay")),
            f"{safe_title}.fdx",
            "application/xml",
            use_container_width=True,
        )
