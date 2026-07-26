from __future__ import annotations

import streamlit as st

from config import DEFAULT_GEMINI_MODEL, ENV_GEMINI_API_KEY, MAX_PDF_SIZE_MB
from core.gemini_client import (
    MODEL_OPTIONS,
    GeminiAnalysisError,
    analyze_screenplay,
)
from core.pdf_utils import (
    PDFValidationError,
    extract_text_preview,
    file_sha256,
    get_page_count,
    validate_pdf,
)
from core.storage import save_analysis
from core.ui import hero


hero(
    "Upload and analyse a screenplay",
    "The PDF is sent to Gemini for native document understanding and returned as validated structured data.",
)

with st.expander("API key and privacy", expanded=True):
    st.write(
        "Use a Gemini API key from Google AI Studio. The key is kept only in the current Streamlit session "
        "unless you place it in `.env` or Streamlit Secrets. Uploaded PDFs are not saved by this app, but "
        "the PDF content is sent to the Gemini API for analysis."
    )
    try:
        secret_key = str(st.secrets.get("GEMINI_API_KEY", ""))
    except Exception:
        secret_key = ""
    default_key = st.session_state.get("api_key") or ENV_GEMINI_API_KEY or secret_key
    api_key = st.text_input(
        "Gemini API key",
        value=default_key,
        type="password",
        placeholder="AIza...",
        help="For deployment, add GEMINI_API_KEY to Streamlit Secrets instead of hard-coding it.",
    )
    st.session_state.api_key = api_key

settings_col, upload_col = st.columns([0.8, 1.2])
with settings_col:
    st.subheader("Analysis settings")
    default_index = MODEL_OPTIONS.index(DEFAULT_GEMINI_MODEL) if DEFAULT_GEMINI_MODEL in MODEL_OPTIONS else 0
    model = st.selectbox(
        "Gemini model",
        MODEL_OPTIONS,
        index=default_index,
        help="Gemini 3.6 Flash is the recommended balance of quality, speed, and multimodal support.",
    )
    allow_fallback = st.checkbox(
        "Try fallback models when the selected model is unavailable",
        value=True,
    )
    save_locally = st.checkbox(
        "Save the completed analysis in the local project database",
        value=True,
        help="Local Streamlit Cloud storage can be temporary. Use an external database for production.",
    )
    st.caption(f"Maximum supported PDF size in this project: {MAX_PDF_SIZE_MB} MB.")

with upload_col:
    st.subheader("Screenplay PDF")
    uploaded_file = st.file_uploader(
        "Choose a PDF screenplay",
        type=["pdf"],
        help="Scanned PDFs are supported because Gemini can inspect pages visually.",
    )

if uploaded_file is not None:
    pdf_bytes = uploaded_file.getvalue()
    try:
        validate_pdf(pdf_bytes, uploaded_file.name, MAX_PDF_SIZE_MB)
        page_count = get_page_count(pdf_bytes)
    except PDFValidationError as exc:
        st.error(str(exc))
        st.stop()

    st.session_state.pdf_bytes = pdf_bytes
    st.session_state.pdf_filename = uploaded_file.name
    st.session_state.pdf_hash = file_sha256(pdf_bytes)

    file_col, page_col, size_col = st.columns(3)
    file_col.metric("File", uploaded_file.name)
    page_col.metric("Pages", page_count)
    size_col.metric("Size", f"{len(pdf_bytes) / (1024 * 1024):.2f} MB")

    preview_tab, text_tab = st.tabs(["PDF preview", "Extracted text preview"])
    with preview_tab:
        try:
            st.pdf(pdf_bytes, height=650)
        except Exception:
            st.info("PDF preview is unavailable in this environment, but analysis can still continue.")
    with text_tab:
        st.text_area(
            "First pages",
            extract_text_preview(pdf_bytes),
            height=350,
            disabled=True,
            label_visibility="collapsed",
        )

    analyse = st.button(
        "Analyse screenplay",
        type="primary",
        icon=":material/auto_awesome:",
        use_container_width=True,
    )

    if analyse:
        if not api_key.strip():
            st.error("Enter a Gemini API key before starting the analysis.")
            st.stop()

        progress = st.progress(0, text="Preparing screenplay...")
        status_box = st.empty()

        def update_status(message: str) -> None:
            status_box.info(message)
            progress.progress(35, text=message)

        try:
            progress.progress(10, text="Validating PDF...")
            result = analyze_screenplay(
                pdf_bytes=pdf_bytes,
                api_key=api_key,
                selected_model=model,
                page_count=page_count,
                allow_fallback=allow_fallback,
                progress_callback=update_status,
            )
            progress.progress(85, text="Validating structured analysis...")
            st.session_state.analysis_report = result.report
            st.session_state.raw_analysis_json = result.raw_json
            st.session_state.model_used = result.model_used
            st.session_state.analysis_saved_id = None

            if save_locally:
                analysis_id = save_analysis(
                    report=result.report,
                    filename=uploaded_file.name,
                    file_hash=st.session_state.pdf_hash,
                    model_used=result.model_used,
                )
                st.session_state.analysis_saved_id = analysis_id

            progress.progress(100, text="Analysis complete")
            status_box.success(
                f"Analysis completed with {result.model_used}. "
                f"Detected {len(result.report.characters)} characters and {len(result.report.scenes)} scenes."
            )
            st.page_link("pages/overview.py", label="Open screenplay overview", icon=":material/arrow_forward:")
        except GeminiAnalysisError as exc:
            progress.empty()
            status_box.empty()
            st.error(str(exc))
        except Exception as exc:
            progress.empty()
            status_box.empty()
            st.exception(exc)
else:
    st.info("Upload a PDF to preview it and begin the analysis.")
