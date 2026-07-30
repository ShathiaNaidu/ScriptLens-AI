from __future__ import annotations

import streamlit as st

from config import APP_TAGLINE
from core.ui import hero

hero(
    "Cinevora AI",
    f"{APP_TAGLINE}. One workspace for screenplay writing, AI development, visualisation, production planning, pitching, collaboration, talent, education, and film community workflows.",
)

st.markdown("### Complete creative-to-production workflow")
features = [
    ("Screenplay Writing", "Write and edit screenplays inside the app."),
    ("Professional Script Formatting", "Clean screenplay structure and export Fountain-friendly text."),
    ("Import / Export Script Files", "PDF, DOCX, TXT, Fountain and Markdown import; TXT, Fountain, DOCX and PDF export."),
    ("AI Script Analysis", "Structured screenplay report with scores, strengths, limitations, and evidence."),
    ("Story Structure Analysis", "Acts, story movements, key events and structure feedback."),
    ("Character Analysis", "Goals, conflicts, traits, relationships and arcs."),
    ("Dialogue Analysis", "Voice, naturalness, exposition, comedy timing and improvements."),
    ("Theme Analysis", "Themes, contradictions, cultural identity and thematic revision opportunities."),
    ("Scene Analysis", "Purpose, stakes, pacing, suspense, setup, payoff and scene-level notes."),
    ("AI Improvement Suggestions", "Prioritized revision roadmap for the next draft."),
    ("AI Story Consultant", "Interactive development Q&A grounded in the analysed screenplay."),
    ("AI Story Generation", "Original concepts, beat sheets, outlines, treatments and scenes."),
    ("AI Script Rewrite Assistant", "Rewrite dialogue or scenes toward a specific creative goal."),
    ("AI Audience Prediction", "Audience segments, likely hooks and positioning estimates."),
    ("Similar Movie Comparison", "Creative comparables and positioning lessons with clear limitations."),
    ("AI Voice Consultant", "Character-voice consistency and dialogue alternatives."),
    ("Emotional Timeline", "Scene-by-scene emotional intensity and suspense trajectory."),
    ("Production Planning", "Scene breakdown, location consolidation and shooting-plan assistance."),
    ("Budget Estimation", "Editable planning calculator plus AI pitch-budget context."),
    ("Pitch Deck Generator", "Synopsis, director vision, market strategy, poster concept and editable PPTX."),
    ("Casting Support", "Role briefs, audition priorities and casting-call preparation."),
    ("Collaboration Tools", "Project notes, tasks, decisions, approvals and handoffs."),
    ("Talent Marketplace", "Workspace directory for actors, crew and creative professionals."),
    ("Professional Consultation", "Consultation request queue and AI briefing pack."),
    ("University Platform", "Course milestones, project tracking and rubric-style feedback."),
    ("Film Community", "Project posts, opportunities, feedback requests and discussions."),
]

html = '<div class="cv-feature-grid">' + ''.join(
    f'<div class="cv-feature-card"><b>✓ {title}</b><span>{description}</span></div>' for title, description in features
) + '</div>'
st.markdown(html, unsafe_allow_html=True)

c1,c2,c3=st.columns(3)
with c1:
    st.page_link("pages/writer.py", label="Start writing", icon=":material/edit_note:")
with c2:
    st.page_link("pages/upload.py", label="Analyse a screenplay", icon=":material/upload_file:")
with c3:
    st.page_link("pages/storyboard.py", label="Open visual studio", icon=":material/view_carousel:")

st.markdown("---")
st.subheader("How Cinevora works")
steps=st.columns(5)
workflow=[
    ("01","Write","Create or import the screenplay."),
    ("02","Analyse","Gemini builds the screenplay intelligence layer."),
    ("03","Develop","Revise story, dialogue, theme and character."),
    ("04","Produce","Plan shots, schedule, budget and casting."),
    ("05","Pitch","Create visual assets, deck, reports and industry workflow."),
]
for col,(number,title,text) in zip(steps,workflow):
    with col:
        st.markdown(f'<div class="sl-card"><div class="sl-kicker">{number}</div><h3>{title}</h3><p>{text}</p></div>',unsafe_allow_html=True)

st.info("Industry/community features in this build are functional workspace tools. For a public multi-user commercial service, connect authentication, moderation, messaging and persistent hosted storage.")
