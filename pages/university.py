from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.storage import add_university_item, list_university_items
from core.ui import get_report, hero

hero("University Platform", "A classroom workspace for screenplay projects, milestones, feedback preparation, and rubric-based evaluation.")
report=get_report()

with st.form("uni_item"):
    c1,c2=st.columns(2)
    course=c1.text_input("Course / module", placeholder="Screenwriting 2")
    team=c2.text_input("Student / team")
    project=st.text_input("Project title", value=report.metadata.title if report else "")
    milestone=st.selectbox("Milestone", ["Idea","Logline","Treatment","First Draft","Table Read","Revision","Pitch","Final Submission"])
    status=st.selectbox("Status", ["Planned","In progress","Submitted","Reviewed","Completed"])
    notes=st.text_area("Notes / lecturer feedback")
    submit=st.form_submit_button("Add project milestone", type="primary")
if submit:
    add_university_item(course.strip() or "Course",project.strip() or "Untitled",team.strip() or "Student/Team",milestone,status,notes.strip())
    st.success("University milestone saved.")

items=list_university_items()
if items:
    df=pd.DataFrame(items)
    st.dataframe(df[["course","project_title","student_or_team","milestone","status","created_at"]],hide_index=True,use_container_width=True)

if report and st.button("Generate assessment rubric feedback", icon=":material/school:"):
    prompt=f"""You are Cinevora AI supporting a university screenplay assessment. Produce rubric-style feedback for: concept/problem significance, story structure, character development, dialogue, originality, technical screenplay craft, production feasibility, audience/impact, presentation/pitch readiness. Give strengths, evidence from the analysis, revision actions, and a suggested score band without claiming to replace the lecturer's grade.\n\n{report_context(report)}"""
    try: st.session_state.uni_feedback=generate_text(prompt,temperature=0.3)
    except CinevoraAIError as exc: st.error(str(exc))
if st.session_state.get("uni_feedback"): st.markdown(st.session_state.uni_feedback)
st.caption("For a real institution-wide deployment, add university SSO, roles, permissions, hosted storage, submission deadlines, and lecturer/student access controls.")
