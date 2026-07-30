from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from config import APP_NAME
from core.models import AnalysisReport


STATE_DEFAULTS = {
    "analysis_report": None,
    "raw_analysis_json": None,
    "pdf_bytes": None,
    "pdf_filename": None,
    "pdf_hash": None,
    "model_used": None,
    "analysis_saved_id": None,
    "api_key": "",
    "cloudflare_account_id": "",
    "cloudflare_api_token": "",
    "cinevora_intro_seen": False,
    "cinevora_intro_stage": 0,
    "screenplay_editor": "",
    "consultant_chat": [],
}


def init_session_state() -> None:
    for key, value in STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, (list, dict)) else value


def inject_css() -> None:
    css_path = Path(__file__).resolve().parent.parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def get_report() -> AnalysisReport | None:
    report = st.session_state.get("analysis_report")
    if isinstance(report, AnalysisReport):
        return report
    if isinstance(report, dict):
        try:
            parsed = AnalysisReport.model_validate(report)
            st.session_state.analysis_report = parsed
            return parsed
        except Exception:
            return None
    return None


def require_report() -> AnalysisReport:
    report = get_report()
    if report is None:
        st.warning("Upload and analyse a screenplay first.")
        st.page_link("pages/upload.py", label="Go to Upload & Analyse", icon=":material/upload_file:")
        st.stop()
    return report


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="sl-hero">
            <div class="sl-kicker">{APP_NAME.upper()}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_badge(label: str = "Available") -> None:
    st.markdown(f'<span class="cv-feature-badge">✓ {label}</span>', unsafe_allow_html=True)


def metric_row(values: list[tuple[str, str | int, str | None]]) -> None:
    columns = st.columns(len(values))
    for column, (label, value, help_text) in zip(columns, values):
        with column:
            st.metric(label, value, help=help_text)


def score_dataframe(report: AnalysisReport) -> pd.DataFrame:
    rows = []
    for category, score in report.scores.model_dump().items():
        rows.append({"Category": category.replace("_", " ").title(), "Score": score})
    return pd.DataFrame(rows)


def list_or_dash(items: list[str]) -> str:
    return ", ".join(items) if items else "-"


def render_bullets(items: list[str], empty_message: str = "No items identified.") -> None:
    if not items:
        st.caption(empty_message)
        return
    for item in items:
        st.markdown(f"- {item}")


def status_sidebar() -> None:
    report = get_report()
    with st.sidebar:
        st.markdown("## 🎬 Cinevora AI")
        st.caption("From Story to Screen — Powered by AI")
        st.markdown("---")
        st.markdown("### Project Status")
        if report:
            st.success(f"Loaded: {report.metadata.title}")
            st.caption(f"Writer: {report.metadata.writer}")
            if st.session_state.get("model_used"):
                st.caption(f"Model: {st.session_state.model_used}")
            st.progress(report.scores.overall_score / 100, text=f"Overall {report.scores.overall_score}/100")
        else:
            st.info("No screenplay analysed yet.")
        st.markdown("---")
        if st.button("Replay cinematic intro", icon=":material/replay:", use_container_width=True):
            st.session_state.cinevora_intro_seen = False
            st.rerun()
        st.caption("AI feedback is advisory. Originality and market features are not legal or financial guarantees.")
