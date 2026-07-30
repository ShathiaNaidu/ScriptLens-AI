from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text
from core.ui import hero

hero("AI Story Generation", "Develop an original concept, outline, treatment, or screenplay scene from your own creative brief.")

with st.form("story_generator"):
    premise = st.text_area("Premise / idea", placeholder="A university student accidentally creates a chemical that temporarily transforms him into a zombie-like state...")
    genre = st.text_input("Genre", placeholder="Horror comedy / science fiction")
    setting = st.text_input("Setting", placeholder="Malaysian university campus")
    tone = st.text_input("Tone", placeholder="Suspenseful, funny, youthful")
    output_type = st.selectbox("Generate", ["Story concept + logline", "Beat sheet", "Three-act outline", "One-page treatment", "Opening scene", "Scene sequence"])
    constraints = st.text_area("Creative constraints", placeholder="Keep the cast small, suitable for a student production, no expensive VFX...")
    submitted = st.form_submit_button("Generate story", type="primary")
if submitted:
    prompt=f"""You are Cinevora AI, a screenplay development partner. Create an ORIGINAL {output_type} based on the writer's brief. Do not imitate a living writer or copy an existing film. Preserve the user's requested cultural context and production constraints. Use screenplay formatting when generating a scene.

Premise: {premise}
Genre: {genre or 'unspecified'}
Setting: {setting or 'unspecified'}
Tone: {tone or 'unspecified'}
Constraints: {constraints or 'none'}"""
    try:
        with st.spinner("Developing the story..."):
            st.session_state.story_generation_result=generate_text(prompt, temperature=0.9)
    except CinevoraAIError as exc:
        st.error(str(exc))
if st.session_state.get("story_generation_result"):
    result=st.session_state.story_generation_result
    st.markdown(result)
    if st.button("Send result to screenplay editor", icon=":material/edit_note:"):
        st.session_state.screenplay_editor = result
        st.success("Sent to Screenplay Writing & Formatting.")
