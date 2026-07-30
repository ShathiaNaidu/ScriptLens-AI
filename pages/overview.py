from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import hero, list_or_dash, metric_row, render_bullets, require_report, score_dataframe


report = require_report()
meta = report.metadata

hero(
    meta.title,
    f"A structured screenplay development report for {meta.writer}.",
)

metric_row(
    [
        ("Overall score", f"{report.scores.overall_score}/100", "AI development score"),
        ("Estimated runtime", f"{meta.estimated_runtime_minutes} min", "Approximate runtime"),
        ("Scenes", meta.scene_count, "Detected screenplay scenes"),
        ("Characters", len(report.characters), "Meaningful named characters"),
        ("Locations", len(meta.locations), "Distinct detected locations"),
    ]
)

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Story concept")
    st.write(meta.story_concept)
    st.markdown(f"**Logline:** {meta.logline}")
    st.markdown(f"**Central conflict:** {meta.central_conflict}")
    st.markdown(f"**Themes:** {list_or_dash(meta.main_themes)}")

    st.subheader("Main recommendation")
    st.info(report.main_recommendation)

with right:
    st.subheader("Screenplay details")
    detail_rows = [
        ("Writer", meta.writer),
        ("Genre", " / ".join(meta.genres)),
        ("Format", meta.format),
        ("Pages", str(meta.page_count)),
        ("Languages", list_or_dash(meta.languages_detected)),
        ("Locations", list_or_dash(meta.locations)),
    ]
    for label, value in detail_rows:
        st.markdown(f"**{label}:** {value}")

    genre_html = "".join(f'<span class="sl-pill">{genre}</span>' for genre in meta.genres)
    st.markdown(genre_html, unsafe_allow_html=True)

st.markdown("---")
score_col, feedback_col = st.columns([1.05, 1])
with score_col:
    st.subheader("Category scores")
    score_df = score_dataframe(report).set_index("Category")
    st.bar_chart(score_df, horizontal=True)
with feedback_col:
    st.subheader("Top strengths")
    render_bullets(report.top_strengths)
    st.subheader("Priority improvements")
    render_bullets(report.priority_improvements)

with st.expander("Correct extracted overview details"):
    st.caption("Use this when the AI misreads cover-page information. Changes affect the current session and downloads.")
    with st.form("metadata_editor"):
        title = st.text_input("Title", meta.title)
        writer = st.text_input("Writer", meta.writer)
        genres = st.text_input("Genres, separated by commas", ", ".join(meta.genres))
        runtime = st.number_input("Estimated runtime in minutes", 1, 600, meta.estimated_runtime_minutes)
        screenplay_format = st.text_input("Format", meta.format)
        logline = st.text_area("Logline", meta.logline)
        story_concept = st.text_area("Story concept", meta.story_concept)
        submitted = st.form_submit_button("Apply corrections")
    if submitted:
        meta.title = title.strip() or "Unknown"
        meta.writer = writer.strip() or "Unknown"
        meta.genres = [item.strip() for item in genres.split(",") if item.strip()]
        meta.estimated_runtime_minutes = int(runtime)
        meta.format = screenplay_format.strip() or "Unknown"
        meta.logline = logline.strip()
        meta.story_concept = story_concept.strip()
        st.session_state.analysis_report = report
        st.success("Overview corrections applied.")
        st.rerun()

with st.expander("Analysis limitations"):
    render_bullets(report.analysis_limitations)
