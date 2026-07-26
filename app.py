from __future__ import annotations

import streamlit as st

from core.ui import init_session_state, inject_css, status_sidebar


st.set_page_config(
    page_title="ScriptLens AI",
    page_icon=":material/movie_edit:",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_css()
status_sidebar()

pages = {
    "Start": [
        st.Page("pages/home.py", title="Home", icon=":material/home:", default=True),
        st.Page("pages/upload.py", title="Upload & Analyse", icon=":material/upload_file:"),
        st.Page("pages/projects.py", title="Saved Projects", icon=":material/folder_open:"),
    ],
    "Screenplay Report": [
        st.Page("pages/overview.py", title="Overview", icon=":material/dashboard:"),
        st.Page("pages/characters.py", title="Characters", icon=":material/groups:"),
        st.Page("pages/structure.py", title="Story Structure", icon=":material/account_tree:"),
        st.Page("pages/scenes.py", title="Scene Analysis", icon=":material/theaters:"),
        st.Page("pages/dialogue.py", title="Dialogue", icon=":material/forum:"),
        st.Page("pages/genre.py", title="Genre & Scores", icon=":material/analytics:"),
        st.Page("pages/market.py", title="Originality & Market", icon=":material/target:"),
        st.Page("pages/storyboard.py", title="Storyboard Generator", icon=":material/view_carousel:"),
        st.Page("pages/pitch.py", title="Pitch Generator", icon=":material/campaign:"),
        st.Page("pages/report.py", title="Download Report", icon=":material/download:"),
    ],
}

navigation = st.navigation(pages, position="sidebar")
navigation.run()
