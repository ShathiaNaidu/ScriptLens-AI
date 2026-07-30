from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.storage import add_consultation_request, list_consultation_requests
from core.ui import get_report, hero

hero("Professional Consultation", "Prepare a consultant-ready brief and track requests for script editing, directing, production, pitching, or market consultation.")
report=get_report()
project=report.metadata.title if report else st.text_input("Project title", value="Untitled Project")

left,right=st.columns([1,1])
with left:
    st.subheader("Request consultation")
    with st.form("consult_request"):
        requester=st.text_input("Your name / team")
        topic=st.selectbox("Consultation area", ["Script Development","Story Structure","Dialogue","Directing","Production Planning","Budgeting","Pitch & Market","Festival Strategy","Other"])
        notes=st.text_area("What help do you need?")
        submit=st.form_submit_button("Save request", type="primary")
    if submit:
        add_consultation_request(project,requester.strip() or "Anonymous",topic,notes.strip())
        st.success("Consultation request added to the workspace queue.")
with right:
    st.subheader("AI consultation prep pack")
    if st.button("Prepare briefing document", icon=":material/support_agent:", use_container_width=True):
        context=report_context(report) if report else f"Project title: {project}. No screenplay analysis loaded."
        prompt=f"""You are Cinevora AI preparing a project for a HUMAN professional consultant. Create a concise briefing pack containing: project snapshot, key strengths, biggest uncertainties, 8 high-value questions to ask the consultant, evidence/examples from the analysis when available, and decisions the team should make after the session. Do not pretend a human consultation has occurred.\n\n{context}"""
        try: st.session_state.consult_prep=generate_text(prompt,temperature=0.35)
        except CinevoraAIError as exc: st.error(str(exc))
    if st.session_state.get("consult_prep"): st.markdown(st.session_state.consult_prep)

requests=list_consultation_requests()
if requests:
    st.subheader("Consultation queue")
    df=pd.DataFrame(requests)
    st.dataframe(df[["project_title","requester","topic","status","created_at"]],hide_index=True,use_container_width=True)
st.caption("Cinevora can prepare and track consultation requests. Actual professional consultation requires a real consultant or service provider connected to your deployment.")
