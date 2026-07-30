from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import hero, require_report

report=require_report()
hero("Casting Support", "Create role briefs, audition priorities, chemistry considerations, and casting-call copy from the characters already identified in the screenplay.")

character_name=st.selectbox("Character", [c.name for c in report.characters])
character=next(c for c in report.characters if c.name==character_name)
left,right=st.columns(2)
with left:
    st.markdown(f"### {character.name}")
    st.write(character.role)
    st.write("**Traits:** "+", ".join(character.traits))
    st.write("**Goal:** "+character.goal)
    st.write("**Conflict:** "+character.conflict)
with right:
    st.write("**Arc**")
    st.write(f"Beginning: {character.arc.beginning}")
    st.write(f"Middle: {character.arc.middle}")
    st.write(f"Ending: {character.arc.ending}")

brief_type=st.selectbox("Generate", ["Casting brief", "Audition checklist", "Casting call notice", "Chemistry-read plan", "Self-tape instructions"])
if st.button("Generate casting support", type="primary", icon=":material/person_search:"):
    prompt=f"""You are Cinevora AI's casting support assistant. Create a professional {brief_type} for character {character.name}, using only supported story information. Focus on performance qualities, emotional range, relationships, scene demands, and audition evaluation. Do not infer protected traits (race, religion, disability, sexuality, health) unless explicitly essential and stated in the screenplay. Do not recommend a real actor unless the user has explicitly named one.\n\n{report_context(report,28000)}"""
    try: st.session_state.casting_result=generate_text(prompt,temperature=0.45)
    except CinevoraAIError as exc: st.error(str(exc))
if st.session_state.get("casting_result"): st.markdown(st.session_state.casting_result)
