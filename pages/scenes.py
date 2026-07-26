from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import hero, list_or_dash, render_bullets, require_report


report = require_report()
hero(
    "Scene-by-scene analysis",
    "Review purpose, emotion, conflict, stakes, pacing, suspense, originality, setup, and payoff.",
)

if not report.scenes:
    st.info("No scenes were reliably detected.")
    st.stop()

scene_frame = pd.DataFrame(
    [
        {
            "Scene": scene.scene_number,
            "Heading": scene.heading,
            "Location": scene.location,
            "Emotion": scene.dominant_emotion,
            "Suspense": scene.suspense_score,
            "Originality": scene.originality_score,
            "Purpose": scene.purpose,
        }
        for scene in report.scenes
    ]
)

filter_col, chart_col = st.columns([0.65, 1.35])
with filter_col:
    locations = sorted({scene.location for scene in report.scenes if scene.location})
    location_filter = st.multiselect("Filter by location", locations)
    min_suspense = st.slider("Minimum suspense", 0, 10, 0)
with chart_col:
    chart_data = scene_frame.set_index("Scene")[["Suspense", "Originality"]]
    st.line_chart(chart_data)

filtered = scene_frame[scene_frame["Suspense"] >= min_suspense]
if location_filter:
    filtered = filtered[filtered["Location"].isin(location_filter)]
st.dataframe(filtered, hide_index=True, use_container_width=True)

available_scenes = filtered["Scene"].tolist() if not filtered.empty else scene_frame["Scene"].tolist()
selected_scene_number = st.selectbox("Open scene", available_scenes)
scene = next(item for item in report.scenes if item.scene_number == selected_scene_number)

st.subheader(f"Scene {scene.scene_number}: {scene.heading}")
metric_cols = st.columns(4)
metric_cols[0].metric("Suspense", f"{scene.suspense_score}/10")
metric_cols[1].metric("Originality", f"{scene.originality_score}/10")
metric_cols[2].metric("Emotion", scene.dominant_emotion)
metric_cols[3].metric("Pacing", scene.pacing)

left, right = st.columns(2)
with left:
    st.markdown(f"**Location:** {scene.location}")
    st.markdown(f"**Time:** {scene.time_of_day}")
    st.markdown(f"**Characters:** {list_or_dash(scene.characters)}")
    st.markdown(f"**Summary:** {scene.summary}")
    st.markdown(f"**Purpose:** {scene.purpose}")
    st.markdown(f"**Conflict:** {scene.conflict}")
    st.markdown(f"**Stakes:** {scene.stakes}")
    st.markdown(f"**Payoff:** {scene.payoff}")
with right:
    st.markdown("#### Strengths")
    render_bullets(scene.strengths)
    st.markdown("#### Suggestions")
    render_bullets(scene.suggestions)
    st.markdown("#### Clues and setup")
    render_bullets(scene.clues_or_setup)

with st.expander("Evidence"):
    if not scene.evidence:
        st.caption("No precise evidence references were returned.")
    for evidence in scene.evidence:
        st.markdown(
            f"**Page {evidence.page_number or '-'}:** “{evidence.short_quote}”  \n{evidence.explanation}"
        )
