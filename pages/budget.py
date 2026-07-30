from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ui import hero, require_report

report = require_report()
hero("Budget Estimation", "Build a transparent planning estimate from shoot days, crew, cast, equipment, locations, post-production, marketing, and contingency.")

currency = st.selectbox("Currency", ["MYR", "USD", "SGD", "INR"], index=0)
left,right=st.columns(2)
with left:
    shoot_days=st.number_input("Shoot days",1,120,max(1, round(report.metadata.estimated_runtime_minutes/8)))
    crew_count=st.number_input("Crew members",1,300,18)
    crew_day=st.number_input(f"Average crew cost / person / day ({currency})",0.0,100000.0,350.0,step=50.0)
    cast_count=st.number_input("Paid cast members",0,100,6)
    cast_day=st.number_input(f"Average cast cost / person / day ({currency})",0.0,100000.0,300.0,step=50.0)
with right:
    equipment_day=st.number_input(f"Camera/lighting/sound package / day ({currency})",0.0,500000.0,1800.0,step=100.0)
    location_day=st.number_input(f"Locations/permits / day ({currency})",0.0,500000.0,600.0,step=100.0)
    art_total=st.number_input(f"Art, wardrobe, props, SFX total ({currency})",0.0,5000000.0,5000.0,step=500.0)
    post_total=st.number_input(f"Post-production total ({currency})",0.0,5000000.0,8000.0,step=500.0)
    marketing_total=st.number_input(f"Marketing/delivery total ({currency})",0.0,5000000.0,3000.0,step=500.0)
    contingency=st.slider("Contingency",0,30,10)

base = shoot_days*(crew_count*crew_day + cast_count*cast_day + equipment_day + location_day) + art_total + post_total + marketing_total
cont = base*contingency/100
total = base+cont
items = [
    ("Crew", shoot_days*crew_count*crew_day),
    ("Cast", shoot_days*cast_count*cast_day),
    ("Equipment", shoot_days*equipment_day),
    ("Locations & permits", shoot_days*location_day),
    ("Art / wardrobe / props / SFX", art_total),
    ("Post-production", post_total),
    ("Marketing / delivery", marketing_total),
    ("Contingency", cont),
]
st.metric("Estimated planning total", f"{currency} {total:,.2f}")
df=pd.DataFrame(items,columns=["Category","Estimate"])
st.dataframe(df,hide_index=True,use_container_width=True)
st.bar_chart(df.set_index("Category"))
st.info(f"Pitch-package AI estimate: {report.pitch_package.budget_estimate}")
st.caption("This is a planning calculator, not a quotation. Confirm rates, payroll, permits, insurance, tax, union/guild obligations where applicable, travel, safety, post, deliverables, and contingency with real production professionals.")
