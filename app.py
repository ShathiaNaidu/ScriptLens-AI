from __future__ import annotations

import streamlit as st

from config import APP_NAME
from core.intro import render_cinematic_intro
from core.ui import init_session_state, inject_css, status_sidebar


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_css()

if not render_cinematic_intro():
    st.stop()

status_sidebar()

pages = {
    "Start": [
        st.Page("pages/home.py", title="Home", icon=":material/home:", default=True),
        st.Page("pages/upload.py", title="Upload & Analyse", icon=":material/upload_file:"),
        st.Page("pages/projects.py", title="Saved Projects", icon=":material/folder_open:"),
    ],
    "Write & Develop": [
        st.Page("pages/writer.py", title="Screenplay Writing & Formatting", icon=":material/edit_note:"),
        st.Page("pages/story_generation.py", title="AI Story Generation", icon=":material/auto_awesome:"),
        st.Page("pages/rewrite.py", title="AI Script Rewrite Assistant", icon=":material/contract_edit:"),
        st.Page("pages/story_consultant.py", title="AI Story Consultant", icon=":material/forum:"),
        st.Page("pages/voice_consultant.py", title="AI Voice Consultant", icon=":material/record_voice_over:"),
    ],
    "Screenplay Intelligence": [
        st.Page("pages/overview.py", title="AI Script Analysis", icon=":material/dashboard:"),
        st.Page("pages/structure.py", title="Story Structure Analysis", icon=":material/account_tree:"),
        st.Page("pages/characters.py", title="Character Analysis", icon=":material/groups:"),
        st.Page("pages/dialogue.py", title="Dialogue Analysis", icon=":material/forum:"),
        st.Page("pages/themes.py", title="Theme Analysis", icon=":material/psychology:"),
        st.Page("pages/scenes.py", title="Scene Analysis", icon=":material/theaters:"),
        st.Page("pages/improvements.py", title="AI Improvement Suggestions", icon=":material/build_circle:"),
        st.Page("pages/audience.py", title="AI Audience Prediction", icon=":material/groups_2:"),
        st.Page("pages/similar_movies.py", title="Similar Movie Comparison", icon=":material/movie:"),
        st.Page("pages/emotional_timeline.py", title="Emotional Timeline", icon=":material/timeline:"),
        st.Page("pages/genre.py", title="Genre & Scores", icon=":material/analytics:"),
        st.Page("pages/market.py", title="Originality & Market", icon=":material/target:"),
    ],
    "Visualise & Pitch": [
        st.Page("pages/storyboard.py", title="Storyboard Generator", icon=":material/view_carousel:"),
        st.Page("pages/pitch.py", title="Pitch Deck Generator", icon=":material/campaign:"),
    ],
    "Production": [
        st.Page("pages/production.py", title="Production Planning", icon=":material/event_note:"),
        st.Page("pages/budget.py", title="Budget Estimation", icon=":material/payments:"),
        st.Page("pages/casting.py", title="Casting Support", icon=":material/person_search:"),
    ],
    "Industry & Community": [
        st.Page("pages/collaboration.py", title="Collaboration Tools", icon=":material/groups:"),
        st.Page("pages/talent_marketplace.py", title="Talent Marketplace", icon=":material/work:"),
        st.Page("pages/consultation.py", title="Professional Consultation", icon=":material/support_agent:"),
        st.Page("pages/university.py", title="University Platform", icon=":material/school:"),
        st.Page("pages/community.py", title="Film Community", icon=":material/diversity_3:"),
    ],
    "Export": [
        st.Page("pages/report.py", title="Download AI Report", icon=":material/download:"),
    ],
}

navigation = st.navigation(pages, position="sidebar")
navigation.run()
