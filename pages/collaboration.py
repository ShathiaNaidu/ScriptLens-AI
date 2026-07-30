from __future__ import annotations

import pandas as pd
import streamlit as st

from core.storage import add_collaboration_item, list_collaboration_items
from core.ui import get_report, hero

hero("Collaboration Tools", "Keep revision notes, tasks, approvals, and team handoffs together with the screenplay project.")
report=get_report()
default_project=report.metadata.title if report else "Untitled Project"
project=st.text_input("Project", value=default_project)

with st.form("collab_form"):
    c1,c2=st.columns(2)
    item_type=c1.selectbox("Type", ["Task","Note","Decision","Feedback","Approval"])
    status=c2.selectbox("Status", ["Open","In progress","Waiting","Done"])
    title=st.text_input("Title")
    body=st.text_area("Details")
    owner=st.text_input("Owner / assignee", placeholder="Writer, Director, Editor...")
    submit=st.form_submit_button("Add collaboration item", type="primary")
if submit:
    if not title.strip(): st.warning("Add a title first.")
    else:
        add_collaboration_item(project.strip() or default_project,item_type,title.strip(),body.strip(),owner.strip() or "Unassigned",status)
        st.success("Collaboration item saved.")

items=list_collaboration_items(project.strip())
if items:
    df=pd.DataFrame(items)
    cols=[c for c in ["item_type","title","owner","status","created_at"] if c in df.columns]
    st.dataframe(df[cols],hide_index=True,use_container_width=True)
    for item in items:
        with st.expander(f"{item['item_type']} · {item['title']}"):
            st.write(item['body'] or "No details")
            st.caption(f"Owner: {item['owner']} · Status: {item['status']}")
else:
    st.info("No collaboration items for this project yet.")
st.caption("This build stores collaboration data in the app's local SQLite database. For multi-user production deployment, connect an authenticated hosted database such as PostgreSQL/Supabase.")
