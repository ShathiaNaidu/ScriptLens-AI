from __future__ import annotations

import pandas as pd
import streamlit as st

from core.storage import delete_analysis, list_analyses, load_analysis
from core.ui import hero


hero(
    "Saved screenplay projects",
    "Load a previous local analysis without using Gemini again.",
)

records = list_analyses(limit=50)
if not records:
    st.info("No saved analyses were found. Analyse a screenplay and enable local saving first.")
    st.stop()

frame = pd.DataFrame(records)
frame["created_at"] = pd.to_datetime(frame["created_at"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M")
st.dataframe(
    frame.rename(
        columns={
            "id": "ID",
            "title": "Title",
            "writer": "Writer",
            "filename": "File",
            "model_used": "Model",
            "created_at": "Created",
        }
    ),
    hide_index=True,
    use_container_width=True,
)

selected_id = st.selectbox(
    "Select a project",
    options=[record["id"] for record in records],
    format_func=lambda value: next(
        f"{record['title']} - {record['writer']} (ID {record['id']})"
        for record in records
        if record["id"] == value
    ),
)

load_col, delete_col = st.columns(2)
with load_col:
    if st.button("Load project", type="primary", use_container_width=True):
        report = load_analysis(int(selected_id))
        st.session_state.analysis_report = report
        st.session_state.model_used = next(
            record["model_used"] for record in records if record["id"] == selected_id
        )
        st.session_state.analysis_saved_id = selected_id
        st.success(f"Loaded {report.metadata.title}.")
        st.page_link("pages/overview.py", label="Open overview", icon=":material/arrow_forward:")
with delete_col:
    if st.button("Delete selected project", use_container_width=True):
        delete_analysis(int(selected_id))
        st.success("Project deleted.")
        st.rerun()
