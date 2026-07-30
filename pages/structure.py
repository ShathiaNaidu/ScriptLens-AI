from __future__ import annotations

import streamlit as st

from core.ui import hero, render_bullets, require_report


report = require_report()
hero(
    "Story structure analysis",
    "How the screenplay sets up its conflict, escalates pressure, and delivers its resolution.",
)

if not report.acts:
    st.info("The AI did not identify a reliable act or movement structure.")
    st.stop()

for act in report.acts:
    with st.expander(
        f"Act {act.act_number}: {act.title} - {act.approximate_scene_range}",
        expanded=act.act_number == 1,
    ):
        st.markdown(f"**Purpose:** {act.purpose}")
        if act.scenes:
            st.markdown(f"**Included scenes:** {', '.join(map(str, act.scenes))}")
        event_col, assessment_col = st.columns(2)
        with event_col:
            st.markdown("#### Key events")
            render_bullets(act.key_events)
        with assessment_col:
            st.markdown("#### Strengths")
            render_bullets(act.strengths)
            st.markdown("#### Suggestions")
            render_bullets(act.suggestions)

st.markdown("---")
st.subheader("Structure-level priorities")
render_bullets(report.priority_improvements)
