from __future__ import annotations

import streamlit as st

from config import ENV_CLOUDFLARE_ACCOUNT_ID, ENV_CLOUDFLARE_API_TOKEN
from core.image_generator import (
    DEFAULT_IMAGE_MODEL,
    IMAGE_MODEL_OPTIONS,
    ImageGenerationError,
    generate_concept_art,
)
from core.ui import hero, require_report


report = require_report()
hero(
    "Storyboard Generator",
    "AI converts the analysed screenplay into shot-planning frames with composition, blocking, lighting, mood, and optional Cloudflare FLUX concept art.",
)

if not report.storyboard:
    st.warning(
        "This analysis does not contain storyboard panels. Re-analyse the screenplay with the updated version to generate Step 13."
    )
    st.stop()

st.caption(
    f"{len(report.storyboard)} storyboard panels generated from {report.metadata.title}. "
    "Concept art is optional and uses Cloudflare Workers AI FLUX.1 Schnell."
)

st.info(
    "Gemini creates the screenplay analysis and storyboard instructions. Cloudflare Workers AI creates only the images. "
    "If the free Cloudflare allowance is reached, the storyboard details and prompts remain fully usable."
)

with st.expander("Cloudflare concept-art settings", expanded=False):
    try:
        secret_account_id = str(st.secrets.get("CLOUDFLARE_ACCOUNT_ID", ""))
        secret_token = str(st.secrets.get("CLOUDFLARE_API_TOKEN", ""))
    except Exception:
        secret_account_id = ""
        secret_token = ""

    default_account_id = (
        st.session_state.get("cloudflare_account_id")
        or ENV_CLOUDFLARE_ACCOUNT_ID
        or secret_account_id
    )
    default_token = (
        st.session_state.get("cloudflare_api_token")
        or ENV_CLOUDFLARE_API_TOKEN
        or secret_token
    )

    account_id = st.text_input(
        "Cloudflare Account ID",
        value=default_account_id,
        type="password",
        key="storyboard_cloudflare_account_id",
        help="Use the Account ID shown on the Cloudflare Workers AI REST API page.",
    )
    api_token = st.text_input(
        "Cloudflare Workers AI API token",
        value=default_token,
        type="password",
        key="storyboard_cloudflare_api_token",
        help="The token needs Workers AI Read and Edit permissions.",
    )
    st.session_state.cloudflare_account_id = account_id
    st.session_state.cloudflare_api_token = api_token

    image_model = st.selectbox(
        "Image model",
        IMAGE_MODEL_OPTIONS,
        index=IMAGE_MODEL_OPTIONS.index(DEFAULT_IMAGE_MODEL),
        disabled=len(IMAGE_MODEL_OPTIONS) == 1,
    )
    image_steps = st.slider(
        "Image generation steps",
        min_value=1,
        max_value=8,
        value=4,
        help="Four steps is the FLUX.1 Schnell default. Higher values may take longer and use more free allocation.",
    )

if "storyboard_images" not in st.session_state:
    st.session_state.storyboard_images = {}

for panel in report.storyboard:
    st.markdown(f"### Scene {panel.scene_number} · {panel.title}")
    image_col, detail_col = st.columns([1.15, 0.85])

    cache_key = f"{report.metadata.title}:{panel.scene_number}"
    with image_col:
        cached = st.session_state.storyboard_images.get(cache_key)
        if cached:
            st.image(
                cached["data"],
                caption=f"AI concept art · {cached['model']}",
                use_container_width=True,
            )
            st.download_button(
                "Download storyboard image",
                data=cached["data"],
                file_name=f"{report.metadata.title}_scene_{panel.scene_number}_storyboard.jpg",
                mime=cached.get("mime_type", "image/jpeg"),
                key=f"download_storyboard_{panel.scene_number}",
                use_container_width=True,
            )
        else:
            st.markdown(
                f'<div class="sl-storyboard-placeholder"><div class="sl-kicker">FRAME {panel.scene_number}</div>'
                f'<h3>{panel.visual_description}</h3><p>{panel.mood}</p></div>',
                unsafe_allow_html=True,
            )

        if st.button(
            f"Generate concept art for Scene {panel.scene_number}",
            key=f"generate_storyboard_{panel.scene_number}",
            icon=":material/image:",
            use_container_width=True,
        ):
            if not account_id.strip() or not api_token.strip():
                st.error("Enter both your Cloudflare Account ID and Workers AI API token in the settings first.")
            else:
                with st.spinner(f"Generating concept art for Scene {panel.scene_number} with Cloudflare FLUX..."):
                    try:
                        generated = generate_concept_art(
                            prompt=panel.concept_art_prompt,
                            account_id=account_id,
                            api_token=api_token,
                            selected_model=image_model,
                            aspect_ratio="16:9",
                            steps=image_steps,
                        )
                        st.session_state.storyboard_images[cache_key] = {
                            "data": generated.data,
                            "mime_type": generated.mime_type,
                            "model": generated.model_used,
                        }
                        st.rerun()
                    except ImageGenerationError as exc:
                        st.error(str(exc))
                        st.caption(
                            "The screenplay analysis is already complete. You can still copy and use the image prompt below."
                        )

    with detail_col:
        st.markdown(f"**Visual:** {panel.visual_description}")
        st.markdown(f"**Camera angle:** {panel.camera_angle}")
        st.markdown(f"**Shot type:** {panel.shot_type}")
        st.markdown(f"**Character positions:** {panel.character_positions}")
        st.markdown(f"**Lighting:** {panel.lighting}")
        st.markdown(f"**Mood:** {panel.mood}")
        with st.expander("AI concept-art prompt"):
            st.text_area(
                "Prompt",
                value=panel.concept_art_prompt,
                height=180,
                key=f"storyboard_prompt_{panel.scene_number}",
            )
            st.caption("The prompt remains available even when the Cloudflare daily free allowance is exhausted.")

    st.markdown("↓" if panel != report.storyboard[-1] else "")
