from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import hero, render_bullets, require_report

report = require_report()
hero("AI Audience Prediction", "Estimate who the screenplay may resonate with, why, and what revisions could strengthen audience fit.")

if report.audience_prediction:
    df = pd.DataFrame([
        {"Segment": x.segment, "Appeal": x.predicted_appeal, "Score": x.appeal_score, "Reason": x.reason}
        for x in report.audience_prediction
    ])
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.bar_chart(df.set_index("Segment")[["Score"]])
    for item in report.audience_prediction:
        with st.expander(f"{item.segment} · {item.appeal_score}/100"):
            st.write(item.reason)
            st.markdown("**Ways to strengthen appeal**")
            render_bullets(item.improvements_for_segment)
else:
    st.info("No audience segments were returned in the current analysis.")

region = st.text_input("Optional target region / market", placeholder="Example: Malaysia, Southeast Asia, global streaming")
if st.button("Generate audience strategy", type="primary", icon=":material/groups_2:"):
    prompt = f"""You are Cinevora AI's audience strategist. Based only on this screenplay analysis, estimate primary, secondary, and niche audience segments; emotional hooks; barriers to engagement; age-positioning considerations; and a release-positioning strategy. Target region: {region or 'not specified'}. Clearly label predictions as estimates, not market research guarantees.\n\n{report_context(report)}"""
    try:
        st.session_state.audience_strategy = generate_text(prompt, temperature=0.5)
    except CinevoraAIError as exc:
        st.error(str(exc))
if st.session_state.get("audience_strategy"):
    st.markdown(st.session_state.audience_strategy)
st.caption("Audience predictions are AI estimates and should be validated with real audience research, testing, and distributor/platform data.")
