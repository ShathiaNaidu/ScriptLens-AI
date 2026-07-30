from __future__ import annotations

import streamlit as st

from core.report_generator import (
    generate_docx,
    generate_json,
    generate_pdf,
    report_basename,
)
from core.ui import hero, require_report


report = require_report()
hero(
    "Download the final screenplay report",
    "Export the complete analysis as editable Word, presentation-ready PDF, or machine-readable JSON.",
)

basename = report_basename(report)

with st.spinner("Building report files..."):
    try:
        json_bytes = generate_json(report)
        docx_bytes = generate_docx(report)
        pdf_bytes = generate_pdf(report)
    except Exception as exc:
        st.error(f"The report files could not be generated: {exc}")
        st.stop()

st.success(
    f"Report ready for {report.metadata.title}. Overall score: {report.scores.overall_score}/100."
)

json_col, docx_col, pdf_col = st.columns(3)
with json_col:
    st.download_button(
        "Download JSON",
        data=json_bytes,
        file_name=f"{basename}.json",
        mime="application/json",
        icon=":material/data_object:",
        use_container_width=True,
    )
    st.caption("Best for databases, APIs, and future app features.")
with docx_col:
    st.download_button(
        "Download editable DOCX",
        data=docx_bytes,
        file_name=f"{basename}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        icon=":material/description:",
        use_container_width=True,
    )
    st.caption("Best for editing, lecturer review, and producer notes.")
with pdf_col:
    st.download_button(
        "Download PDF",
        data=pdf_bytes,
        file_name=f"{basename}.pdf",
        mime="application/pdf",
        icon=":material/picture_as_pdf:",
        use_container_width=True,
    )
    st.caption("Best for sharing a fixed professional report.")

st.markdown("---")
st.subheader("Report contents")
st.markdown(
    """
    - Executive summary and overall score
    - Screenplay metadata, themes, logline, and central conflict
    - Character database and character arcs
    - Act and story-structure analysis
    - Scene-by-scene development notes
    - Dialogue and genre analysis
    - Originality disclaimer and local identity opportunities
    - Audience prediction and target market
    - Step 13 storyboard panels with camera, shot, blocking, lighting, mood, and concept-art prompts
    - Step 14 professional pitch package, poster concept, investor deck outline, and final AI scorecard
    - Producer pitch, selling points, and production considerations
    - App target market and analysis limitations
    """
)
