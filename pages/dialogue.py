from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import hero, render_bullets, require_report


report = require_report()
hero(
    "Dialogue analysis",
    "Representative dialogue moments assessed for purpose, voice, naturalness, exposition, and comedy timing.",
)

identified_speakers = sorted(
    {character.name.strip() for character in report.characters if character.name.strip()},
    key=str.casefold,
)
analyzed_speakers = sorted(
    {item.speaker.strip() for item in report.dialogue_analysis if item.speaker.strip()},
    key=str.casefold,
)

# Character analysis identifies meaningful named speaking characters, while
# dialogue_analysis contains representative sampled moments. Use the union so
# the filter never silently hides a character if a model response misses a sample.
speaker_lookup = {name.casefold(): name for name in identified_speakers}
for name in analyzed_speakers:
    speaker_lookup.setdefault(name.casefold(), name)
speakers = sorted(speaker_lookup.values(), key=str.casefold)

analyzed_keys = {name.casefold() for name in analyzed_speakers}
missing_dialogue_samples = [
    name for name in identified_speakers if name.casefold() not in analyzed_keys
]

coverage_left, coverage_right = st.columns(2)
coverage_left.metric("Identified speaking characters", len(identified_speakers))
coverage_right.metric(
    "Speakers represented in dialogue",
    f"{len(identified_speakers) - len(missing_dialogue_samples)}/{len(identified_speakers)}"
    if identified_speakers
    else len(analyzed_speakers),
)

if missing_dialogue_samples:
    st.warning(
        "No representative dialogue sample was returned for: "
        + ", ".join(missing_dialogue_samples)
        + ". They remain available in the speaker filter. Re-analyse the screenplay "
        "with this updated version to request dialogue coverage for every speaking character."
    )

if not report.dialogue_analysis:
    st.info("No representative dialogue analysis was returned.")

selected_speakers = st.multiselect("Filter by speaker", speakers)
minimum_naturalness = st.slider("Minimum naturalness score", 0, 10, 0)

selected_keys = {name.casefold() for name in selected_speakers}
items = [
    item
    for item in report.dialogue_analysis
    if item.naturalness_score >= minimum_naturalness
    and (not selected_keys or item.speaker.strip().casefold() in selected_keys)
]

if selected_speakers and not items:
    st.info(
        "No representative dialogue sample matches the selected speaker(s) and naturalness threshold. "
        "The character can still be present in the screenplay even when Gemini did not return a sampled line."
    )

summary = pd.DataFrame(
    [
        {
            "Scene": item.scene_number or "-",
            "Speaker": item.speaker,
            "Excerpt": item.dialogue_excerpt,
            "Purpose": item.purpose,
            "Naturalness": item.naturalness_score,
            "Exposition": item.exposition_level,
            "Comedy timing": item.comedy_timing,
        }
        for item in items
    ]
)
st.dataframe(summary, hide_index=True, use_container_width=True)

for index, item in enumerate(items):
    with st.expander(
        f"{item.speaker} - Scene {item.scene_number or 'Unknown'}: “{item.dialogue_excerpt[:70]}”",
        expanded=index == 0,
    ):
        st.markdown(f"> {item.dialogue_excerpt}")
        left, right = st.columns(2)
        with left:
            st.markdown(f"**Purpose:** {item.purpose}")
            st.markdown(f"**Voice match:** {item.character_voice_match}")
            st.markdown(f"**Naturalness:** {item.naturalness_score}/10")
            st.markdown(f"**Exposition:** {item.exposition_level}")
            st.markdown(f"**Comedy timing:** {item.comedy_timing}")
        with right:
            st.markdown("#### Strengths")
            render_bullets(item.strengths)
            st.markdown("#### Improvements")
            render_bullets(item.improvements)
