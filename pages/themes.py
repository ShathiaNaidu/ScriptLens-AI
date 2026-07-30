from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import hero, render_bullets, require_report

report = require_report()
hero("Theme Analysis", "Explore the screenplay's central ideas, recurring tensions, thematic contradictions, and opportunities to express theme through action rather than exposition.")

st.subheader("Detected main themes")
render_bullets(report.metadata.main_themes)

left, right = st.columns(2)
with left:
    st.subheader("Distinctive thematic identity")
    render_bullets(report.originality.distinctive_elements)
with right:
    st.subheader("Local / cultural opportunities")
    render_bullets(report.originality.local_identity_opportunities)

if st.button("Generate deep thematic analysis", type="primary", icon=":material/psychology:"):
    prompt = f"""You are Cinevora AI's screenplay theme consultant.
Using ONLY the screenplay analysis JSON below, produce a professional theme report with:
1. Core thematic statement
2. 3-6 major themes
3. How each theme is dramatized through character choices/scenes
4. Contradictions or underdeveloped themes
5. Specific revision opportunities
6. A concise thematic promise to the audience
Do not invent scenes or quotations.

ANALYSIS JSON:\n{report_context(report)}"""
    try:
        with st.spinner("Building thematic map..."):
            st.session_state.theme_deep_dive = generate_text(prompt, temperature=0.45)
    except CinevoraAIError as exc:
        st.error(str(exc))
if st.session_state.get("theme_deep_dive"):
    st.markdown(st.session_state.theme_deep_dive)
