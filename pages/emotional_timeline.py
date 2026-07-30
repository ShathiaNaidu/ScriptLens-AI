from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import hero, require_report

report = require_report()
hero("Emotional Timeline", "See how suspense, stakes, pacing signals, and dominant emotion move across the screenplay scene by scene.")

emotion_weight = {
    "terror": 10, "fear": 9, "panic": 9, "grief": 9, "rage": 9, "shock": 9,
    "tension": 8, "suspense": 8, "sadness": 7, "anger": 7, "anxiety": 7,
    "joy": 7, "excitement": 8, "romance": 6, "hope": 6, "humour": 5, "comedy": 5,
    "calm": 3, "neutral": 4,
}
rows=[]
for scene in report.scenes:
    emotion = (scene.dominant_emotion or "neutral").strip()
    lower = emotion.lower()
    base = next((score for key, score in emotion_weight.items() if key in lower), 5)
    intensity = round((base + scene.suspense_score) / 2, 1)
    rows.append({
        "Scene": scene.scene_number,
        "Emotion": emotion,
        "Emotional intensity": intensity,
        "Suspense": scene.suspense_score,
        "Pacing": scene.pacing,
        "Heading": scene.heading,
    })

df = pd.DataFrame(rows)
if df.empty:
    st.info("No scene data is available.")
else:
    st.line_chart(df.set_index("Scene")[["Emotional intensity", "Suspense"]])
    st.dataframe(df, hide_index=True, use_container_width=True)
    peaks = df.sort_values("Emotional intensity", ascending=False).head(min(5, len(df)))
    st.subheader("Highest emotional peaks")
    for _, row in peaks.iterrows():
        st.markdown(f"**Scene {int(row['Scene'])} · {row['Heading']}** — {row['Emotion']} · intensity {row['Emotional intensity']}/10")
    st.caption("Emotional intensity is a derived planning indicator based on detected emotion and suspense, not a biometric audience measurement.")
