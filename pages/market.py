from __future__ import annotations

import pandas as pd
import streamlit as st

from core.report_generator import APP_TARGET_MARKET
from core.ui import hero, render_bullets, require_report


report = require_report()
hero(
    "Originality, audience, and target market",
    "Separate the likely viewers of this screenplay from the customers of the screenplay-analysis platform.",
)

originality_tab, audience_tab, app_market_tab = st.tabs(
    ["Originality", "Screenplay audience", "App target market"]
)

with originality_tab:
    st.info(report.originality.originality_summary)
    left, right = st.columns(2)
    with left:
        st.subheader("Familiar patterns")
        render_bullets(report.originality.familiar_storytelling_patterns)
        st.subheader("Distinctive elements")
        render_bullets(report.originality.distinctive_elements)
    with right:
        st.subheader("Local identity opportunities")
        render_bullets(report.originality.local_identity_opportunities)
    st.warning(report.originality.disclaimer)

with audience_tab:
    if report.audience_prediction:
        audience_df = pd.DataFrame(
            [
                {
                    "Audience segment": item.segment,
                    "Predicted appeal": item.predicted_appeal,
                    "Appeal score": item.appeal_score,
                    "Reason": item.reason,
                }
                for item in report.audience_prediction
            ]
        )
        st.dataframe(audience_df, hide_index=True, use_container_width=True)
        st.bar_chart(audience_df.set_index("Audience segment")[["Appeal score"]])
        for item in report.audience_prediction:
            with st.expander(f"{item.segment} - {item.appeal_score}/100"):
                st.write(item.reason)
                st.markdown("#### How to improve appeal")
                render_bullets(item.improvements_for_segment)
    else:
        st.info("No reliable audience segments were returned.")
    st.caption("Audience predictions are AI estimates, not guaranteed market research results.")

with app_market_tab:
    st.subheader("Who may use or pay for Cinevora AI")
    render_bullets(APP_TARGET_MARKET)
    st.markdown(
        """
        **Possible business models**

        - Free limited analysis with paid full reports
        - Monthly writer subscription
        - University or film-school licence
        - Production-company submission screening package
        - Film competition and workshop partnership
        """
    )
