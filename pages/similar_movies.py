from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import hero, require_report

report=require_report()
hero("Similar Movie Comparison", "Generate creative and market-positioning comparables while keeping the screenplay's unique identity clear.")

st.warning("Comparables are AI suggestions from model knowledge, not an exhaustive or live box-office/streaming database. Verify titles and current market performance before using them in an investor pitch.")
mode=st.selectbox("Comparison focus", ["Story premise", "Genre & tone", "Target audience", "Production scale", "Streaming positioning", "Malaysian / regional context"])
known=st.text_input("Optional titles you want compared", placeholder="Example: Zombieland, Happy Death Day")
if st.button("Generate comparable films", type="primary", icon=":material/movie:"):
    prompt=f"""You are Cinevora AI's film positioning analyst. Based only on this screenplay analysis, suggest 3-6 well-known film/series comparables for {mode}. For each: explain the useful similarity, the important difference, what Cinevora's screenplay should NOT copy, and the positioning lesson. If user-specified titles are provided, include them where relevant. Never claim current revenue, platform availability, awards, or rights unless provided.
User titles: {known or 'none'}
\n{report_context(report)}"""
    try: st.session_state.comp_result=generate_text(prompt,temperature=0.45)
    except CinevoraAIError as exc: st.error(str(exc))
if st.session_state.get("comp_result"): st.markdown(st.session_state.comp_result)
