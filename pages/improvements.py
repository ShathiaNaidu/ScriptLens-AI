from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import hero, render_bullets, require_report

report = require_report()
hero("AI Improvement Suggestions", "Turn Cinevora's diagnosis into a prioritized revision plan for the next screenplay draft.")

p1, p2 = st.columns(2)
with p1:
    st.subheader("Priority improvements")
    render_bullets(report.priority_improvements)
with p2:
    st.subheader("Protect these strengths")
    render_bullets(report.top_strengths)

st.subheader("Scene-level revision opportunities")
for scene in report.scenes:
    if scene.suggestions:
        with st.expander(f"Scene {scene.scene_number}: {scene.heading}"):
            render_bullets(scene.suggestions)

focus = st.selectbox("Revision focus", ["Whole screenplay", "Structure", "Characters", "Dialogue", "Pacing", "Suspense", "Commercial clarity", "Production practicality"])
if st.button("Build revision roadmap", type="primary", icon=":material/route:"):
    prompt = f"""Act as Cinevora AI's senior script editor. Build a concrete revision roadmap focused on {focus}.
Use only this existing screenplay analysis. Prioritize changes as MUST / SHOULD / COULD. For each item include why it matters, where it applies, and a practical rewrite action. Preserve the writer's premise and voice. Do not invent new facts.

{report_context(report)}"""
    try:
        with st.spinner("Prioritising revisions..."):
            st.session_state.revision_roadmap = generate_text(prompt, temperature=0.4)
    except CinevoraAIError as exc:
        st.error(str(exc))
if st.session_state.get("revision_roadmap"):
    st.markdown(st.session_state.revision_roadmap)
