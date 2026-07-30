from __future__ import annotations

import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import get_report, hero

hero("AI Voice Consultant", "Check whether dialogue sounds consistent with a character's established voice and generate alternatives without changing story facts.")
report=get_report()
if report and report.characters:
    character=st.selectbox("Character", [c.name for c in report.characters])
    profile=next(c for c in report.characters if c.name==character)
    st.caption(f"Role: {profile.role} · Traits: {', '.join(profile.traits)}")
else:
    character=st.text_input("Character name")
line=st.text_area("Dialogue line or short exchange", height=180)
intent=st.text_input("What should the character achieve in this moment?", placeholder="Hide fear while warning a friend")
if st.button("Analyse character voice", type="primary", icon=":material/record_voice_over:"):
    if not line.strip(): st.warning("Enter dialogue first.")
    else:
        context=report_context(report,25000) if report else "No analysed screenplay supplied."
        prompt=f"""You are Cinevora AI's dialogue and character-voice coach. Analyse the following line for character consistency, subtext, rhythm, exposition, distinctiveness, and speakability. Then give three alternative versions: subtle, emotionally stronger, and concise. Do not add new plot facts.
Character: {character}
Intent: {intent or 'not specified'}
Dialogue: {line}
Analysis context: {context}"""
        try: st.session_state.voice_result=generate_text(prompt,temperature=0.65)
        except CinevoraAIError as exc: st.error(str(exc))
if st.session_state.get("voice_result"): st.markdown(st.session_state.voice_result)
