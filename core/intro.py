from __future__ import annotations

import time
from pathlib import Path

import streamlit as st

from config import APP_NAME, APP_TAGLINE


def _sound_bytes() -> bytes:
    path = Path(__file__).resolve().parent.parent / "assets" / "cinevora_intro.wav"
    return path.read_bytes() if path.exists() else b""


def _visual() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"], [data-testid="stHeader"] {display:none !important;}
        .block-container {padding:0 !important; max-width:100% !important;}
        .cv-intro {
            min-height: 78vh; display:flex; align-items:center; justify-content:center;
            position:relative; overflow:hidden; border-radius:0 0 28px 28px;
            background:
              radial-gradient(circle at 50% 45%, rgba(255,180,60,.18), transparent 22%),
              radial-gradient(circle at 15% 15%, rgba(150,45,255,.25), transparent 30%),
              linear-gradient(180deg,#02040b 0%,#070915 55%,#020308 100%);
        }
        .cv-intro:before,.cv-intro:after {
            content:""; position:absolute; inset:-30%;
            background:repeating-linear-gradient(90deg,transparent 0 84px,rgba(255,255,255,.028) 85px 86px);
            transform:perspective(600px) rotateX(64deg) translateY(36%);
            animation:cv-grid 8s linear infinite;
        }
        .cv-intro:after {filter:blur(35px); opacity:.35;}
        .cv-reel {position:absolute;width:66vmin;height:66vmin;border:1px solid rgba(255,255,255,.08);border-radius:50%;animation:cv-spin 20s linear infinite;}
        .cv-reel:before,.cv-reel:after {content:"";position:absolute;border:1px solid rgba(255,195,90,.13);border-radius:50%;inset:13%;}
        .cv-reel:after {inset:31%;}
        .cv-content {position:relative;z-index:3;text-align:center;padding:2rem;animation:cv-rise 1.5s ease both;}
        .cv-eyebrow {font-size:.72rem;letter-spacing:.55em;text-transform:uppercase;color:#d5b26c;margin-bottom:1rem;}
        .cv-title {font-size:clamp(3.4rem,9vw,8.8rem);line-height:.92;margin:0;font-weight:900;letter-spacing:-.055em;
            background:linear-gradient(110deg,#fff 12%,#e8c47b 42%,#fff 62%,#a990ff 90%);-webkit-background-clip:text;color:transparent;
            text-shadow:0 0 50px rgba(232,196,123,.08);}
        .cv-rule {height:1px;width:min(520px,70vw);margin:1.6rem auto;background:linear-gradient(90deg,transparent,#d6ad5d,transparent);animation:cv-rule 1.6s ease both .5s;}
        .cv-tag {font-size:clamp(1rem,2vw,1.35rem);letter-spacing:.12em;color:#d9dbe8;text-transform:uppercase;}
        .cv-sub {margin-top:1.2rem;color:#7f8499;font-size:.88rem;letter-spacing:.08em;}
        @keyframes cv-spin {to{transform:rotate(360deg)}}
        @keyframes cv-grid {to{transform:perspective(600px) rotateX(64deg) translateY(43%)}}
        @keyframes cv-rise {from{opacity:0;transform:translateY(22px) scale(.98)}to{opacity:1;transform:none}}
        @keyframes cv-rule {from{width:0;opacity:0}to{opacity:1}}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="cv-intro">
          <div class="cv-reel"></div>
          <div class="cv-content">
            <div class="cv-eyebrow">A cinematic AI studio</div>
            <div class="cv-title">{APP_NAME}</div>
            <div class="cv-rule"></div>
            <div class="cv-tag">{APP_TAGLINE}</div>
            <div class="cv-sub">WRITE • ANALYSE • VISUALISE • PRODUCE • PITCH</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cinematic_intro() -> bool:
    """Show the Cinevora opening once per browser session, with user-triggered sound."""
    if st.session_state.get("cinevora_intro_seen"):
        return True

    _visual()
    stage = int(st.session_state.get("cinevora_intro_stage", 0))

    if stage == 0:
        left, centre, right = st.columns([1, 1.2, 1])
        with centre:
            if st.button("Enter Cinevora AI", type="primary", use_container_width=True, icon=":material/play_arrow:"):
                st.session_state.cinevora_intro_stage = 1
                st.rerun()
            st.caption("Tap Enter for the cinematic sound cue, then Cinevora opens automatically.")
        return False

    # This stage is reached only after a user gesture, which improves audio autoplay support.
    sound = _sound_bytes()
    if sound:
        st.audio(sound, format="audio/wav", autoplay=True)
    st.markdown("<p style='text-align:center;color:#d6ad5d;letter-spacing:.22em'>INITIALISING CINEVORA...</p>", unsafe_allow_html=True)
    time.sleep(2.9)
    st.session_state.cinevora_intro_seen = True
    st.session_state.cinevora_intro_stage = 0
    st.rerun()
    return False
