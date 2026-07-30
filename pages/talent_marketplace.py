from __future__ import annotations

import pandas as pd
import streamlit as st

from core.storage import add_talent_profile, list_talent_profiles
from core.ui import hero

hero("Talent Marketplace", "Create and browse a lightweight in-app directory for actors, crew, writers, editors, composers, designers, and other film talent.")

browse,join=st.tabs(["Browse talent","Create profile"])
with join:
    with st.form("talent_form"):
        name=st.text_input("Display name")
        role=st.selectbox("Primary role", ["Actor","Director","Writer","Producer","Cinematographer","Editor","Sound","Composer","Production Designer","VFX","Makeup","Costume","Other"])
        location=st.text_input("Location")
        skills=st.text_area("Skills / credits / languages")
        portfolio=st.text_input("Portfolio link (optional)")
        contact=st.text_input("Professional contact (optional)")
        submit=st.form_submit_button("Publish profile", type="primary")
    if submit:
        if not name.strip(): st.warning("Display name is required.")
        else:
            add_talent_profile(name.strip(),role,location.strip(),skills.strip(),portfolio.strip(),contact.strip())
            st.success("Talent profile added to this Cinevora workspace.")
with browse:
    profiles=list_talent_profiles()
    role_filter=st.selectbox("Filter by role", ["All"]+sorted({p['role'] for p in profiles})) if profiles else "All"
    visible=[p for p in profiles if role_filter=="All" or p['role']==role_filter]
    for p in visible:
        with st.container(border=True):
            st.markdown(f"### {p['name']} · {p['role']}")
            st.caption(p['location'] or "Location not specified")
            st.write(p['skills'] or "No skills description yet.")
            if p['portfolio']: st.write(f"Portfolio: {p['portfolio']}")
            if p['contact']: st.write(f"Contact: {p['contact']}")
    if not visible: st.info("No talent profiles yet.")
st.caption("This is a functional workspace directory, not a verified hiring marketplace. Add identity verification, moderation, privacy controls, messaging, and a hosted database before public commercial use.")
