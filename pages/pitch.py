from __future__ import annotations

import streamlit as st

from config import ENV_CLOUDFLARE_ACCOUNT_ID, ENV_CLOUDFLARE_API_TOKEN
from core.image_generator import DEFAULT_IMAGE_MODEL, IMAGE_MODEL_OPTIONS, ImageGenerationError, generate_concept_art
from core.report_generator import generate_pitch_pptx, pitch_deck_basename
from core.ui import hero, render_bullets, require_report


report = require_report()
pitch = report.pitch_package
hero(
    "Step 14 · Pitch Generator",
    "A professional pitch package built from the screenplay: creative vision, market positioning, investor deck, poster concept, and final AI recommendation.",
)

core_tab, creative_tab, market_tab, deck_tab, final_tab = st.tabs(
    ["Core Pitch", "Creative Direction", "Market & Budget", "Investor Deck", "Final AI Report"]
)

with core_tab:
    st.subheader("Logline")
    st.success(pitch.logline)
    st.subheader("One-page synopsis")
    st.write(pitch.one_page_synopsis)
    st.subheader("Storyboard")
    st.write(f"The pitch package includes the visual plan from Step 13 ({len(report.storyboard)} frames).")
    st.page_link("pages/storyboard.py", label="Open storyboard generator", icon=":material/view_carousel:")
    st.subheader("Character profiles")
    for character in pitch.character_profiles:
        with st.container(border=True):
            st.markdown(f"**{character.name} — {character.role}**")
            st.write(character.pitch_description)

with creative_tab:
    st.subheader("Director's vision")
    st.write(pitch.directors_vision)
    left, right = st.columns(2)
    with left:
        st.subheader("Mood board")
        render_bullets(pitch.mood_board)
    with right:
        st.subheader("Poster concept")
        st.write(pitch.poster_concept)
        with st.expander("Poster art prompt"):
            st.code(pitch.poster_art_prompt, language=None)

    try:
        secret_account_id = str(st.secrets.get("CLOUDFLARE_ACCOUNT_ID", ""))
        secret_token = str(st.secrets.get("CLOUDFLARE_API_TOKEN", ""))
    except Exception:
        secret_account_id = ""
        secret_token = ""
    default_account_id = st.session_state.get("cloudflare_account_id") or ENV_CLOUDFLARE_ACCOUNT_ID or secret_account_id
    default_token = st.session_state.get("cloudflare_api_token") or ENV_CLOUDFLARE_API_TOKEN or secret_token
    with st.expander("Generate poster concept art with Cloudflare FLUX", expanded=False):
        poster_account_id = st.text_input(
            "Cloudflare Account ID",
            value=default_account_id,
            type="password",
            key="pitch_poster_account_id",
        )
        poster_token = st.text_input(
            "Cloudflare Workers AI API token",
            value=default_token,
            type="password",
            key="pitch_poster_api_token",
        )
        st.session_state.cloudflare_account_id = poster_account_id
        st.session_state.cloudflare_api_token = poster_token
        poster_model = st.selectbox(
            "Image model",
            IMAGE_MODEL_OPTIONS,
            index=IMAGE_MODEL_OPTIONS.index(DEFAULT_IMAGE_MODEL),
            key="pitch_poster_model",
        )
        if "pitch_poster_images" not in st.session_state:
            st.session_state.pitch_poster_images = {}
        cache_key = report.metadata.title
        cached = st.session_state.pitch_poster_images.get(cache_key)
        if cached:
            st.image(cached["data"], caption=f"AI poster concept · {cached['model']}", width=520)
        poster_steps = st.slider("Image generation steps", 1, 8, 4, key="pitch_poster_steps")
        if st.button("Generate poster concept", icon=":material/movie_filter:", use_container_width=True):
            if not poster_account_id.strip() or not poster_token.strip():
                st.error("Enter both your Cloudflare Account ID and Workers AI API token first.")
            else:
                with st.spinner("Generating poster concept art..."):
                    try:
                        generated = generate_concept_art(
                            prompt=pitch.poster_art_prompt,
                            account_id=poster_account_id,
                            api_token=poster_token,
                            selected_model=poster_model,
                            aspect_ratio="2:3",
                            steps=poster_steps,
                        )
                        st.session_state.pitch_poster_images[cache_key] = {
                            "data": generated.data,
                            "mime_type": generated.mime_type,
                            "model": generated.model_used,
                        }
                        st.rerun()
                    except ImageGenerationError as exc:
                        st.error(str(exc))

