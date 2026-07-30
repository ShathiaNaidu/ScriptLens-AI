from __future__ import annotations

import streamlit as st

from core.storage import add_community_post, list_community_posts
from core.ui import hero

hero("Film Community", "Share project updates, collaboration calls, feedback requests, screenings, and filmmaking discussions inside the Cinevora workspace.")

with st.expander("Create community post", expanded=False):
    with st.form("community_form"):
        author=st.text_input("Display name")
        category=st.selectbox("Category", ["Project Update","Feedback Request","Crew Call","Casting Call","Screening","Opportunity","Question","Discussion"])
        title=st.text_input("Post title")
        body=st.text_area("Post")
        submit=st.form_submit_button("Publish", type="primary")
    if submit:
        if not title.strip() or not body.strip(): st.warning("Title and post text are required.")
        else:
            add_community_post(author.strip() or "Community Member",category,title.strip(),body.strip())
            st.success("Post published to this Cinevora workspace.")

posts=list_community_posts()
filter_cat=st.selectbox("Filter feed", ["All"]+sorted({p['category'] for p in posts})) if posts else "All"
visible=[p for p in posts if filter_cat=="All" or p['category']==filter_cat]
for p in visible:
    with st.container(border=True):
        st.caption(f"{p['category']} · {p['author']} · {p['created_at'][:10]}")
        st.markdown(f"### {p['title']}")
        st.write(p['body'])
if not visible: st.info("No community posts yet.")
st.caption("This local community feed is suitable for demos/small private workspaces. Public deployment needs authentication, moderation, reporting, abuse prevention, privacy controls, and hosted persistent storage.")
