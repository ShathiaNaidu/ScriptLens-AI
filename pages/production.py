from __future__ import annotations

from collections import Counter

import pandas as pd
import streamlit as st

from core.ai_tools import CinevoraAIError, generate_text, report_context
from core.ui import hero, require_report

report = require_report()
hero("Production Planning", "Convert screenplay analysis into a practical scene breakdown, location plan, shooting-order starting point, and department checklist.")

rows=[]
for scene in report.scenes:
    rows.append({
        "Scene": scene.scene_number,
        "Heading": scene.heading,
        "Location": scene.location,
        "Time": scene.time_of_day,
        "Characters": ", ".join(scene.characters),
        "Purpose": scene.purpose,
        "Complexity": "High" if scene.suspense_score >= 8 or len(scene.characters) >= 6 else "Medium" if scene.suspense_score >= 5 or len(scene.characters) >= 3 else "Low",
    })
df=pd.DataFrame(rows)
st.dataframe(df, hide_index=True, use_container_width=True)

locations=Counter(scene.location for scene in report.scenes if scene.location)
if locations:
    st.subheader("Location consolidation")
    loc_df=pd.DataFrame([{"Location":k,"Scenes":v} for k,v in locations.most_common()])
    st.bar_chart(loc_df.set_index("Location")[["Scenes"]])

plan_style = st.selectbox("Planning goal", ["Low-budget shooting order", "Fastest schedule", "Location-efficient schedule", "Student production plan", "Festival short-film plan"])
if st.button("Generate production plan", type="primary", icon=":material/event_note:"):
    prompt=f"""You are Cinevora AI's production coordinator. Using only the screenplay analysis below, create a practical {plan_style}. Include assumptions, scene grouping, suggested shooting days, location consolidation, cast calls, props/wardrobe/SFX/VFX/sound considerations, safety considerations, and pre-production checklist. Do not invent exact supplier prices or claim a legal/safety approval.\n\n{report_context(report)}"""
    try:
        st.session_state.production_plan=generate_text(prompt, temperature=0.35)
    except CinevoraAIError as exc:
        st.error(str(exc))
if st.session_state.get("production_plan"):
    st.markdown(st.session_state.production_plan)