with market_tab:
    budget_col, audience_col = st.columns([0.8, 1.2])
    with budget_col:
        st.subheader("Budget estimate")
        st.info(pitch.budget_estimate)
        st.caption("AI planning estimate only; confirm with real quotations, crew rates, locations, insurance, post-production, and contingency.")
    with audience_col:
        st.subheader("Target audience")
        render_bullets(pitch.target_audience)
    platform_col, marketing_col = st.columns(2)
    with platform_col:
        st.subheader("Suggested platforms")
        render_bullets(pitch.suggested_platforms)
    with marketing_col:
        st.subheader("Marketing strategy")
        render_bullets(pitch.marketing_strategy)

with deck_tab:
    st.subheader("Investor pitch deck")
    for slide in pitch.investor_pitch_deck:
        with st.expander(f"Slide {slide.slide_number}: {slide.title}", expanded=slide.slide_number <= 2):
            render_bullets(slide.key_points)

    try:
        deck_bytes = generate_pitch_pptx(report)
        st.download_button(
            "Download investor pitch deck (PPTX)",
            data=deck_bytes,
            file_name=f"{pitch_deck_basename(report)}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            icon=":material/slideshow:",
            use_container_width=True,
        )
    except Exception as exc:
        st.error(f"The PPTX deck could not be generated: {exc}")

with final_tab:
    st.subheader("Final AI Report")
    score_rows = {
        "Story Structure": pitch.final_scores.story_structure,
        "Character Development": pitch.final_scores.character_development,
        "Dialogue": pitch.final_scores.dialogue,
        "Originality": pitch.final_scores.originality,
        "Horror Impact": pitch.final_scores.horror_impact,
        "Commercial Potential": pitch.final_scores.commercial_potential,
        "Streaming Potential": pitch.final_scores.streaming_potential,
        "Audience Engagement": pitch.final_scores.audience_engagement,
        "Overall Score": pitch.final_scores.overall_score,
    }
    for label, score in score_rows.items():
        col1, col2 = st.columns([3, 1])
        col1.write(label)
        col2.metric(label="", value=f"{score}/100", label_visibility="collapsed")

    st.subheader("AI Recommendation")
    st.info(pitch.ai_recommendation)

with st.expander("Edit key pitch fields"):
    with st.form("pitch_package_editor"):
        logline = st.text_area("Logline", pitch.logline)
        synopsis = st.text_area("One-page synopsis", pitch.one_page_synopsis, height=240)
        vision = st.text_area("Director's vision", pitch.directors_vision, height=180)
        budget = st.text_input("Budget estimate", pitch.budget_estimate)
        poster = st.text_area("Poster concept", pitch.poster_concept, height=130)
        recommendation = st.text_area("AI recommendation", pitch.ai_recommendation, height=180)
        submit = st.form_submit_button("Apply pitch edits")
    if submit:
        pitch.logline = logline.strip()
        pitch.one_page_synopsis = synopsis.strip()
        pitch.directors_vision = vision.strip()
        pitch.budget_estimate = budget.strip()
        pitch.poster_concept = poster.strip()
        pitch.ai_recommendation = recommendation.strip()
        report.pitch_package = pitch
        report.producer_pitch.logline = pitch.logline
        report.producer_pitch.short_synopsis = pitch.one_page_synopsis
        st.session_state.analysis_report = report
        st.success("Pitch edits applied to the current session and exported files.")
        st.rerun()
