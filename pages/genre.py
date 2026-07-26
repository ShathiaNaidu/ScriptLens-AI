from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import hero, render_bullets, require_report, score_dataframe


report = require_report()
hero(
    "Genre performance and scorecard",
    "Genre expectations, category scores, and the strongest revision opportunities.",
)

score_df = score_dataframe(report)
left, right = st.columns([1.15, 0.85])
with left:
    st.subheader("Screenplay scorecard")
    st.bar_chart(score_df.set_index("Category"), horizontal=True)
with right:
    st.metric("Overall score", f"{report.scores.overall_score}/100")
    st.info(report.main_recommendation)

st.subheader("Genre analysis")
if not report.genre_analysis:
    st.caption("No dominant genres were reliably identified.")
for genre in report.genre_analysis:
    with st.expander(f"{genre.genre}: {genre.score}/100", expanded=True):
        st.write(genre.reason)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Strengths")
            render_bullets(genre.strengths)
            st.markdown("#### Expectations met")
            render_bullets(genre.genre_expectations_met)
        with col2:
            st.markdown("#### Suggestions")
            render_bullets(genre.suggestions)
            st.markdown("#### Expectations missing")
            render_bullets(genre.genre_expectations_missing)

with st.expander("Edit scores for the current report"):
    st.caption(
        "The original scores come from the AI rubric. Manual edits are useful after a lecturer, producer, or writer reviews the screenplay."
    )
    editable = score_df.copy()
    edited = st.data_editor(
        editable,
        hide_index=True,
        use_container_width=True,
        disabled=["Category"],
        column_config={
            "Score": st.column_config.NumberColumn("Score", min_value=0, max_value=100, step=1)
        },
        key="score_editor",
    )
    if st.button("Apply edited scores"):
        reverse_map = {
            key.replace("_", " ").title(): key for key in report.scores.model_dump().keys()
        }
        for row in edited.to_dict("records"):
            field = reverse_map[row["Category"]]
            setattr(report.scores, field, int(row["Score"]))
        st.session_state.analysis_report = report
        st.success("Scores updated for the current session and downloads.")
        st.rerun()
