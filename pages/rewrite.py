from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text
from core.ui import hero

hero("AI Script Rewrite Assistant", "Rewrite a selected screenplay passage while preserving story facts, character identity, and screenplay format.")

source = st.text_area("Scene or dialogue to rewrite", value=st.session_state.get("rewrite_source", ""), height=350)
st.session_state.rewrite_source=source
goal=st.selectbox("Rewrite goal", ["Make dialogue more natural", "Increase suspense", "Improve pacing", "Strengthen emotion", "Reduce exposition", "Make comedy sharper", "Make action more visual", "Shorten the scene", "Custom"])
custom=st.text_input("Custom goal", disabled=goal!="Custom")
strength=st.slider("Rewrite intensity",1,5,3,help="1 = light polish, 5 = substantial rewrite while keeping the same story purpose.")
if st.button("Rewrite", type="primary", icon=":material/contract_edit:"):
    if not source.strip():
        st.warning("Paste a screenplay passage first.")
    else:
        actual_goal=custom if goal=="Custom" and custom.strip() else goal
        prompt=f"""You are Cinevora AI's screenplay rewrite assistant. Rewrite the passage to achieve: {actual_goal}. Rewrite intensity: {strength}/5. Preserve character names, established plot facts, and the scene's core purpose. Do not add unrelated plot developments. Return the revised screenplay passage first, followed by 3-6 concise notes explaining the changes.

PASSAGE:\n{source}"""
        try:
            st.session_state.rewrite_result=generate_text(prompt,temperature=0.65)
        except CinevoraAIError as exc:
            st.error(str(exc))
if st.session_state.get("rewrite_result"):
    st.text_area("Rewritten version", st.session_state.rewrite_result, height=500)
    if st.button("Use in screenplay editor"):
        st.session_state.screenplay_editor=st.session_state.rewrite_result
        st.success("Added to the writing workspace.")
