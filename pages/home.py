from __future__ import annotations

import streamlit as st

from core.report_generator import APP_TARGET_MARKET
from core.ui import hero, render_bullets


hero(
    "AI screenplay development, from PDF to producer pitch",
    "Upload a screenplay, extract its structure, evaluate characters and scenes, predict audiences, and generate a professional development report.",
)

left, right = st.columns([1.25, 1])
with left:
    st.subheader("What the app analyses")
    feature_cols = st.columns(2)
    features = [
        ("Screenplay extraction", "Title, writer, genres, scenes, locations, dialogue, and action."),
        ("Character database", "Goals, conflicts, traits, arcs, relationships, and evidence."),
        ("Story structure", "Acts, key events, setup, escalation, climax, and resolution."),
        ("Scene diagnosis", "Purpose, emotion, stakes, pacing, suspense, clues, and payoff."),
        ("Dialogue feedback", "Voice consistency, naturalness, exposition, and comedy timing."),
        ("Industry preparation", "Logline, synopsis, target market, selling points, pitch, and Cloudflare FLUX concept art."),
    ]
    for index, (title, description) in enumerate(features):
        with feature_cols[index % 2]:
            st.markdown(
                f'<div class="sl-card"><strong>{title}</strong><br><span>{description}</span></div>',
                unsafe_allow_html=True,
            )

    st.page_link("pages/upload.py", label="Upload a screenplay", icon=":material/arrow_forward:")

with right:
    st.subheader("Important boundaries")
    st.info(
        "The application gives development feedback, not a guarantee of production success. "
        "Its originality section identifies storytelling patterns but does not perform a legal plagiarism investigation."
    )
    st.markdown("#### Target market of the application")
    render_bullets(APP_TARGET_MARKET)

st.markdown("---")
st.subheader("Recommended workflow")
steps = st.columns(4)
workflow = [
    ("1", "Upload", "Add a screenplay PDF and Gemini API key."),
    ("2", "Analyse", "Gemini reads the PDF natively and returns structured JSON."),
    ("3", "Review", "Inspect evidence, scores, suggestions, audience, and pitch."),
    ("4", "Export", "Download JSON, DOCX, or PDF development reports."),
]
for col, (number, title, text) in zip(steps, workflow):
    with col:
        st.markdown(
            f'<div class="sl-card"><div class="sl-kicker">STEP {number}</div><h3>{title}</h3><p>{text}</p></div>',
            unsafe_allow_html=True,
        )


st.markdown("---")
st.subheader("Production-ready AI workflow")
step13, step14 = st.columns(2)
with step13:
    st.markdown(
        '<div class="sl-card"><div class="sl-kicker">STEP 13</div><h3>Storyboard Generator</h3>'
        '<p>Turns analysed scenes into visual frames with camera angle, shot type, character blocking, lighting, mood, and optional AI concept art.</p></div>',
        unsafe_allow_html=True,
    )
with step14:
    st.markdown(
        '<div class="sl-card"><div class="sl-kicker">STEP 14</div><h3>Pitch Generator</h3>'
        '<p>Builds the logline, synopsis, character profiles, director vision, mood board, budget estimate, audience, platforms, marketing, poster concept, investor deck, and final AI report.</p></div>',
        unsafe_allow_html=True,
    )
