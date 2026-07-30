from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import hero, list_or_dash, render_bullets, require_report


report = require_report()
hero(
    "Character database",
    "Goals, conflicts, relationships, arcs, strengths, improvements, and screenplay evidence.",
)

if not report.characters:
    st.info("No meaningful named characters were detected.")
    st.stop()

summary = pd.DataFrame(
    [
        {
            "Character": character.name,
            "Role": character.role,
            "Traits": ", ".join(character.traits),
            "Goal": character.goal,
            "Conflict": character.conflict,
        }
        for character in report.characters
    ]
)
st.dataframe(summary, hide_index=True, use_container_width=True)

selected_name = st.selectbox("Select a character", [character.name for character in report.characters])
character = next(item for item in report.characters if item.name == selected_name)

left, right = st.columns([1.05, 1])
with left:
    st.subheader(character.name)
    st.markdown(f"**Role:** {character.role}")
    st.markdown(f"**Traits:** {list_or_dash(character.traits)}")
    st.markdown(f"**Goal:** {character.goal}")
    st.markdown(f"**Conflict:** {character.conflict}")
    st.markdown(f"**Relationships:** {list_or_dash(character.relationships)}")
    st.info(character.ai_feedback)

with right:
    st.subheader("Character arc")
    st.markdown(f"**Beginning:** {character.arc.beginning}")
    st.markdown(f"**Middle:** {character.arc.middle}")
    st.markdown(f"**Ending:** {character.arc.ending}")
    st.subheader("Strengths")
    render_bullets(character.strengths)
    st.subheader("Improvements")
    render_bullets(character.improvements)

st.subheader("Evidence")
if not character.evidence:
    st.caption("No precise evidence references were returned.")
else:
    evidence_rows = [
        {
            "Scene": evidence.scene_number or "-",
            "Page": evidence.page_number or "-",
            "Short quote": evidence.short_quote,
            "Explanation": evidence.explanation,
        }
        for evidence in character.evidence
    ]
    st.dataframe(pd.DataFrame(evidence_rows), hide_index=True, use_container_width=True)
