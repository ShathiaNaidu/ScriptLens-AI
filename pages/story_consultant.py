from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import get_report, hero

hero("AI Story Consultant", "Ask development questions about your analysed screenplay—or discuss a story idea before uploading a script.")
report=get_report()

for item in st.session_state.consultant_chat:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

question=st.chat_input("Ask Cinevora about structure, character, scene logic, stakes, pacing, genre, theme, or pitch...")
if question:
    st.session_state.consultant_chat.append({"role":"user","content":question})
    context = report_context(report) if report else "No screenplay analysis is currently loaded. Answer as a general story consultant and ask for missing facts rather than inventing them."
    history="\n".join(f"{x['role'].upper()}: {x['content']}" for x in st.session_state.consultant_chat[-8:])
    prompt=f"""You are Cinevora AI, a practical screenplay consultant. Give clear, constructive, specific advice. Distinguish facts from suggestions. If an analysed screenplay is supplied, do not invent scenes or quotes.

SCREENPLAY CONTEXT:\n{context}\n\nRECENT CONVERSATION:\n{history}\n\nAnswer the latest user question."""
    try:
        response=generate_text(prompt,temperature=0.55)
    except CinevoraAIError as exc:
        response=str(exc)
    st.session_state.consultant_chat.append({"role":"assistant","content":response})
    st.rerun()

if st.session_state.consultant_chat and st.button("Clear consultant conversation"):
    st.session_state.consultant_chat=[]
    st.rerun()
